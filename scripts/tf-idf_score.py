import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

file_path = "/Users/coldestblue/projects/Movie-Coverage-and-Reception-Analysis/data/movies_data.tsv"
movies_data = pd.read_csv(file_path, sep='\t', engine='python', encoding='utf-8', on_bad_lines='skip')
movies_data['Text'] = movies_data['Title'].fillna('') + " " + movies_data['Description'].fillna('')

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(movies_data['Text'])
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

word_scores = tfidf_df.sum(axis=0)
top_10_words = word_scores.sort_values(ascending=False).head(10).index
top_10_tfidf_df = tfidf_df[top_10_words]

output_file = "/Users/coldestblue/projects/Movie-Coverage-and-Reception-Analysis/data/top_10_tfidf_scores.csv"
top_10_tfidf_df.to_csv(output_file, index=False)
print("success")



