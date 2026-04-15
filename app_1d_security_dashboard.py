"""
🏆 SECURITY DASHBOARD
Personal cybersecurity assessment and goal tracking
"""

import streamlit as st
import json
from datetime import datetime
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="🏆 Security Dashboard", page_icon="🏆")

st.title("🏆 Personal Security Dashboard")
st.write("Track your cybersecurity posture and improvement goals!")

st.sidebar.markdown("---")
st.sidebar.write("📊 **Dashboard Features:**")
st.sidebar.write("• Security score tracking")
st.sidebar.write("• Goal setting and progress")
st.sidebar.write("• Personalized recommendations")
st.sidebar.write("• Security habit tracking")

# Data storage functions
def load_security_data():
    try:
        with open("security_dashboard_data.json", "r") as f:
            return json.load(f)
    except:
        return {
            "assessments": [],
            "goals": [],
            "habits": [],
            "last_assessment": None
        }

def save_security_data(data):
    with open("security_dashboard_data.json", "w") as f:
        json.dump(data, f, indent=2, default=str)

security_data = load_security_data()

tab1, tab2, tab3, tab4 = st.tabs(["📊 Assessment", "🎯 Goals", "📈 Progress", "💡 Recommendations"])

with tab1:
    st.header("🛡️ Security Assessment")
    
    st.write("Answer these questions to evaluate your current cybersecurity posture:")
    
    # Assessment questions
    questions = [
        {
            "id": "unique_passwords",
            "question": "Do you use unique passwords for each important account?",
            "weight": 20,
            "category": "Password Security"
        },
        {
            "id": "password_manager",
            "question": "Do you use a password manager?",
            "weight": 15,
            "category": "Password Security"
        },
        {
            "id": "two_factor_auth",
            "question": "Do you have 2FA enabled on important accounts (email, banking, social media)?",
            "weight": 20,
            "category": "Account Security"
        },
        {
            "id": "software_updates",
            "question": "Do you keep your software and operating system updated?",
            "weight": 15,
            "category": "System Security"
        },
        {
            "id": "antivirus",
            "question": "Do you have antivirus software installed and updated?",
            "weight": 10,
            "category": "System Security"
        },
        {
            "id": "secure_browsing",
            "question": "Do you avoid clicking suspicious links and downloading unknown files?",
            "weight": 10,
            "category": "Browsing Security"
        },
        {
            "id": "wifi_security",
            "question": "Do you avoid using public WiFi for sensitive activities?",
            "weight": 5,
            "category": "Network Security"
        },
        {
            "id": "backup_strategy",
            "question": "Do you have a regular backup strategy for important data?",
            "weight": 5,
            "category": "Data Protection"
        }
    ]
    
    # Display questions
    responses = {}
    for q in questions:
        responses[q["id"]] = st.radio(
            f"**{q['question']}**",
            ["Yes", "Partially", "No"],
            key=q["id"],
            horizontal=True
        )
        st.write(f"*Category: {q['category']} | Weight: {q['weight']}%*")
        st.write("---")
    
    if st.button("📊 Calculate Security Score", type="primary"):
        # Calculate score
        total_score = 0
        max_score = sum(q["weight"] for q in questions)
        category_scores = {}
        
        for q in questions:
            response = responses[q["id"]]
            if response == "Yes":
                score = q["weight"]
            elif response == "Partially":
                score = q["weight"] * 0.5
            else:
                score = 0
            
            total_score += score
            
            # Category tracking
            if q["category"] not in category_scores:
                category_scores[q["category"]] = {"score": 0, "max": 0}
            category_scores[q["category"]]["score"] += score
            category_scores[q["category"]]["max"] += q["weight"]
        
        percentage_score = (total_score / max_score) * 100
        
        # Save assessment
        assessment = {
            "date": datetime.now().isoformat(),
            "total_score": percentage_score,
            "responses": responses,
            "category_scores": category_scores
        }
        
        security_data["assessments"].append(assessment)
        security_data["last_assessment"] = assessment
        save_security_data(security_data)
        
        # Display results
        st.success("✅ Security Assessment Complete!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Overall Security Score", f"{percentage_score:.1f}%")
        
        with col2:
            if percentage_score >= 80:
                level = "🟢 Excellent"
            elif percentage_score >= 60:
                level = "🔵 Good"
            elif percentage_score >= 40:
                level = "🟡 Fair"
            else:
                level = "🔴 Needs Work"
            st.metric("Security Level", level)
        
        with col3:
            improvement_potential = 100 - percentage_score
            st.metric("Room for Improvement", f"{improvement_potential:.1f}%")
        
        # Category breakdown
        st.subheader("📋 Category Breakdown")
        
        category_df = []
        for category, scores in category_scores.items():
            category_percentage = (scores["score"] / scores["max"]) * 100
            category_df.append({
                "Category": category,
                "Score": category_percentage,
                "Points": f"{scores['score']:.0f}/{scores['max']}"
            })
        
        category_df = pd.DataFrame(category_df)
        
        # Visualization
        fig = px.bar(category_df, x='Category', y='Score',
                    title='Security Score by Category',
                    color='Score',
                    color_continuous_scale='RdYlGn')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display category details
        for _, row in category_df.iterrows():
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"**{row['Category']}**")
            with col_b:
                st.write(f"{row['Score']:.1f}% ({row['Points']})")

