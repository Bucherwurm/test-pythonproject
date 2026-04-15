"""
🎲 SECURE PASSWORD GENERATOR
Generate cryptographically secure passwords
"""

import streamlit as st
import string
import secrets
from zxcvbn import zxcvbn

st.set_page_config(page_title="🎲 Password Generator", page_icon="🎲")

st.title("🎲 Secure Password Generator")
st.write("Create unbreakable passwords with cryptographic security!")

st.sidebar.markdown("---")
st.sidebar.write("🔐 **Generator Features:**")
st.sidebar.write("• Cryptographically secure")
st.sidebar.write("• Customizable complexity")
st.sidebar.write("• Instant strength testing")
st.sidebar.write("• Copy-friendly output")

st.header("Password Configuration")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🎛️ Basic Settings")
    length = st.slider("Password Length:", 8, 50, 16)
    
    st.subheader("🔤 Character Types")
    include_uppercase = st.checkbox("Include Uppercase (A-Z)", True)
    include_lowercase = st.checkbox("Include Lowercase (a-z)", True)
    include_numbers = st.checkbox("Include Numbers (0-9)", True)
    include_symbols = st.checkbox("Include Symbols (!@#$)", True)

with col2:
    st.subheader("⚙️ Advanced Options")
    exclude_ambiguous = st.checkbox("Exclude ambiguous characters (0, O, l, 1)", True)
    
    custom_symbols = st.text_input("Custom symbols (optional):", placeholder="!@#$%^&*")
    
    quantity = st.number_input("Number of passwords to generate:", 1, 10, 1)

if st.button("🎲 Generate Secure Passwords", type="primary"):
    # Build character set
    chars = ""
    if include_lowercase:
        chars += string.ascii_lowercase
    if include_uppercase:
        chars += string.ascii_uppercase
    if include_numbers:
        chars += string.digits
    if include_symbols:
        if custom_symbols:
            chars += custom_symbols
        else:
            chars += "!@#$%^&*"
            
    if exclude_ambiguous:
        chars = chars.replace('0', '').replace('O', '').replace('l', '').replace('1', '')
        chars = chars.replace('I', '').replace('|', '')
    
    if chars:
        st.success(f"🔐 Generated {quantity} Secure Password{'s' if quantity > 1 else ''}:")
        
        for i in range(quantity):
            # Generate cryptographically secure password
            password = ''.join(secrets.choice(chars) for _ in range(length))
            
            # Quick strength check
            strength = zxcvbn(password)
            
            col_a, col_b = st.columns([3, 1])
            
            with col_a:
                st.code(password, language=None)
            with col_b:
                score = strength['score']
                strength_labels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
                strength_colors = ["🔴", "🟠", "🟡", "🔵", "🟢"]
                st.write(f"{strength_colors[score]} {strength_labels[score]}")
            
            # Detailed analysis for first password
            if i == 0:
                with st.expander("🔬 Detailed Analysis"):
                    col_x, col_y, col_z = st.columns(3)
                    with col_x:
                        st.metric("Strength Score", f"{score}/4")
                    with col_y:
                        crack_time = strength['crack_times_display']['offline_slow_hashing_1e4_per_second']
                        st.metric("Time to Crack", crack_time)
                    with col_z:
                        st.metric("Character Set Size", len(set(chars)))
                    
                    st.write(f"**Entropy:** ~{len(password) * 6:.0f} bits")
                    st.write(f"**Possible combinations:** {len(chars)**len(password):e}")
        
        # Copy instructions
        st.info("💡 **Tip:** Click the copy button (📋) in the top-right corner of any password box to copy it!")
        
    else:
        st.error("⚠️ Please select at least one character type!")

# Password strength comparison
st.markdown("---")
st.subheader("📊 Password Strength Comparison")

comparison_passwords = [
    ("password123", "Common weak password"),
    ("P@ssw0rd!", "Slightly better but still predictable"),
    ("MyDog'sName2023", "Personal information based"),
    ("Tr0ub4dor&3", "Strong but memorable"),
    ("correct horse battery staple", "Passphrase method")
]

st.write("**Compare different password approaches:**")

for pwd, description in comparison_passwords:
    if st.button(f"Analyze: {description}", key=pwd):
        result = zxcvbn(pwd)
        score = result['score']
        strength_labels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
        strength_colors = ["🔴", "🟠", "🟡", "🔵", "🟢"]
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.code(pwd)
        with col_b:
            st.write(f"**Strength:** {strength_colors[score]} {strength_labels[score]}")
        with col_c:
            crack_time = result['crack_times_display']['offline_slow_hashing_1e4_per_second']
            st.write(f"**Crack Time:** {crack_time}")

# Educational content
with st.expander("🧠 Understanding Cryptographic Security"):
    st.write("""
    **What makes our generator secure?**
    
    1. **Cryptographically Secure Random Number Generator (CSPRNG)**
       - Uses `secrets` module instead of `random`
       - Suitable for security-sensitive applications
       - Unpredictable even with knowledge of previous outputs
    
    2. **Entropy Calculation**
       - Entropy = log₂(possible_characters^password_length)
       - Higher entropy = harder to crack
       - Recommended minimum: 60-80 bits for strong security
    
    3. **Character Set Diversity**
       - Larger character sets increase possible combinations
       - Each additional character type exponentially increases security
       - Custom symbols allow for even more entropy
    
    **Security Best Practices:**
    - Generated passwords are never stored or logged
    - Use immediately and don't regenerate the same password
    - Store securely in a password manager
    - Never share generated passwords
    """)

st.write("💡 **Learning Outcome:** Understand cryptographic random generation, entropy, and secure password creation.")
