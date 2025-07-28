import streamlit as st
import requests

st.title("🎬 Movie Recommendation System")

movie_input = st.text_input("Enter a movie name:")

if st.button("Get Recommendations"):
    if movie_input:
        try:
            response = requests.post("http://127.0.0.1:5000/recommend", json={"movie": movie_input})
            data = response.json()
            recommendations = data.get("recommendations", [])

            if recommendations:
                st.subheader("Recommended Movies:")
                for rec in recommendations:
                    st.write(f"- {rec}")
            else:
                st.error("No recommendations found.")
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")
    else:
        st.warning("Please enter a movie name.")