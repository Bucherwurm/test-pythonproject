import streamlit as st
from textblob import TextBlob

def ai_check(text):
    scores = TextBlob(text).sentiment.polarity
    if(scores > 0.05):
        sentiment = "Positive"  
    elif(scores < -0.05):
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment   

subject = st.text_input("Enter the email subject:", key="subject")
body = st.text_area("Enter the email body:", key="body")
if st.button("Check Email Sentiment"):
    full_text = subject + " " + body
    sentiment = ai_check(full_text)
    st.write(f"The sentiment of the email is: {sentiment}")     
    
   
        
