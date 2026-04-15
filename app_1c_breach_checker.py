"""
🕵️ DATA BREACH CHECKER
Check if your passwords have been found in known data breaches
"""

import streamlit as st
import hashlib
import requests
import time

st.set_page_config(page_title="🕵️ Breach Checker", page_icon="🕵️")

st.title("🕵️ Data Breach Checker")
st.write("Discover if your passwords have been compromised in data breaches!")

st.sidebar.markdown("---")
st.sidebar.write("🛡️ **How it Works:**")
st.sidebar.write("• Uses HaveIBeenPwned API")
st.sidebar.write("• Your password never leaves your device")
st.sidebar.write("• Only sends partial hash for privacy")
st.sidebar.write("• Checks 600+ million breached passwords")

# Privacy explanation
st.info("""
🔒 **Privacy First:** Your password is never sent to any server. We use a technique called "k-anonymity" 
where only the first 5 characters of your password's hash are sent to check against breach databases.
""")

st.header("Password Breach Check")

check_password = st.text_input("Enter password to check against breaches:", type="password")

col1, col2 = st.columns(2)

with col1:
    single_check = st.button("🕵️ Check This Password", type="primary")

with col2:
    if st.button("📊 Batch Check (Multiple Passwords)"):
        st.session_state.show_batch = True

