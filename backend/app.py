# -*- coding: utf-8 -*-
"""
JelaPedia - AI-powered District Information & Trip Planning Assistant
Main Flask application.
"""
import os
import json
import random

from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from config import SECRET_KEY, DEFAULT_LANG
from translations import t as translate
from ai_search import DistrictSearchAssistant
from quiz import generate_question
from trip_planner import suggest_districts, TAG_LABELS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "districts.json")

app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, "templates"),
    static_folder=os.path.join(FRONTEND_DIR, "static"),
)
app.secret_key = SECRET_KEY

# ---------------------------------------------------------------------
# Load data & build the AI search index once at startup
# ---------------------------------------------------------------------
with open(DATA_PATH, "r", encoding="utf-8") as f:
    DISTRICTS = json.load(f)

DISTRICTS_BY_ID = {d["id"]: d for d in DISTRICTS}
DIVISIONS = sorted({d["division_en"] for d in DISTRICTS})

search_assistant = DistrictSearchAssistant(DISTRICTS)

DID_YOU_KNOW_FACTS = [
    {"en": f"{d['name_en']} is famous for {d['famous_for_en'][0]}.",
     "bn": f"{d['name_bn']} বিখ্যাত {d['famous_for_bn'][0]}-এর জন্য।"}
    for d in DISTRICTS
]


# ---------------------------------------------------------------------
# Language helpers
# ---------------------------------------------------------------------
@app.before_request
def ensure_lang():
    if "lang" not in session:
        session["lang"] = DEFAULT_LANG


@app.context_processor
def inject_globals():
    lang = session.get("lang", DEFAULT_LANG)
    return {
        "t": lambda key: translate(key, lang),
        "lang": lang,
        "favorites": session.get("favorites", []),
    }


@app.route("/set-language/<lang_code>")
def set_language(lang_code):
    if lang_code in ("bn", "en"):
        session["lang"] = lang_code
    return redirect(request.referrer or url_for("home"))


def field(d, base):
    """Get the language-appropriate value of a bilingual field, e.g.
    field(district, 'name') -> district['name_bn'] or district['name_en']."""
    lang = session.get("lang", DEFAULT_LANG)
    return d[f"{base}_{lang}"]


app.jinja_env.globals.update(field=field)


# ---------------------------------------------------------------------
# Public pages
# ---------------------------------------------------------------------
@app.route("/")
def home():
    division_filter = request.args.get("division", "")
    q = request.args.get("q", "").strip().lower()

    districts = DISTRICTS
    if division_filter:
        districts = [d for d in districts if d["division_en"] == division_filter]
    if q:
        districts = [d for d in districts if q in d["name_en"].lower() or q in d["name_bn"]]

    fact = random.choice(DID_YOU_KNOW_FACTS)
    return render_template(
        "home.html", districts=districts, divisions=DIVISIONS,
        selected_division=division_filter, query=q, fact=fact,
        total_districts=len(DISTRICTS)
    )


@app.route("/district/<district_id>")
def district_detail(district_id):
    d = DISTRICTS_BY_ID.get(district_id)
    if not d:
        return redirect(url_for("home"))
    return render_template("district_detail.html", d=d, all_districts=DISTRICTS)


@app.route("/district/<district_id>/print")
def district_print(district_id):
    d = DISTRICTS_BY_ID.get(district_id)
    if not d:
        return redirect(url_for("home"))
    return render_template("district_print.html", d=d)


# ---------------------------------------------------------------------
# AI Search
# ---------------------------------------------------------------------
@app.route("/search")
def search_page():
    return render_template("search.html")


@app.route("/api/ask")
def api_ask():
    query = request.args.get("q", "")
    lang = session.get("lang", DEFAULT_LANG)
    result = search_assistant.answer(query, lang=lang)
    if not result:
        return jsonify({"found": False})
    d = result["district"]
    return jsonify({
        "found": True,
        "confidence": result["confidence"],
        "district": {
            "id": d["id"],
            "name": field(d, "name"),
            "division": field(d, "division"),
            "description": field(d, "description"),
            "famous_for": field(d, "famous_for"),
            "url": url_for("district_detail", district_id=d["id"]),
        }
    })


