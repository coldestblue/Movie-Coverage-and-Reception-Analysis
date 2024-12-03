import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

file_path = "/Users/coldestblue/projects/Movie-Coverage-and-Reception-Analysis/data/tf_idf_data.csv"
movies_data = pd.read_csv(file_path, sep=',', engine='python', encoding='utf-8', on_bad_lines='skip')

movies_data['Text'] = movies_data['Title'].fillna('') + " " + movies_data['Description'].fillna('')


stop_words = ['Moana', 'Heretic', 'Gladiator', 'Wicked', 'Red', 'very', 'this', 'that', 'she', 'he', 'his', 'her', 'also','of', 'was', 'how', 'as', 'would', 'their', 'he', 'no', 'at', 'are', 'both', 'who', 'on', 'her', 'with', 'all', 'when', 'can', 'will', 'you', 'but', 'not', 'your', 'we', 'and', 'is', 'if', 'us', 'the', 'its', 'ii', 'to', 'in', 'for', 'one', 'so', 'again', 'from', 'it']

vectorizer = TfidfVectorizer(stop_words=stop_words)
tfidf_matrix = vectorizer.fit_transform(movies_data['Text'])
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())


def compute_top_10_with_scores(df, condition, exclude_words=None):
    filtered_df = df[condition]
    word_scores = filtered_df.sum(axis=0)
    if exclude_words:
        word_scores = word_scores.drop(labels=exclude_words, errors='ignore')
    top_10 = word_scores.sort_values(ascending=False).head(10)
    return list(top_10.index), list(top_10.values)

results = {}

exclude_cast_spotlight = {'Paul', 'Ariana', 'Cynthia', 'Hugh', 'Denzel', 'Pedro', 'Dwayne', 'paul', 'ariana', 'cynthia', 'hugh', 'denzel', 'pedro', 'dwayne'}
exclude_box_office = {'box', 'office'}
exclude_words_per_topic = {
    'cast spotlight': exclude_cast_spotlight,
    'box office': exclude_box_office 
}

for topic in movies_data['Topic'].unique():
    topic_articles = movies_data[movies_data['Topic'] == topic]
    exclude_words = exclude_words_per_topic.get(topic, None)
    
    for movie in topic_articles['Movie'].unique():
        condition = (movies_data['Topic'] == topic) & (movies_data['Movie'] == movie)
        top_10_words, top_10_scores = compute_top_10_with_scores(tfidf_df, condition, exclude_words)
        results[(topic, movie)] = list(zip(top_10_words, top_10_scores))
    
    if topic == 'box office':
        condition = movies_data['Topic'] == 'box office'
        top_10_words, top_10_scores = compute_top_10_with_scores(tfidf_df, condition, exclude_words)
        results[(topic, 'All Movies')] = list(zip(top_10_words, top_10_scores))


output_file = "/Users/coldestblue/projects/Movie-Coverage-and-Reception-Analysis/data/top_10_tfidf_scores_with_values.csv"
results_expanded = []
for (topic, movie), top_10 in results.items():
    for word, score in top_10:
        results_expanded.append((topic, movie, word, score))

results_df = pd.DataFrame(results_expanded, columns=['Topic', 'Movie', 'Word', 'Score'])
results_df.to_csv(output_file, index=False)

print("successsssss")
