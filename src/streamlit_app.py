import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating


def get_user_ratings():
    movie_list = st.session_state["movie_list"]
    review_button = st.button("Start rating!")
    if review_button:
        st.session_state["review_button"]  = True
    if "review_button" in st.session_state.keys():
        if st.session_state["review_button"]:
            st.write("Please rate the movies you watched!")
            ratings = pd.Series()
            for i, m in enumerate(movie_list):
                r = pd.Series({m: st_star_rating(m, maxValue=5, defaultValue=0, key=f"rating_{i}")})
                ratings = pd.concat([ratings if not ratings.empty else None, r])
            return ratings


def get_recommendations(recommender, ratings, n_rec):
    rec_button = st.button("Get recommendations!")
    if rec_button:
        st.write("Here are some recommendations tailored for you!")
        recs = recommender.get_similarity_score(ratings).head(n_rec)

        st.dataframe(recs)
