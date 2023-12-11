import streamlit as st
from datetime import datetime
from classification_script import classify_tweets
from fetchtweets import fetch_tweets
from annotated_text import annotated_text

from embedtweet import Tweet
# t = Tweet("https://twitter.com/OReillyMedia/status/901048172738482176").component()


st.set_page_config(page_title="Disaster Tweet Management")

def main_page(input_dict):

    st.markdown("<center><h1>🕊️ Tweet Analytics for Disaster & Calamity Management</h1></center>", unsafe_allow_html=True)

    if input_dict:
        tweets_dict = fetch_tweets(**input_dict)

        if tweets_dict["tweets"] != []:
            tweets = tweets_dict["tweets"]
            # st.write(tweets)    
            for tweet in tweets:

                with st.container(border=True):
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.subheader("User")
                        st.write(tweet["user"]["name"])

                    with col2:
                        st.subheader("Tweet")
                        st.write(tweet["text"])

                    with col3:
                        st.subheader("Link")
                        st.write(tweet["link"])
        else:
            st.write("Empty list returned, change parameters and retry")
    # annotated_text(("Fake", ".", "#DC143C"))


def sidebar_page():

    with st.sidebar:

        st.title("Fetch Tweets")

        keyword = st.text_input("Tweets from User, Hashtag, Term")
        mode = st.selectbox("Select the type of keyword", options=["keyword", "hashtag", "user"], index=1,
                            format_func = lambda x: "term" if x == "keyword" else x)
        number = st.number_input("Number of tweets to fetch", min_value=10, max_value=100)
        location = st.text_input("Location of the tweet")

        include_date = st.checkbox("Include date range",)
        if include_date:
            since = st.date_input("Tweet since:", value="today")
            until = st.date_input("Tweet until:", value="today")
        else:
            since = None
            until = None

        user_mention = st.text_input("User Mentions (if any)")
        btn = st.button("Search")

        if btn and keyword != "" and number != None:
            if location == "": location = None
            if user_mention == "": user_mention = None
            if mode == "keyword": mode = "term"


            return {"keyword": keyword, "number": number, "mode": mode, "near": location,
                    "since": since, "until": until, "to": user_mention}
        


if __name__ == "__main__":

    input_dict = sidebar_page()
    main_page(input_dict)