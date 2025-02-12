import os
import pandas as pd
import numpy as np

from utils import download_and_unzip_from_url
from recommenders import MovieRecommender


if __name__=='__main__':
    folder_name = "ml-latest-small"  # "ml-latest"
    if os.path.exists(f"./{folder_name}"):
        pass
    else:
        os.makedirs(f"./{folder_name}")
        url = f'https://files.grouplens.org/datasets/movielens/{folder_name}.zip'
        download_and_unzip_from_url(url, folder_name)

    recommender = MovieRecommender(folder_name)

    new_user_ratings = {"Toy Story (1995)":5.0,
                        "Incredibles, The (2004)": 5.0,
                        "Holiday, The (2006)": 5.0,
                        "The Intern (2015)": 5.0,
                        "The Lobster (2015)": 1.0,
                        "Get Out (2017)": 1.0
                        }
    new_user_ratings = pd.Series(new_user_ratings)

    simScores = recommender.get_similarity_score(new_user_ratings)
    print(simScores.head(10))
