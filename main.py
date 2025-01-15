import re
from collections import Counter
from typing import List

def clean_text(text: str) -> List[str]:
    return re.sub(r"[^\w\s]", "", text).lower().split(" ")

def calculate_corpus_stats(texts: List[List[str]]) -> dict:
    word_frequencies = Counter()
    word_total = 0
    text_index = 0
    while text_index < len(texts):
        word_frequencies.update(texts[text_index])
        word_total += len(texts[text_index])
        text_index += 1
    return {word: freq / word_total for word, freq in word_frequencies.items()}

def calculate_text_relevance(
    search_words: List[str],
    text_content: List[str],
    corpus_stats: dict,
    smoothing_factor: float = 0.5,
) -> float:
    word_freq = Counter(text_content)
    text_length = len(text_content)
    total_relevance = 0
    word_index = 0
    while word_index < len(search_words):
        word = search_words[word_index]
        text_probability = word_freq[word] / text_length if text_length > 0 else 0
        corpus_probability = corpus_stats.get(word, 0)
        final_probability = smoothing_factor * text_probability + (1 - smoothing_factor) * corpus_probability
        if final_probability > 0:
            total_relevance += final_probability
        word_index += 1
    return total_relevance

def read_search_data() -> tuple[List[List[str]], List[str]]:
    text_count = int(input().strip())
    text_collection = []
    counter = 0
    while counter < text_count:
        text = clean_text(input().strip())
        text_collection.append(text)
        counter += 1
    search_query = clean_text(input().strip())
    return text_collection, search_query

def rank_texts(
    text_collection: List[List[str]], search_query: List[str], corpus_stats: dict
) -> List[tuple[int, float]]:
    rankings = []
    idx = 0
    while idx < len(text_collection):
        relevance_score = calculate_text_relevance(search_query, text_collection[idx], corpus_stats)
        rankings.append((idx, relevance_score))
        idx += 1
    return rankings

# Execute search engine
texts, query = read_search_data()
corpus_statistics = calculate_corpus_stats(texts)
text_rankings = rank_texts(texts, query, corpus_statistics)
sorted_rankings = sorted(text_rankings, key=lambda x: x[1], reverse=True)
ranked_indices = []
i = 0
while i < len(sorted_rankings):
    ranked_indices.append(sorted_rankings[i][0])
    i += 1
print(ranked_indices)