with tab2:
    st.header("🎯 Security Goals")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("➕ Create New Goal")
        
        goal_title = st.text_input("Goal title:")
        goal_description = st.text_area("Description:")
        goal_category = st.selectbox("Category:", [
            "Password Security",
            "Account Security", 
            "System Security",
            "Browsing Security",
            "Network Security",
            "Data Protection",
            "Learning & Awareness"
        ])
        goal_deadline = st.date_input("Target completion date:")
        goal_priority = st.selectbox("Priority:", ["Low", "Medium", "High"])
        
        if st.button("🎯 Create Goal") and goal_title:
            goal = {
                "id": len(security_data["goals"]),
                "title": goal_title,
                "description": goal_description,
                "category": goal_category,
                "deadline": goal_deadline.isoformat(),
                "priority": goal_priority,
                "created_date": datetime.now().isoformat(),
                "completed": False,
                "progress": 0
            }
            
            security_data["goals"].append(goal)
            save_security_data(security_data)
            st.success("✅ Security goal created!")
            st.rerun()
    
    with col2:
        st.subheader("📋 Active Goals")
        
        if security_data["goals"]:
            active_goals = [goal for goal in security_data["goals"] if not goal["completed"]]
            
            for goal in active_goals:
                with st.expander(f"🎯 {goal['title']} ({goal['priority']} Priority)"):
                    st.write(f"**Category:** {goal['category']}")
                    st.write(f"**Description:** {goal['description']}")
                    st.write(f"**Deadline:** {goal['deadline']}")
                    
                    # Progress tracker
                    current_progress = st.slider("Progress:", 0, 100, goal['progress'], 
                                                key=f"goal_progress_{goal['id']}")
                    
                    if current_progress != goal['progress']:
                        goal['progress'] = current_progress
                        if current_progress >= 100:
                            goal['completed'] = True
                        save_security_data(security_data)
                    
                    st.progress(current_progress / 100)
                    
                    if st.button(f"✅ Complete", key=f"complete_goal_{goal['id']}"):
                        goal['completed'] = True
                        goal['progress'] = 100
                        save_security_data(security_data)
                        st.success("🎉 Goal completed!")
                        st.rerun()
        else:
            st.info("No goals set yet. Create your first security goal!")
    
    # Suggested goals based on last assessment
    if security_data.get("last_assessment"):
        st.subheader("💡 Suggested Goals Based on Your Assessment")
        
        last_assessment = security_data["last_assessment"]
        suggestions = []
        
        # Generate suggestions based on weak areas
        for q_id, response in last_assessment["responses"].items():
            if response in ["No", "Partially"]:
                if q_id == "unique_passwords":
                    suggestions.append({
                        "title": "Implement Unique Passwords",
                        "description": "Create unique passwords for all important accounts",
                        "category": "Password Security"
                    })
                elif q_id == "password_manager":
                    suggestions.append({
                        "title": "Set Up Password Manager",
                        "description": "Research and install a reputable password manager",
                        "category": "Password Security"
                    })
                elif q_id == "two_factor_auth":
                    suggestions.append({
                        "title": "Enable 2FA on All Accounts",
                        "description": "Activate two-factor authentication on email, banking, and social media",
                        "category": "Account Security"
                    })
        
        for suggestion in suggestions[:3]:  # Show top 3 suggestions
            if st.button(f"➕ Add Goal: {suggestion['title']}", key=f"suggest_{suggestion['title']}"):
                goal = {
                    "id": len(security_data["goals"]),
                    "title": suggestion['title'],
                    "description": suggestion['description'],
                    "category": suggestion['category'],
                    "deadline": (datetime.now().date().replace(month=datetime.now().month + 1)).isoformat(),
                    "priority": "High",
                    "created_date": datetime.now().isoformat(),
                    "completed": False,
                    "progress": 0
                }
                
                security_data["goals"].append(goal)
                save_security_data(security_data)
                st.success("✅ Suggested goal added!")
                st.rerun()