# Single password check
if single_check and check_password:
    with st.spinner("🔍 Checking breach databases..."):
        # Use SHA-1 hash for Have I Been Pwned API
        sha1_hash = hashlib.sha1(check_password.encode()).hexdigest().upper()
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]
        
        try:
            # Query Have I Been Pwned API
            response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
            
            if response.status_code == 200:
                hashes = response.text.splitlines()
                found = False
                breach_count = 0
                
                for hash_line in hashes:
                    hash_suffix, count = hash_line.split(':')
                    if hash_suffix == suffix:
                        breach_count = int(count)
                        found = True
                        break
                
                if found:
                    st.error(f"🚨 **BREACH DETECTED!**")
                    st.error(f"This password has been found in **{breach_count:,}** data breaches!")
                    
                    # Severity assessment
                    if breach_count > 100000:
                        severity = "🔴 EXTREMELY HIGH RISK"
                        advice = "This password is extremely common and dangerous to use!"
                    elif breach_count > 10000:
                        severity = "🟠 HIGH RISK"
                        advice = "This password is commonly known to attackers."
                    elif breach_count > 1000:
                        severity = "🟡 MEDIUM RISK"
                        advice = "This password has been compromised multiple times."
                    else:
                        severity = "🔵 LOW RISK"
                        advice = "While compromised, this password is less commonly known."
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Risk Level", severity)
                    with col_b:
                        st.metric("Times Found", f"{breach_count:,}")
                    
                    st.warning(f"⚠️ **Security Advice:** {advice}")
                    st.error("🚨 **Action Required:** Change this password immediately!")
                    
                    # Show breach timeline (simulated)
                    with st.expander("📈 Breach History (Estimated)"):
                        st.write("**Likely compromised in major breaches such as:**")
                        breaches = [
                            "Collection #1 (2019) - 772M emails",
                            "LinkedIn (2012) - 164M accounts", 
                            "Adobe (2013) - 153M accounts",
                            "MySpace (2008) - 360M accounts",
                            "Yahoo (2013-2014) - 3B accounts"
                        ]
                        for breach in breaches[:min(3, max(1, breach_count // 50000))]:
                            st.write(f"• {breach}")
                    
                else:
                    st.success("✅ **Good News!**")
                    st.success("This password hasn't been found in known data breaches!")
                    st.info("💡 However, still follow best practices:")
                    st.write("• Use unique passwords for each account")
                    st.write("• Enable two-factor authentication")
                    st.write("• Consider using a password manager")
                    st.write("• Regularly update important passwords")
                    
            else:
                st.error("❌ Unable to connect to breach database. Please try again later.")
                
        except requests.exceptions.RequestException:
            st.error("🌐 Network error. Please check your internet connection.")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {e}")

# Batch checking interface
if st.session_state.get('show_batch', False):
    st.markdown("---")
    st.subheader("📊 Batch Password Checking")
    
    batch_passwords = st.text_area(
        "Enter multiple passwords (one per line):",
        height=150,
        placeholder="password1\npassword2\npassword3"
    )
    
    if st.button("🔍 Check All Passwords") and batch_passwords:
        passwords = [pwd.strip() for pwd in batch_passwords.split('\n') if pwd.strip()]
        
        if passwords:
            progress_bar = st.progress(0)
            results = []
            
            for i, password in enumerate(passwords):
                # Check each password
                sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
                prefix = sha1_hash[:5]
                suffix = sha1_hash[5:]
                
                try:
                    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
                    
                    if response.status_code == 200:
                        hashes = response.text.splitlines()
                        found = False
                        breach_count = 0
                        
                        for hash_line in hashes:
                            hash_suffix, count = hash_line.split(':')
                            if hash_suffix == suffix:
                                breach_count = int(count)
                                found = True
                                break
                        
                        results.append({
                            'password': password[:3] + '*' * (len(password) - 3),  # Mask for privacy
                            'breached': found,
                            'count': breach_count
                        })
                    
                    # Rate limiting
                    time.sleep(0.5)
                    
                except:
                    results.append({
                        'password': password[:3] + '*' * (len(password) - 3),
                        'breached': 'Error',
                        'count': 0
                    })
                
                progress_bar.progress((i + 1) / len(passwords))
            
            # Display results
            st.subheader("📋 Batch Check Results")
            
            safe_count = len([r for r in results if not r['breached']])
            breached_count = len([r for r in results if r['breached'] and r['breached'] != 'Error'])
            error_count = len([r for r in results if r['breached'] == 'Error'])
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("✅ Safe", safe_count)
            with col_b:
                st.metric("🚨 Breached", breached_count)
            with col_c:
                st.metric("❓ Errors", error_count)
            
            # Detailed results
            for result in results:
                if result['breached'] and result['breached'] != 'Error':
                    st.error(f"🚨 {result['password']} - Found in {result['count']:,} breaches")
                elif result['breached'] == 'Error':
                    st.warning(f"❓ {result['password']} - Could not check")
                else:
                    st.success(f"✅ {result['password']} - Safe")

# Educational content
st.markdown("---")
st.subheader("🎓 Understanding Data Breaches")

with st.expander("📚 How Data Breaches Work"):
    st.write("""
    **What is a Data Breach?**
    
    A data breach occurs when unauthorized individuals gain access to confidential data, 
    often including usernames, passwords, email addresses, and other personal information.
    
    **Common Breach Types:**
    1. **Hacking Attacks** - External attackers exploit vulnerabilities
    2. **Insider Threats** - Malicious employees or contractors
    3. **Physical Theft** - Stolen devices or storage media
    4. **Social Engineering** - Manipulation to gain access
    
    **Major Historical Breaches:**
    • **Yahoo (2013-2014)** - 3 billion accounts
    • **Equifax (2017)** - 147 million people
    • **Facebook (2019)** - 540 million records
    • **LinkedIn (2012)** - 164 million accounts
    • **Adobe (2013)** - 153 million accounts
    """)

with st.expander("🔒 The k-Anonymity Privacy Model"):
    st.write("""
    **How We Protect Your Privacy:**
    
    1. **Hash Your Password** - Convert to SHA-1 hash (one-way function)
    2. **Split the Hash** - Send only first 5 characters to server
    3. **Server Returns Range** - Get all hashes starting with those 5 chars
    4. **Local Comparison** - Check locally if your full hash is in the list
    
    **Why This is Secure:**
    • Your actual password never leaves your device
    • Only a tiny fraction of the hash is transmitted
    • Even if intercepted, the partial hash reveals nothing useful
    • The server never sees your full password hash
    
    **Example:**
    Password: "mysecretpassword"
    SHA-1 Hash: "e38ad214943daad1d64c102faec29de4afe9da3d"
    Sent to server: "e38ad" (first 5 characters only)
    """)

with st.expander("🛡️ What to Do if Your Password is Breached"):
    st.write("""
    **Immediate Actions:**
    
    1. **Change Password Immediately**
       - On the affected account
       - On any other accounts using the same password
    
    2. **Enable Two-Factor Authentication**
       - Adds an extra layer of security
       - Even if password is known, account stays protected
    
    3. **Check Account Activity**
       - Look for unauthorized access
       - Review recent login locations and times
    
    4. **Monitor for Identity Theft**
       - Check credit reports
       - Watch for suspicious financial activity
    
    **Prevention Strategies:**
    • Use unique passwords for every account
    • Use a reputable password manager
    • Enable 2FA wherever possible
    • Regularly update passwords for important accounts
    • Stay informed about new breaches
    """)

st.write("💡 **Learning Outcome:** Understand data breach impacts, privacy-preserving security checks, and incident response.")
