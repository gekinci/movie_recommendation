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

    def set_state_movie_list():
        st.session_state["movie_list"] = random.sample(recommender.pop_movie_list, st.session_state.n_ratings)

    num_ratings = st.slider("How many movies would you like to rate?", 5, 25, 5, key="n_ratings", on_change=set_state_movie_list)
    num_recommendations = st.slider("How many recommendations would you like to get?", 5, 10, 5)

    if "movie_list" not in st.session_state.keys():
        st.session_state["movie_list"] =  random.sample(recommender.pop_movie_list, num_ratings)

    review_button = st.button("Start rating!")

    if review_button:
        st.session_state["review_button"] = True
    if "review_button" in st.session_state.keys():
        if st.session_state["review_button"]:
            new_user_ratings = st_app.get_user_ratings()
            rec_button = st.button("Get recommendations!")
            if rec_button:
                st_app.get_recommendations(recommender, new_user_ratings, num_recommendations)
