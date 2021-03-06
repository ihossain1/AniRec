# Following tutorial at https://www.datacamp.com/community/tutorials/recommender-systems-python

# Importing pandas due to data manip and analysis
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Storing data in a variable
# using low_memory=false to make sure it doesn't infer what type of data it's trying to parse through
# Reference: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
# data is from: https://www.kaggle.com/canggih/anime-data-score-staff-synopsis-and-genre
metadata = pd.read_csv('dataanime.csv', low_memory=False)


# Prints first three rows of anime
# print(metadata.head(3))

# Prints plot descriptions of first 10 anime
# print(metadata['Description'].head(10))

# We need to compute word vectors for each description
# Vectors are representations of words in the description
# Semantic meaning: man and king will have closer vector representations
# While something like cat and dog will have farther representations

# Using Term Frequency-Inverse Document Frequency vectors for each description
# Returns matrix where each column is a single word out of all of the words in description
# And each column is an anime (?)
# TFIDF score is the frequency of a word occurring
# Weight(importance) of the word is lowered by the number of descriptions that word shows up in

# scikit-learn has a built in TFIDF vectorizer

# import TFIDF module
# Check top

def genre_clean(x):
    if isinstance(x['Genres'], str):
        gen = str.lower(x['Genres'].replace(" ", ""))
    else:
        gen = ""
    return gen


# remove stop words (the, an, and, etc.)
tfidf = TfidfVectorizer(stop_words='english')
countVec = CountVectorizer(stop_words='english')

# replace not a number values with an empty string
metadata['Description'] = metadata['Description'].fillna('')
metadata['Genres'] = metadata.apply(genre_clean, axis=1)

# construct tfidf matrix
tfidf_matrix = tfidf.fit_transform(metadata['Description'])
countVec_matrix = countVec.fit_transform(metadata['Genres'])

# print(tfidf_matrix.shape)
# We have 15545 different vocabs for our 1563 anime
# print(tfidf.get_feature_names()[500:510])

# The matrix is now available, time to compute similarity score
# Any similarity metric is valid, I'll use cosine similarity
# use sklearn's linear_kernel to calculate because it's faster
# check top for import

# compute similarity matrix
cosine_sim_plot = linear_kernel(tfidf_matrix, tfidf_matrix)
cosine_sim_gen = linear_kernel(countVec_matrix, countVec_matrix)

# Should be a matrix of shape (1563, 1563)
# print(cosine_sim.shape)
# print(cosine_sim[1])

indices = pd.Series(metadata.index, index=metadata['Title']).drop_duplicates()
# print(indices[:10])


def get_recs(title):
    idx = indices[title]

    sim_scores_plot = list(enumerate(cosine_sim_plot[idx]))
    sim_scores_gen = list(enumerate(cosine_sim_gen[idx]))

    sim_scores_plot = sorted(sim_scores_plot, key=lambda x: x[1], reverse=True)
    sim_scores_gen = sorted(sim_scores_gen, key=lambda x: x[1], reverse=True)

    avg_sim_score = [(idx, (sc_plot + sc_gen)/2) for (idx, sc_plot), (_, sc_gen)
                     in zip(sim_scores_plot, sim_scores_gen)]

    avg_sim_score = sorted(avg_sim_score, key=lambda x: x[1], reverse=True)

    anime_indices = [i[0] for i in avg_sim_score[1:26]]

    return metadata['Title'].iloc[anime_indices]


print(get_recs("Dragon Ball"))
