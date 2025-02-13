import os
import pandas as pd

import utils as utl
from recommenders import MovieRecommender


if __name__=='__main__':
    cfg = utl.load_yml("./src/config.yaml")

    data_folder_name = cfg['dataset']
    data_folder_path = utl.get_full_path(cfg["root_path"], cfg["dataset"])

    if os.path.exists(data_folder_path):
        pass
    else:
        os.makedirs(data_folder_path)
        url = f'https://files.grouplens.org/datasets/movielens/{data_folder_name}.zip'
        utl.download_and_unzip_from_url(url, cfg["root_path"])

    recommender = MovieRecommender(data_folder_name)

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
