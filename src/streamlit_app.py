import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating


def get_user_ratings():
    movie_list = st.session_state["movie_list"]
    st.write("Please rate the movies you watched!")
    ratings = pd.Series()
    for i, m in enumerate(movie_list):
        r = pd.Series({m: st_star_rating(m, maxValue=5, defaultValue=0, key=f"rating_{i}")})
        ratings = pd.concat([ratings if not ratings.empty else None, r])
    return ratings


def get_recommendations(recommender, ratings, n_rec):
    st.write("Great taste! Almost there...")
    recs = recommender.get_similarity_score(ratings).head(n_rec)
    st.write("Here we go! Have fun watching!")
    st.write(recs)
