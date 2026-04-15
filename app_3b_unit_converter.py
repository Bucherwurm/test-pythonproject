"""
🔄 UNIT CONVERTER
Convert between common units interactively
"""

import streamlit as st

st.set_page_config(page_title="🔄 Unit Converter", page_icon="🔄")
st.title("🔄 Unit Converter")
st.write("Convert length, mass, and temperature units easily!")

category = st.selectbox("Choose category:", ["Length", "Mass", "Temperature"])

if category == "Length":
    units = ["meters", "kilometers", "miles", "feet"]
    factors = {
        ("meters", "kilometers"): 0.001,
        ("meters", "miles"): 0.000621371,
        ("meters", "feet"): 3.28084,
        ("kilometers", "meters"): 1000,
        ("miles", "meters"): 1609.34,
        ("feet", "meters"): 0.3048,
    }
elif category == "Mass":
    units = ["grams", "kilograms", "pounds", "ounces"]
    factors = {
        ("grams", "kilograms"): 0.001,
        ("grams", "pounds"): 0.00220462,
        ("grams", "ounces"): 0.035274,
        ("kilograms", "grams"): 1000,
        ("pounds", "grams"): 453.592,
        ("ounces", "grams"): 28.3495,
    }
elif category == "Temperature":
    units = ["Celsius", "Fahrenheit", "Kelvin"]

from_unit = st.selectbox("From:", units)
to_unit = st.selectbox("To:", units)
value = st.number_input("Value:", value=0.0)

result = None
if st.button("Convert"):
    if category == "Temperature":
        if from_unit == to_unit:
            result = value
        elif from_unit == "Celsius" and to_unit == "Fahrenheit":
            result = value * 9/5 + 32
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            result = value + 273.15
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            result = (value - 32) * 5/9
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            result = (value - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            result = value - 273.15
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            result = (value - 273.15) * 9/5 + 32
    else:
        if from_unit == to_unit:
            result = value
        else:
            key = (from_unit, to_unit)
            if key in factors:
                result = value * factors[key]
            else:
                st.error("Conversion not supported.")
    if result is not None:
        st.success(f"{value} {from_unit} = {result} {to_unit}")

st.markdown("---")
st.write("💡 **Learning Outcome:** Practice unit conversion and understand relationships between units.")
