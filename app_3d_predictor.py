"""
🔮 SIMPLE PREDICTOR
Predict outcomes using basic AI models
"""

import streamlit as st
import random
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="🔮 Predictor", page_icon="🔮")
st.title("🔮 Simple Predictor")
st.write("Enter numbers and let AI predict the next value!")

st.markdown("Enter a sequence of numbers (e.g. 2, 4, 6, 8):")
seq = st.text_input("Sequence:")

if seq:
    nums = [float(x.strip()) for x in seq.split(",") if x.strip()]
    if len(nums) >= 2:
        X = np.arange(len(nums)).reshape(-1, 1)
        y = np.array(nums)
        model = LinearRegression()
        model.fit(X, y)
        next_idx = len(nums)
        pred = model.predict(np.array([[next_idx]]))[0]
        st.success(f"Predicted next value: {pred:.2f}")
        st.write("(Uses linear regression to predict the next value in your sequence)")
    else:
        st.warning("Enter at least 2 numbers for prediction.")

st.markdown("---")
st.write("💡 **Learning Outcome:** See how simple AI models can make predictions from data.")
