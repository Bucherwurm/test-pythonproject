"""
🔍 PASSWORD STRENGTH CHECKER
A focused cybersecurity tool for analyzing password strength
"""

import streamlit as st
from zxcvbn import zxcvbn

st.set_page_config(page_title="🔍 Password Strength Checker", page_icon="🔍")

st.title("🔍 Password Strength Checker")
st.write("Analyze your password security with advanced AI algorithms!")

st.sidebar.markdown("---")
st.sidebar.write("🛡️ **Security Tips:**")
st.sidebar.write("• Use 12+ characters")
st.sidebar.write("• Mix letters, numbers, symbols")
st.sidebar.write("• Avoid personal information")
st.sidebar.write("• Use unique passwords")

st.header("Password Analysis")

password = st.text_input("Enter password to check:", type="password")

if password:
    # Use zxcvbn for advanced password analysis
    result = zxcvbn(password)
    
    score = result['score']
    strength_labels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
    strength_colors = ["🔴", "🟠", "🟡", "🔵", "🟢"]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Strength Score", f"{score}/4")
    with col2:
        st.metric("Strength Level", f"{strength_colors[score]} {strength_labels[score]}")
    with col3:
        crack_time = result['crack_times_display']['offline_slow_hashing_1e4_per_second']
        st.metric("Time to Crack", crack_time)
    
    # Visual strength meter
    progress_value = (score + 1) / 5
    st.progress(progress_value)
    
    # Security recommendations
    if result['feedback']['suggestions']:
        st.subheader("🔧 Recommendations:")
        for suggestion in result['feedback']['suggestions']:
            st.write(f"• {suggestion}")
    
    # Advanced analysis
    with st.expander("🔬 Detailed Analysis"):
        st.write(f"**Guesses needed:** {result['guesses']:,}")
        st.write(f"**Pattern matches found:** {len(result['sequence'])}")
        if result['feedback']['warning']:
            st.warning(f"⚠️ {result['feedback']['warning']}")

# Educational content
st.markdown("---")
st.subheader("🎓 Learn About Password Security")

with st.expander("📚 How Password Strength is Calculated"):
    st.write("""
    **Advanced Analysis Factors:**
    
    1. **Length**: Longer passwords are exponentially harder to crack
    2. **Character Variety**: Mixing uppercase, lowercase, numbers, symbols
    3. **Pattern Recognition**: Avoiding common patterns like "123" or "abc"
    4. **Dictionary Attacks**: Resistance to common word lists
    5. **Personal Information**: Avoiding names, dates, addresses
    6. **Keyboard Patterns**: Avoiding sequences like "qwerty" or "asdf"
    
    **Time to Crack Estimates:**
    - Based on modern hacking hardware
    - Assumes offline attacks with specialized equipment
    - Real-world attacks may be faster or slower
    """)

with st.expander("💡 Password Best Practices"):
    st.write("""
    **Creating Strong Passwords:**
    
    ✅ **Do:**
    - Use 12+ characters (longer is better)
    - Mix character types (A-z, 0-9, symbols)
    - Use unique passwords for each account
    - Consider passphrases with random words
    - Use a password manager
    
    ❌ **Don't:**
    - Use personal information (birthdays, names)
    - Reuse passwords across accounts
    - Use common words or phrases
    - Use keyboard patterns (123456, qwerty)
    - Share passwords with others
    """)

st.write("💡 **Learning Outcome:** Understand cybersecurity principles, password entropy, and attack vectors.")