with tab3:
    st.header("📈 Security Progress Tracking")
    
    if security_data["assessments"]:
        # Progress over time
        assessments_df = pd.DataFrame(security_data["assessments"])
        assessments_df['date'] = pd.to_datetime(assessments_df['date']).dt.date
        
        fig = px.line(assessments_df, x='date', y='total_score',
                     title='Security Score Progress Over Time',
                     markers=True)
        fig.update_yaxes(range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
        
        # Latest vs First comparison
        if len(assessments_df) > 1:
            first_score = assessments_df.iloc[0]['total_score']
            latest_score = assessments_df.iloc[-1]['total_score']
            improvement = latest_score - first_score
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("First Assessment", f"{first_score:.1f}%")
            with col2:
                st.metric("Latest Assessment", f"{latest_score:.1f}%")
            with col3:
                st.metric("Improvement", f"{improvement:+.1f}%")
    
    # Goals progress
    if security_data["goals"]:
        st.subheader("🎯 Goals Progress")
        
        goals_df = pd.DataFrame(security_data["goals"])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_goals = len(goals_df)
            st.metric("Total Goals", total_goals)
        
        with col2:
            completed_goals = len(goals_df[goals_df['completed']])
            st.metric("Completed", completed_goals)
        
        with col3:
            completion_rate = (completed_goals / total_goals * 100) if total_goals > 0 else 0
            st.metric("Completion Rate", f"{completion_rate:.1f}%")
        
        with col4:
            avg_progress = goals_df['progress'].mean()
            st.metric("Average Progress", f"{avg_progress:.1f}%")
        
        # Goals by category
        if not goals_df.empty:
            category_progress = goals_df.groupby('category')['progress'].mean().reset_index()
            
            fig = px.bar(category_progress, x='category', y='progress',
                        title='Average Progress by Category')
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("Complete an assessment and set some goals to see your progress!")

with tab4:
    st.header("💡 Personalized Security Recommendations")
    
    if security_data.get("last_assessment"):
        last_assessment = security_data["last_assessment"]
        
        st.subheader("🔍 Based on Your Latest Assessment")
        
        # Priority recommendations
        priority_actions = []
        quick_wins = []
        long_term_goals = []
        
        for q_id, response in last_assessment["responses"].items():
            if response == "No":
                if q_id == "two_factor_auth":
                    priority_actions.append("🚨 **URGENT:** Enable two-factor authentication on all important accounts")
                elif q_id == "unique_passwords":
                    priority_actions.append("🚨 **URGENT:** Stop reusing passwords across accounts")
                elif q_id == "password_manager":
                    quick_wins.append("💡 **Quick Win:** Install and set up a password manager (1-2 hours)")
                elif q_id == "software_updates":
                    quick_wins.append("💡 **Quick Win:** Enable automatic updates on all devices")
                elif q_id == "antivirus":
                    quick_wins.append("💡 **Quick Win:** Install reputable antivirus software")
                elif q_id == "backup_strategy":
                    long_term_goals.append("📅 **Long-term:** Set up automated backup system")
        
        # Display recommendations
        if priority_actions:
            st.error("🚨 **Priority Actions (Do These First!)**")
            for action in priority_actions:
                st.write(action)
        
        if quick_wins:
            st.warning("💡 **Quick Wins (Easy Improvements)**")
            for win in quick_wins:
                st.write(win)
        
        if long_term_goals:
            st.info("📅 **Long-term Improvements**")
            for goal in long_term_goals:
                st.write(goal)
        
        # Overall recommendation
        score = last_assessment["total_score"]
        
        if score >= 80:
            st.success("🎉 **Excellent!** You have strong security practices. Focus on maintaining them and staying updated on new threats.")
        elif score >= 60:
            st.info("👍 **Good job!** You have solid foundations. Work on the areas identified above for even better security.")
        elif score >= 40:
            st.warning("⚠️ **Moderate security.** There are several important areas that need attention. Prioritize the urgent actions above.")
        else:
            st.error("🚨 **Security needs immediate attention!** Your current practices leave you vulnerable. Start with the priority actions immediately.")
    
    else:
        st.info("Complete a security assessment to get personalized recommendations!")
    
    # General security resources
    st.subheader("📚 Security Resources & Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Password Managers:**")
        st.write("• Bitwarden (Free/Premium)")
        st.write("• 1Password (Premium)")
        st.write("• LastPass (Free/Premium)")
        st.write("• KeePass (Free, Open Source)")
        
        st.write("**Two-Factor Authentication:**")
        st.write("• Google Authenticator")
        st.write("• Authy")
        st.write("• Microsoft Authenticator")
        st.write("• Hardware keys (YubiKey)")
    
    with col2:
        st.write("**Security Learning:**")
        st.write("• SANS Cyber Basics")
        st.write("• NIST Cybersecurity Framework")
        st.write("• Cybersecurity & Infrastructure Security Agency (CISA)")
        st.write("• KnowBe4 Security Awareness Training")
        
        st.write("**Threat Intelligence:**")
        st.write("• Have I Been Pwned")
        st.write("• VirusTotal")
        st.write("• Shodan (for advanced users)")
        st.write("• CVE Database")

st.write("💡 **Learning Outcome:** Understand security assessment methodologies, goal setting, progress tracking, and personalized security recommendations.")
