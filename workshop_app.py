import streamlit as st
import json
from datetime import datetime
from textblob import TextBlob

st.sidebar.markdown("---")
st.sidebar.write("🎓 **Workshop Topics Covered:**")
st.sidebar.write("• File Database (JSON)")
st.sidebar.write("• AI Sentiment Analysis")
st.sidebar.write("• Phishing Detection")
st.sidebar.write("• Data Visualization")

def save_load_emails():
    try:
        with open("workshop_database.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_emails(emails):
    with open("workshop_database.json", "w") as f:
        json.dump(emails, f)

def ai_check(text):
    scores = TextBlob(text).sentiment.polarity

    if scores >= 0.05:
        sentiment = "😊 Positive"
    elif scores <= -0.05:
        sentiment = "😔 Negative"
    else:
        sentiment = "😐 Neutral"

    phishing_words = [
        "urgent",
        "click now",
        "verify account",
        "suspended",
        "limited time",
        "act now",
        "money",
        "free"
    ]
    phishing_count = sum(1 for word in phishing_words if word.lower() in text.lower())

    if phishing_count >= 2:
        security = "🚨 Possible Phishing"
    elif phishing_count == 1:
        security = "⚠️ Be Careful"
    else:
        security = "✅ Looks Safe"

    return sentiment, security, scores

st.title("📧 Email Analysis Workshop")
st.write("Learn Python with AI-powered email analysis!")

emails = save_load_emails()

tab1, tab2, tab3 = st.tabs(["✍️ Write Email", "📥 Inbox", "📊 Stats"])

with tab1:
    st.header("Write New Email")

    subject = st.text_input("Subject:")
    message = st.text_area("Message:", height=200)

    if st.button("📤 Send Email"):
        if subject and message:
            sentiment, security, score = ai_check(message)
            
            email = {
                "subject": subject,
                "message": message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "sentiment": sentiment,
                "security": security,
                "score": score,
            }

            emails.append(email)
            save_emails(emails)

            st.success("✅ Email sent!")
            st.info(f"AI Analysis: {sentiment} | {security}")
        else:
            st.error("Please fill in both subject and message!")

with tab2:
    st.header("Email Inbox")

    if emails:
        for i, email in enumerate(reversed(emails)):
            with st.expander(f"📧 {email['subject']} - {email['timestamp']}"):
                st.write(f"**Message:** {email['message']}")
                st.write(f"**AI Sentiment:** {email['sentiment']}")
                st.write(f"**Security Check:** {email['security']}")
    else:
        st.info("No emails yet. Write your first email!")

with tab3:
    st.header("Email Statistics")

    if emails:
        positive = sum(1 for e in emails if "😊" in e["sentiment"])
        negative = sum(1 for e in emails if "😔" in e["sentiment"])
        neutral = sum(1 for e in emails if "😐" in e["sentiment"])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("😊 Positive", positive)
        with col2:
            st.metric("😐 Neutral", neutral)
        with col3:
            st.metric("😔 Negative", negative)
            
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            chart_data = {
                "Sentiment": ["Positive", "Neutral", "Negative"],
                "Count": [positive, neutral, negative],
            }
            st.bar_chart(chart_data, x="Sentiment", y="Count")
        with col2:
            scores = [email["score"] for email in emails]
            score_data = {"Email Index": range(len(scores)), "Sentiment Score": scores}
            st.line_chart(score_data, x="Email Index", y="Sentiment Score")

        safe = sum(1 for e in emails if "✅" in e["security"])
        warning = sum(1 for e in emails if "⚠️" in e["security"])
        phishing = sum(1 for e in emails if "🚨" in e["security"])

        st.subheader("Security Analysis")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("✅ Safe", safe)
        with col2:
            st.metric("⚠️ Careful", warning)
        with col3:
            st.metric("🚨 Phishing", phishing)

        st.markdown("---")
        chart_data = {
            "Security": ["Safe", "Careful", "Phishing"],
            "Count": [safe, warning, phishing],
        }
        st.bar_chart(chart_data, x="Security", y="Count")

    else:
        st.info("No data to analyze yet!")
