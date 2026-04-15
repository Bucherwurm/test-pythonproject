"""
🔢 PRIME NUMBER CHECKER
Check if a number is prime and learn how it works
"""

import streamlit as st
import math

st.set_page_config(page_title="🔢 Prime Checker", page_icon="🔢")
st.title("🔢 Prime Number Checker")
st.write("Enter a number to check if it's prime. See the steps and learn the math!")

num = st.number_input("Enter a number:", min_value=2, max_value=100000, step=1)

def is_prime(n):
    if n < 2:
        return False, []
    steps = []
    for i in range(2, int(math.sqrt(n)) + 1):
        steps.append(f"Check if {n} is divisible by {i}")
        if n % i == 0:
            steps.append(f"{n} is divisible by {i} (not prime)")
            return False, steps
    steps.append(f"No divisors found. {n} is prime!")
    return True, steps

if st.button("Check Prime"):
    prime, steps = is_prime(num)
    st.subheader("Steps:")
    for s in steps:
        st.write(s)
    if prime:
        st.success(f"{num} is a prime number!")
    else:
        st.error(f"{num} is not a prime number.")

st.markdown("---")
st.write("💡 **Learning Outcome:** Understand prime numbers and basic algorithms in computing.")
