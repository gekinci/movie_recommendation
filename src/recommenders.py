import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.df_movies = self.get_df_movies()
        self.pop_movie_list = self.get_popular_movie_list()

    def get_df_movies(self):
        df_ratings = pd.read_csv(f"{self.folder_path}/ratings.csv")

        df_info = pd.read_csv(f"{self.folder_path}/movies.csv")
        # Splitting genres and creating binary columns
        df_genres = df_info['genres'].str.get_dummies(sep='|')
        df_genres.drop(columns=["(no genres listed)"], inplace=True)
        self.genre_list = df_genres.columns.values
        df_info = pd.concat([df_info, df_genres], axis=1)

        df_movies = pd.merge(df_info, df_ratings)
        return df_movies

    def get_popular_movie_list(self):
        df_popularity = self.df_movies.groupby("title").count()["rating"]
        df_popularity = df_popularity / df_popularity.max()
        movie_list = list(df_popularity[df_popularity>0.3].index)
        return movie_list

    def get_ratings_corr_matrix(self):
        # Correlation matrix based on ratings
        ratings_matrix = self.df_movies.pivot_table(index=['userId'], columns=['title'], values='rating')
        corr_matrix_ratings = ratings_matrix.corr(method='pearson', min_periods=50)
        return corr_matrix_ratings

    def get_genres_corr_matrix(self):
        genre_matrix = (pd.concat([self.df_movies[self.genre_list], self.df_movies["title"]], axis=1)
                        .drop_duplicates(subset=['title'])
                        .set_index("title"))
        corr_matrix_genre = pd.DataFrame(cosine_similarity(genre_matrix), index=genre_matrix.index, columns=genre_matrix.index)
        return corr_matrix_genre

    def get_similarity_score(self, new_user, adjust_rating=2.5):
        # Generate correlation matrices based on ratings and genre
        corr_ratings = self.get_ratings_corr_matrix()
        corr_genres = self.get_genres_corr_matrix()
        # Adjusting the ratings so that low rated movies have negative similarity score
        new_user = new_user - adjust_rating
        similar_movies = pd.Series()
        for i in range(0, len(new_user.index)):
            # Get similar movies based on ratings
            sim_rating = corr_ratings[new_user.index[i]].dropna()
            # More similar movies based on genre
            sim_genre = corr_genres[new_user.index[i]].dropna()
            # Now scale its similarity by how well I rated this movie
            sims = pd.concat([sim_rating, sim_genre]).map(lambda x: x * new_user.iloc[i])
            # Collecting all similar movies
            similar_movies = pd.concat([similar_movies if not similar_movies.empty else None, sims])
        similar_movies = similar_movies.groupby(similar_movies.index).sum()
        similar_movies.sort_values(inplace=True, ascending=False)
        similar_movies.drop(labels=new_user.index, inplace=True, errors='ignore')
        return similar_movies
