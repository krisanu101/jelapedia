# -*- coding: utf-8 -*-
"""
JelaPedia - Trip Planner
Suggests districts based on the traveller's chosen interest tags
(beach, hill, tea, river, historical, forest, religious, haor, etc.)
"""

TAG_LABELS = {
    "beach": {"en": "beaches", "bn": "সমুদ্র সৈকত"},
    "hill": {"en": "hills & tea gardens", "bn": "পাহাড় ও চা বাগান"},
    "tea": {"en": "tea gardens", "bn": "চা বাগান"},
    "historical": {"en": "historical sites", "bn": "ঐতিহাসিক স্থান"},
    "river": {"en": "rivers", "bn": "নদী"},
    "forest": {"en": "forests", "bn": "বনাঞ্চল"},
    "religious": {"en": "religious sites", "bn": "ধর্মীয় স্থান"},
    "haor": {"en": "haor (wetlands)", "bn": "হাওর"},
    "archaeological": {"en": "archaeological sites", "bn": "প্রত্নতাত্ত্বিক স্থান"},
    "coastal": {"en": "coastal areas", "bn": "উপকূলীয় অঞ্চল"},
    "industrial": {"en": "industrial areas", "bn": "শিল্পাঞ্চল"},
    "border": {"en": "border regions", "bn": "সীমান্ত অঞ্চল"},
    "agricultural": {"en": "agricultural land", "bn": "কৃষি অঞ্চল"},
}


def suggest_districts(districts, interests, lang="bn", limit=8):
    """Rank districts by how many of the chosen interest tags they match.
    Returns a list of (district, matched_tags, reason_text)."""
    if not interests:
        return []

    scored = []
    for d in districts:
        matched = [tag for tag in interests if tag in d.get("tags", [])]
        if matched:
            scored.append((d, matched))

    scored.sort(key=lambda x: len(x[1]), reverse=True)

    results = []
    for d, matched in scored[:limit]:
        labels = [TAG_LABELS.get(tag, {}).get(lang, tag) for tag in matched]
        if lang == "bn":
            reason = f"{d['name_bn']} — " + ", ".join(labels) + "-এর জন্য পরিচিত"
        else:
            reason = f"{d['name_en']} is known for " + ", ".join(labels)
        results.append({"district": d, "matched_tags": matched, "reason": reason})
    return results
