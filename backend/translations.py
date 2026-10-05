# -*- coding: utf-8 -*-
"""
JelaPedia - UI text translations (Bangla / English)
Used by the `t()` helper injected into every template via app.py's
context processor. Add a new key here whenever a template needs new
UI text, in both languages.
"""

TRANSLATIONS = {
    "site_name": {"en": "JelaPedia", "bn": "জেলাপিডিয়া"},
    "tagline": {"en": "Know every district of Bangladesh", "bn": "বাংলাদেশের প্রতিটি জেলা সম্পর্কে জানুন"},

    "nav_home": {"en": "Home", "bn": "হোম"},
    "nav_search": {"en": "AI Search", "bn": "AI সার্চ"},
    "nav_compare": {"en": "Compare", "bn": "তুলনা"},
    "nav_trip": {"en": "Trip Planner", "bn": "ভ্রমণ পরিকল্পনা"},
    "nav_quiz": {"en": "Quiz", "bn": "কুইজ"},
    "nav_insights": {"en": "Insights", "bn": "পরিসংখ্যান"},
    "nav_favorites": {"en": "Favorites", "bn": "পছন্দের তালিকা"},

    "hero_title": {"en": "Explore all 64 districts of Bangladesh", "bn": "বাংলাদেশের ৬৪টি জেলা এক জায়গায় জানুন"},
    "hero_subtitle": {
        "en": "District facts, an AI search assistant, trip planning and more — all in one place.",
        "bn": "জেলার তথ্য, AI সার্চ অ্যাসিস্ট্যান্ট, ভ্রমণ পরিকল্পনা — সবকিছু এক জায়গায়।"
    },
    "did_you_know": {"en": "Did you know?", "bn": "আপনি কি জানেন?"},
    "all_divisions": {"en": "All Divisions", "bn": "সব বিভাগ"},
    "search_placeholder": {"en": "Search a district by name...", "bn": "জেলার নাম লিখে খুঁজুন..."},
    "view_details": {"en": "View Details", "bn": "বিস্তারিত দেখুন"},

    "area": {"en": "Area", "bn": "আয়তন"},
    "population": {"en": "Population", "bn": "জনসংখ্যা"},
    "division": {"en": "Division", "bn": "বিভাগ"},
    "famous_for": {"en": "Famous For", "bn": "যা বিখ্যাত"},
    "local_food": {"en": "Local Food", "bn": "স্থানীয় খাবার"},
    "rivers": {"en": "Rivers", "bn": "নদী"},
    "sqkm": {"en": "sq km", "bn": "বর্গ কিমি"},
    "people": {"en": "people", "bn": "জন"},
    "add_favorite": {"en": "Add to Favorites", "bn": "পছন্দে যোগ করুন"},
    "remove_favorite": {"en": "Remove from Favorites", "bn": "পছন্দ থেকে সরান"},
    "download_pdf": {"en": "Download Fact Sheet", "bn": "তথ্যপত্র ডাউনলোড"},
    "compare_with": {"en": "Compare with another district", "bn": "অন্য জেলার সাথে তুলনা করুন"},

    "ai_search_title": {"en": "Ask JelaPedia AI", "bn": "জেলাপিডিয়া AI-কে জিজ্ঞাসা করুন"},
    "ai_search_subtitle": {
        "en": "Ask a question about any district — e.g. \"What is Sylhet famous for?\"",
        "bn": "যেকোনো জেলা নিয়ে প্রশ্ন করুন — যেমন \"সিলেট কীসের জন্য বিখ্যাত?\""
    },
    "ai_ask_btn": {"en": "Ask", "bn": "জিজ্ঞাসা করুন"},
    "ai_mic_hint": {"en": "Tap the mic to speak your question", "bn": "কথা বলে প্রশ্ন করতে মাইকে চাপুন"},
    "ai_no_match": {
        "en": "Couldn't find a confident answer — try mentioning a district name.",
        "bn": "নিশ্চিত উত্তর খুঁজে পাইনি — একটা জেলার নাম উল্লেখ করে চেষ্টা করুন।"
    },
    "confidence": {"en": "Confidence", "bn": "নিশ্চয়তা"},

    "compare_title": {"en": "Compare Two Districts", "bn": "দুইটি জেলার তুলনা"},
    "select_district": {"en": "Select a district", "bn": "একটি জেলা বেছে নিন"},
    "compare_btn": {"en": "Compare", "bn": "তুলনা করুন"},

    "trip_title": {"en": "Plan Your Trip", "bn": "আপনার ভ্রমণ পরিকল্পনা করুন"},
    "trip_subtitle": {
        "en": "Tell us your interests, we'll suggest matching districts.",
        "bn": "আপনার আগ্রহ বলুন, আমরা মিলিয়ে জেলা suggest করব।"
    },
    "interest_beach": {"en": "Beaches", "bn": "সমুদ্র সৈকত"},
    "interest_hill": {"en": "Hills & Tea Gardens", "bn": "পাহাড় ও চা বাগান"},
    "interest_historical": {"en": "Historical Sites", "bn": "ঐতিহাসিক স্থান"},
    "interest_river": {"en": "Rivers", "bn": "নদী"},
    "interest_forest": {"en": "Forests", "bn": "বনাঞ্চল"},
    "interest_religious": {"en": "Religious Sites", "bn": "ধর্মীয় স্থান"},
    "interest_haor": {"en": "Haor (Wetlands)", "bn": "হাওর"},
    "interest_archaeological": {"en": "Archaeological Sites", "bn": "প্রত্নতাত্ত্বিক স্থান"},
    "get_suggestions": {"en": "Get Suggestions", "bn": "পরামর্শ দেখুন"},
    "why_suggested": {"en": "Why suggested", "bn": "কেন suggest করা হলো"},

    "quiz_title": {"en": "District Trivia Quiz", "bn": "জেলা কুইজ"},
    "quiz_next": {"en": "Next Question", "bn": "পরের প্রশ্ন"},
    "quiz_correct": {"en": "Correct!", "bn": "সঠিক!"},
    "quiz_wrong": {"en": "Not quite — the correct answer was", "bn": "ভুল হয়েছে — সঠিক উত্তর ছিল"},
    "quiz_score": {"en": "Score", "bn": "স্কোর"},

    "insights_title": {"en": "Bangladesh at a Glance", "bn": "এক নজরে বাংলাদেশ"},
    "insights_by_division": {"en": "Population by Division", "bn": "বিভাগ অনুযায়ী জনসংখ্যা"},
    "insights_area_by_division": {"en": "Area by Division", "bn": "বিভাগ অনুযায়ী আয়তন"},
    "largest_district": {"en": "Largest District (Area)", "bn": "আয়তনে বৃহত্তম জেলা"},
    "smallest_district": {"en": "Smallest District (Area)", "bn": "আয়তনে ক্ষুদ্রতম জেলা"},
    "most_populous": {"en": "Most Populous District", "bn": "সর্বাধিক জনবহুল জেলা"},

    "favorites_title": {"en": "Your Favorite Districts", "bn": "আপনার পছন্দের জেলাসমূহ"},
    "no_favorites": {"en": "You haven't added any favorites yet.", "bn": "এখনো কোনো পছন্দের জেলা যোগ করেননি।"},

    "footer_note": {
        "en": "JelaPedia — an educational project. Population figures are approximate (2022 census).",
        "bn": "জেলাপিডিয়া — একটি শিক্ষামূলক প্রজেক্ট। জনসংখ্যা আনুমানিক (২০২২ আদমশুমারি)।"
    },
    "filter_btn": {"en": "Filter", "bn": "ফিল্টার"},
    "no_districts_found": {"en": "No districts found.", "bn": "কোনো জেলা পাওয়া যায়নি।"},
    "districts_word": {"en": "districts", "bn": "জেলা"},
}


def t(key, lang="bn"):
    """Translate a UI string key into the given language ('bn' or 'en')."""
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key
    return entry.get(lang, entry.get("en", key))