# ---------------------------------------------------------------------
# Compare
# ---------------------------------------------------------------------
@app.route("/compare")
def compare():
    id1 = request.args.get("d1", "")
    id2 = request.args.get("d2", "")
    d1 = DISTRICTS_BY_ID.get(id1)
    d2 = DISTRICTS_BY_ID.get(id2)
    return render_template("compare.html", districts=DISTRICTS, d1=d1, d2=d2)


# ---------------------------------------------------------------------
# Trip Planner
# ---------------------------------------------------------------------
@app.route("/trip-planner", methods=["GET", "POST"])
def trip_planner_page():
    suggestions = []
    selected_interests = []
    if request.method == "POST":
        selected_interests = request.form.getlist("interests")
        lang = session.get("lang", DEFAULT_LANG)
        suggestions = suggest_districts(DISTRICTS, selected_interests, lang=lang)
    return render_template(
        "trip_planner.html", suggestions=suggestions,
        selected_interests=selected_interests, tag_labels=TAG_LABELS
    )


# ---------------------------------------------------------------------
# Quiz
# ---------------------------------------------------------------------
@app.route("/quiz")
def quiz_page():
    return render_template("quiz.html")


@app.route("/api/quiz/question")
def api_quiz_question():
    lang = session.get("lang", DEFAULT_LANG)
    q = generate_question(DISTRICTS, lang=lang)
    return jsonify(q)


# ---------------------------------------------------------------------
# Insights dashboard
# ---------------------------------------------------------------------
@app.route("/insights")
def insights():
    by_division_pop = {}
    by_division_area = {}
    for d in DISTRICTS:
        by_division_pop[d["division_en"]] = by_division_pop.get(d["division_en"], 0) + d["population"]
        by_division_area[d["division_en"]] = by_division_area.get(d["division_en"], 0) + d["area_sqkm"]

    largest = max(DISTRICTS, key=lambda d: d["area_sqkm"])
    smallest = min(DISTRICTS, key=lambda d: d["area_sqkm"])
    most_populous = max(DISTRICTS, key=lambda d: d["population"])

    return render_template(
        "insights.html",
        division_labels=list(by_division_pop.keys()),
        population_values=list(by_division_pop.values()),
        area_values=list(by_division_area.values()),
        largest=largest, smallest=smallest, most_populous=most_populous,
    )


# ---------------------------------------------------------------------
# Favorites (session-based, no login needed)
# ---------------------------------------------------------------------
@app.route("/favorites/toggle/<district_id>", methods=["POST"])
def toggle_favorite(district_id):
    favs = session.get("favorites", [])
    if district_id in favs:
        favs.remove(district_id)
    else:
        favs.append(district_id)
    session["favorites"] = favs
    return redirect(request.referrer or url_for("home"))


@app.route("/favorites")
def favorites_page():
    favs = session.get("favorites", [])
    fav_districts = [DISTRICTS_BY_ID[i] for i in favs if i in DISTRICTS_BY_ID]
    return render_template("favorites.html", fav_districts=fav_districts)


# ---------------------------------------------------------------------
# REST API (for developers / other apps to consume)
# ---------------------------------------------------------------------
@app.route("/api/districts")
def api_districts():
    lang = session.get("lang", DEFAULT_LANG)
    return jsonify([
        {"id": d["id"], "name": field(d, "name"), "division": field(d, "division"),
         "area_sqkm": d["area_sqkm"], "population": d["population"]}
        for d in DISTRICTS
    ])


@app.route("/api/district/<district_id>")
def api_district(district_id):
    d = DISTRICTS_BY_ID.get(district_id)
    if not d:
        return jsonify({"error": "not found"}), 404
    return jsonify(d)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
