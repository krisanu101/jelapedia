# -*- coding: utf-8 -*-
"""
JelaPedia - AI Search Assistant

A lightweight, fully offline "AI" search feature: it builds a small text
corpus out of every district's structured data (name, famous places, food,
rivers, description) in both languages, vectorizes it with TF-IDF, and
answers a free-text question by finding the most similar document with
cosine similarity. No external API key or internet connection required.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DistrictSearchAssistant:
    def __init__(self, districts):
        self.districts = districts
        self._build_corpus()

    def _district_text(self, d, lang):
        """Flatten one district's fields into a single searchable text blob."""
        if lang == "bn":
            parts = [
                d["name_bn"], d["division_bn"], d["description_bn"],
                " ".join(d["famous_for_bn"]), " ".join(d["food_bn"]), " ".join(d["rivers_bn"]),
            ]
        else:
            parts = [
                d["name_en"], d["division_en"], d["description_en"],
                " ".join(d["famous_for_en"]), " ".join(d["food_en"]), " ".join(d["rivers_en"]),
            ]
        return " ".join(parts)

    def _build_corpus(self):
        # One combined bilingual document per district, so a query in either
        # language can still match (e.g. an English query matching a Bangla name).
        self.corpus = [
            self._district_text(d, "en") + " " + self._district_text(d, "bn")
            for d in self.districts
        ]
        # word-level TF-IDF. Python's regex \w does NOT include Bangla
        # combining vowel signs (matras) as word characters, so the default
        # \w+ pattern would shatter Bangla words into single letters. We use
        # a whitespace/punctuation-based tokenizer instead, which keeps
        # every Bangla or English word intact.
        self.vectorizer = TfidfVectorizer(
            token_pattern=r"[^\s.,!?;:()\'\"।]+",
            lowercase=True,
        )
        self.doc_matrix = self.vectorizer.fit_transform(self.corpus)

    def search(self, query, top_k=1):
        """Return the top_k most relevant districts for a free-text query,
        each as (district_dict, confidence_score in 0..1)."""
        if not query or not query.strip():
            return []
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.doc_matrix)[0]
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        results = []
        for idx in ranked[:top_k]:
            if scores[idx] > 0:
                results.append((self.districts[idx], float(scores[idx])))
        return results

    def answer(self, query, lang="bn"):
        """Return a human-readable answer dict for a question, or None if
        nothing matched with reasonable confidence.

        Strategy: if the query directly names a district ("Sylhet", "সিলেট"),
        that's a much stronger and more reliable signal than TF-IDF similarity
        over a short question full of common words ("what", "is", "famous",
        "for") — so we check for a direct name mention first, and only fall
        back to TF-IDF similarity for descriptive queries that don't name a
        specific district (e.g. "which district has the longest beach").
        """
        direct = self._match_by_name(query)
        if direct:
            return {"district": direct, "confidence": 0.95, "raw_score": 1.0}

        results = self.search(query, top_k=1)
        if results and results[0][1] >= 0.08:
            district, score = results[0]
            return {
                "district": district,
                "confidence": round(min(score * 2.2, 0.9), 2),
                "raw_score": round(score, 4),
            }

        # Fallback: Bangla words often carry suffixes attached with no space
        # (e.g. "সুন্দরবনের" = "সুন্দরবন" + "ের"), so a short topic word like
        # "সুন্দরবন" may not match any single whitespace-delimited token even
        # though it's clearly present. A plain substring scan over the raw
        # corpus text catches these cases that token-based TF-IDF misses.
        substring_hit = self._match_by_substring(query)
        if substring_hit:
            return {"district": substring_hit, "confidence": 0.55, "raw_score": 0.0}

        if results:
            district, score = results[0]
            return {
                "district": district,
                "confidence": round(min(score * 2.2, 0.9), 2),
                "raw_score": round(score, 4),
            }
        return None

    def _match_by_substring(self, query):
        """Loose fallback: find a district whose corpus text contains the
        (cleaned) query text as a raw substring, ignoring Bangla suffixes."""
        needle = query.strip().rstrip("।?!.,;:")
        if len(needle) < 3:
            return None
        needle_lower = needle.lower()
        for i, doc in enumerate(self.corpus):
            if needle_lower in doc.lower():
                return self.districts[i]
        return None

    def _match_by_name(self, query):
        """Return the district dict if its English or Bangla name appears
        as a whole word in the query, else None."""
        q_lower = query.lower()
        best = None
        best_len = 0
        for d in self.districts:
            for name in (d["name_en"], d["name_bn"]):
                name_l = name.lower()
                if name_l in q_lower or name_l in query:
                    # prefer the longest matching name (avoids short
                    # substrings accidentally matching inside another word)
                    if len(name_l) > best_len:
                        best, best_len = d, len(name_l)
        return best
