import streamlit as st

st.set_page_config(page_title="My First App", layout="wide") # page configuration
st.title("First Title") #simple title

st.write("Hello, World!") #simple text

name = st.text_input("Enter your name:", key="name") # text input

st.write(f"Hello, {name}!") # display input

num1 = st.number_input("Enter first number:", key="num1") # first number input
num2 = st.number_input("Enter second number:", key="num2") # second number input

if st.button("Add Numbers"): #tab after this
    result = num1 + num2
    st.write(f"The sum of {num1} and {num2} is {result}")

def average(num1, num2, num3):
    result = (num1+num2+num3)/3
    return result

st.write("Average Calculator")
n1 = st.number_input("Enter first number:", key="n1") 
n2 = st.number_input("Enter second number:", key="n2")
n3 = st.number_input("Enter third number:", key="n3")

if st.button("Average"): #tab after this
    avg = average(n1, n2, n3)
    st.write(f"The average is {avg}")



