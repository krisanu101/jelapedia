# -*- coding: utf-8 -*-
"""
JelaPedia - Quiz generator
Builds multiple-choice trivia questions on the fly from districts.json,
so no separate quiz-question file needs to be maintained by hand.
"""
import random


def generate_question(districts, lang="bn"):
    """Return one random multiple-choice question as a dict:
    {question, options: [4 strings], answer_index, explanation}"""
    qtype = random.choice([
        "largest_area", "smallest_area", "most_populous", "division_of",
        "famous_for",
    ])

    def name(d):
        return d["name_bn"] if lang == "bn" else d["name_en"]

    def division(d):
        return d["division_bn"] if lang == "bn" else d["division_en"]

    if qtype == "largest_area":
        sample = random.sample(districts, 4)
        correct = max(sample, key=lambda d: d["area_sqkm"])
        q = "নিচের কোনটি আয়তনে সবচেয়ে বড়?" if lang == "bn" else "Which of these is the largest by area?"

    elif qtype == "smallest_area":
        sample = random.sample(districts, 4)
        correct = min(sample, key=lambda d: d["area_sqkm"])
        q = "নিচের কোনটি আয়তনে সবচেয়ে ছোট?" if lang == "bn" else "Which of these is the smallest by area?"

    elif qtype == "most_populous":
        sample = random.sample(districts, 4)
        correct = max(sample, key=lambda d: d["population"])
        q = "নিচের কোনটির জনসংখ্যা সবচেয়ে বেশি?" if lang == "bn" else "Which of these has the highest population?"

    elif qtype == "division_of":
        target = random.choice(districts)
        same_division = [d for d in districts if d["division_en"] == target["division_en"] and d["id"] != target["id"]]
        other_divisions = list({d["division_en"] for d in districts if d["division_en"] != target["division_en"]})
        wrong_divs = random.sample(other_divisions, min(3, len(other_divisions)))
        options_text = [target["division_bn"] if lang == "bn" else target["division_en"]]
        div_lookup = {d["division_en"]: d["division_bn"] for d in districts}
        for wd in wrong_divs:
            options_text.append(div_lookup[wd] if lang == "bn" else wd)
        random.shuffle(options_text)
        q = (f"{name(target)} কোন বিভাগে অবস্থিত?" if lang == "bn"
             else f"{name(target)} belongs to which division?")
        answer_text = target["division_bn"] if lang == "bn" else target["division_en"]
        answer_index = options_text.index(answer_text)
        return {
            "question": q, "options": options_text, "answer_index": answer_index,
            "explanation": ""
        }

    else:  # famous_for
        target = random.choice(districts)
        famous_key = "famous_for_bn" if lang == "bn" else "famous_for_en"
        correct_fact = random.choice(target[famous_key])
        distractor_pool = [d for d in districts if d["id"] != target["id"]]
        wrong_facts = []
        for d in random.sample(distractor_pool, 6):
            candidates = [f for f in d[famous_key] if f != correct_fact]
            if candidates:
                wrong_facts.append(random.choice(candidates))
            if len(wrong_facts) == 3:
                break
        options_text = [correct_fact] + wrong_facts[:3]
        random.shuffle(options_text)
        q = (f"নিচের কোনটি {name(target)}-এর জন্য বিখ্যাত?" if lang == "bn"
             else f"Which of these is {name(target)} famous for?")
        answer_index = options_text.index(correct_fact)
        return {
            "question": q, "options": options_text, "answer_index": answer_index,
            "explanation": ""
        }

    # for largest_area / smallest_area / most_populous
    options_text = [name(d) for d in sample]
    answer_index = options_text.index(name(correct))
    return {"question": q, "options": options_text, "answer_index": answer_index, "explanation": ""}
