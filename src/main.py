import os
import random
import pandas as pd
import streamlit as st

import utils as utl
import streamlit_app as st_app
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

    st.title("What to watch tonight?: A movie guru")
    st.write("Let's get some movie recommendations based on your ratings!")

    # with st.sidebar:
    num_ratings = st.select_slider(label="How many movies would you like to rate?", options=range(5, 26), value=5)
    num_recommendations = st.select_slider(label="How many recommendations would you like to get?", options=range(5, 21), value=5)

    # TODO: add popularity metric for rating list
    if "movie_list" not in st.session_state.keys():
        st.session_state["movie_list"] =  random.sample(recommender.movie_list, num_ratings)
    new_user_ratings = st_app.get_user_ratings()

    st_app.get_recommendations(recommender, new_user_ratings, num_recommendations)
