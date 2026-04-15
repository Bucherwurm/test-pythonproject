# menu_planner_csv.py
# Enhanced with "Show Alternatives" feature for variety

import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime

# ======================
# 1. CONSTANTS & DEFAULTS
# ======================

CALORIE_GUIDELINES = {
    'casual': {'min': 400, 'max': 700},
    'business': {'min': 500, 'max': 800},
    'birthday': {'min': 600, 'max': 1000},
    'wedding': {'min': 700, 'max': 1200},
    'family': {'min': 600, 'max': 900},
    'festival': {'min': 700, 'max': 1100},
    'dashain': {'min': 800, 'max': 1300},
    'tihar': {'min': 750, 'max': 1200},
    'healthy': {'min': 300, 'max': 600}
}

# ======================
# 2. ENHANCED MATCHING ALGORITHM WITH VARIETY
# ======================

def get_recommendations(criteria, menu_df, variation_level=0):
    """
    Generate recommendations with variation control
    variation_level: 0 = standard, 1 = some variety, 2 = completely different
    """
    if menu_df is None or len(menu_df) == 0:
        return pd.DataFrame(), 0
    
    filtered = menu_df.copy()
    
    # Apply basic filters
    filtered = apply_basic_filters(filtered, criteria)
    
    if len(filtered) == 0:
        return pd.DataFrame(), 0
    
    # Add variation based on variation_level
    if variation_level > 0:
        filtered = add_variation(filtered, criteria, variation_level)
    
    # Create balanced meal plan
    final_items, total_calories = create_meal_plan(filtered, criteria)
    
    return pd.DataFrame(final_items), total_calories

def apply_basic_filters(df, criteria):
    """Apply all basic filters"""
    filtered = df.copy()
    
    # Budget filter
    if criteria['budget_per_person'] > 0:
        filtered = filtered[filtered['price'] <= criteria['budget_per_person']]
    
    # Dietary restrictions
    if criteria['dietary'] != 'any':
        dietary_map = {
            'vegetarian': ['vegetarian', 'vegan'],
            'vegan': ['vegan'],
            'pescatarian': ['pescatarian'],
            'gluten-free': [],  # Special handling below
            'non-vegetarian': ['regular', 'non-vegetarian']
        }
        
        if criteria['dietary'] in dietary_map:
            diets = dietary_map[criteria['dietary']]
            if diets:
                filtered = filtered[filtered['dietary'].isin(diets)]
            elif criteria['dietary'] == 'gluten-free':
                filtered = filtered[~filtered['allergens'].str.contains('gluten', na=False)]
    
    # Allergen avoidance
    if criteria['allergens']:
        for allergen in criteria['allergens']:
            filtered = filtered[~filtered['allergens'].str.contains(allergen, na=False)]
    
    # Beverage preference
    if criteria['include_beverage'] != 'any':
        if criteria['include_beverage'] == 'none':
            filtered = filtered[~filtered['category'].str.contains('beverage|drink', na=False)]
        elif criteria['beverage_only']:
            beverage_filtered = filtered[filtered['category'].str.contains('beverage|drink', na=False)]
            if 'beverage_type' in filtered.columns:
                beverage_filtered = beverage_filtered[beverage_filtered['beverage_type'] == criteria['include_beverage']]
            filtered = beverage_filtered
    
    return filtered

def add_variation(df, criteria, variation_level):
    """Add variation to recommendations"""
    if len(df) < 5:  # Not enough items for variation
        return df
    
    # Create scoring for variation
    df = df.copy()
    
    # Start with popularity if available
    if 'popularity' in df.columns:
        df['base_score'] = df['popularity'] * 0.5
    else:
        df['base_score'] = 0
    
    # Price variation (prefer mid-range for variety)
    if variation_level == 1:
        # Mild variation: slightly different price points
        avg_price = df['price'].mean()
        df['price_score'] = 1 / (1 + abs(df['price'] - avg_price) / avg_price)
        df['base_score'] += df['price_score'] * 2
    elif variation_level >= 2:
        # Strong variation: actively seek different items
        df['price_score'] = np.random.rand(len(df)) * 2
        df['base_score'] += df['price_score']
    
    # Category variation
    if 'category' in df.columns:
        category_counts = df['category'].value_counts()
        if variation_level >= 1:
            # Penalize over-represented categories
            df['category_score'] = df['category'].apply(
                lambda x: 1 / (category_counts.get(x, 1))
            )
            df['base_score'] += df['category_score'] * (variation_level * 2)
    
    # Tag variation for occasion
    occasion = criteria.get('occasion', 'casual')
    if 'tags' in df.columns and variation_level >= 1:
        # For variety, sometimes suggest non-obvious items
        df['occasion_score'] = df['tags'].apply(
            lambda x: 1 if occasion in str(x).lower() else 0.5
        )
        df['base_score'] += df['occasion_score'] * (1 - variation_level * 0.3)
    
    # Sort by variation-influenced score
    df = df.sort_values('base_score', ascending=False)
    
    return df

def create_meal_plan(filtered, criteria):
    """Create balanced meal plan"""
    final_items = []
    remaining_budget = criteria['budget_per_person']
    total_calories = 0
    
    # Get calorie target
    calorie_target = CALORIE_GUIDELINES.get(criteria['occasion'], CALORIE_GUIDELINES['casual'])
    min_calories = calorie_target['min']
    max_calories = calorie_target['max']
    
    # Separate food and beverages
    food_items = filtered[~filtered['category'].str.contains('beverage|drink', na=False)]
    beverage_items = filtered[filtered['category'].str.contains('beverage|drink', na=False)]
    
    # Build balanced meal
    if not criteria.get('beverage_only', False):
        categories_order = ['starter', 'main', 'dessert', 'side']
        
        for category in categories_order:
            if category in food_items['category'].unique():
                cat_items = food_items[food_items['category'] == category].copy()
                
                if len(cat_items) > 0:
                    # Score items for this category
                    cat_items = score_category_items(cat_items, category, remaining_budget)
                    
                    for _, item in cat_items.iterrows():
                        if item['name'] not in [i['name'] for i in final_items]:
                            item_calories = item.get('calories', 0)
                            
                            if (total_calories + item_calories <= max_calories and 
                                item['price'] <= remaining_budget):
                                
                                final_items.append(item)
                                total_calories += item_calories
                                remaining_budget -= item['price']
                                break
    
    # Add beverage if requested and budget allows
    if criteria['include_beverage'] != 'none' and len(beverage_items) > 0:
        beverage_items = beverage_items.sort_values('price', ascending=True)
        for _, beverage in beverage_items.iterrows():
            if beverage['price'] <= remaining_budget:
                final_items.append(beverage)
                total_calories += beverage.get('calories', 0)
                remaining_budget -= beverage['price']
                break
    
    return final_items, total_calories

def score_category_items(items, category, remaining_budget):
    """Score items within a category"""
    items = items.copy()
    items['score'] = 0
    
    # Score by price efficiency
    if remaining_budget > 0:
        items['price_score'] = (remaining_budget - items['price']) / remaining_budget
        items['score'] += items['price_score'] * 2
    
    # Score by calories (if available)
    if 'calories' in items.columns:
        if category == 'starter':
            ideal_cal = 200
        elif category == 'main':
            ideal_cal = 500
        elif category == 'dessert':
            ideal_cal = 250
        elif category == 'side':
            ideal_cal = 150
        else:
            ideal_cal = 300
        
        items['calorie_score'] = 1 / (1 + abs(items['calories'] - ideal_cal) / ideal_cal)
        items['score'] += items['calorie_score']
    
    # Score by popularity if available
    if 'popularity' in items.columns:
        items['score'] += items['popularity'] * 0.1
    
    # Sort by score
    items = items.sort_values('score', ascending=False)
    
    return items

def get_alternative_recommendations(criteria, menu_df, previous_selections, variation_level=2):
    """Get completely different recommendations avoiding previous selections"""
    if menu_df is None or len(menu_df) == 0:
        return pd.DataFrame(), 0
    
    # Remove previously selected items
    available_items = menu_df.copy()
    if previous_selections and len(previous_selections) > 0:
        previous_names = [item['name'] for item in previous_selections]
        available_items = available_items[~available_items['name'].isin(previous_names)]
    
    # If too few items, expand to all items but with different scoring
    if len(available_items) < 5:
        available_items = menu_df.copy()
        variation_level = 3  # Force maximum variation
    
    # Apply higher variation
    criteria_with_variation = criteria.copy()
    
    # Get recommendations with maximum variation
    recommendations, total_calories = get_recommendations(
        criteria_with_variation, 
        available_items, 
        variation_level=variation_level
    )
    
    return recommendations, total_calories

# ======================
# 3. STREAMLIT UI ENHANCEMENTS
# ======================

# Initialize session state for tracking previous selections
if 'previous_recommendations' not in st.session_state:
    st.session_state.previous_recommendations = []
if 'current_recommendation_set' not in st.session_state:
    st.session_state.current_recommendation_set = None
if 'recommendation_count' not in st.session_state:
    st.session_state.recommendation_count = 0

# Add to your existing Streamlit code, in the TAB 3 section:

# In the recommendations section, add these features:

# MODIFIED RECOMMENDATIONS SECTION
# Ensure tab3 is defined (create tabs if missing)
if 'tab3' not in globals():
    # Create three tabs; adjust labels if your app defines different tabs elsewhere
    t1, t2, tab3 = st.tabs(["Menu Upload", "Settings", "Recommendations"])

with tab3:
    st.header("📋 Get Recommendations")
    
    if not st.session_state.menu_uploaded:
        st.warning("⚠️ Please upload a menu CSV file first.")
    elif st.session_state.current_menu is None:
        st.error("❌ No menu data available.")
    else:
        # Prepare criteria
        criteria = {
            'num_people': st.session_state.get('num_people', 4),
            'budget_per_person': st.session_state.get('budget_per_person', 1000),
            'dietary': st.session_state.get('dietary', 'any'),
            'allergens': st.session_state.get('allergens', []),
            'occasion': st.session_state.get('occasion', 'casual'),
            'include_beverage': st.session_state.get('include_beverage', 'any'),
            'beverage_only': st.session_state.get('beverage_only', False)
        }
        
        # VARIATION CONTROLS
        st.subheader("🎲 Recommendation Variety")
        
        col_var1, col_var2 = st.columns(2)
        
        with col_var1:
            variation_level = st.slider(
                "Variation Level",
                min_value=0,
                max_value=3,
                value=0,
                step=1,
                help="0: Standard recommendations\n1: Mild variation\n2: Different options\n3: Maximum variety"
            )
        
        with col_var2:
            show_alternatives = st.checkbox(
                "Show alternative options",
                value=False,
                help="Get completely different recommendations"
            )
        
        # Generate button
        generate_col1, generate_col2 = st.columns([3, 1])
        
        with generate_col1:
            if st.button("🎯 Generate Recommendations", type="primary", use_container_width=True):
                with st.spinner("Analyzing menu and generating recommendations..."):
                    if show_alternatives and st.session_state.current_recommendation_set is not None:
                        # Get alternatives avoiding previous selections
                        previous_items = []
                        if st.session_state.current_recommendation_set is not None:
                            previous_items = st.session_state.current_recommendation_set.to_dict('records')
                        
                        recommendations, total_calories = get_alternative_recommendations(
                            criteria, 
                            st.session_state.current_menu,
                            previous_items,
                            variation_level=variation_level
                        )
                        
                        # Store as new recommendation set
                        st.session_state.current_recommendation_set = recommendations.copy()
                        st.session_state.recommendation_count += 1
                        st.session_state.previous_recommendations.append({
                            'set': recommendations.copy(),
                            'criteria': criteria.copy(),
                            'timestamp': datetime.now()
                        })
                    else:
                        # Standard recommendations
                        recommendations, total_calories = get_recommendations(
                            criteria, 
                            st.session_state.current_menu,
                            variation_level=variation_level
                        )
                        st.session_state.current_recommendation_set = recommendations.copy()
                        st.session_state.recommendation_count = 1
        
        with generate_col2:
            if st.session_state.recommendation_count > 0:
                st.metric("Recommendation Set", f"#{st.session_state.recommendation_count}")
        
        # Display recommendations if available
        if (st.session_state.current_recommendation_set is not None and 
            len(st.session_state.current_recommendation_set) > 0):
            
            recommendations = st.session_state.current_recommendation_set
            calorie_target = CALORIE_GUIDELINES.get(criteria['occasion'], CALORIE_GUIDELINES['casual'])
            total_calories = recommendations['calories'].sum() if 'calories' in recommendations.columns else 0
            
            # Success message with variety indicator
            if variation_level == 0:
                variety_msg = "Standard"
            elif variation_level == 1:
                variety_msg = "Mild Variation"
            elif variation_level == 2:
                variety_msg = "Different Options"
            else:
                variety_msg = "Maximum Variety"
            
            if show_alternatives:
                st.success(f"✅ Alternative Set #{st.session_state.recommendation_count} ({variety_msg})")
            else:
                st.success(f"✅ Found {len(recommendations)} recommendations ({variety_msg})")
            
            # Display each recommendation
            total_cost_per_person = recommendations['price'].sum()
            
            for idx, (_, item) in enumerate(recommendations.iterrows(), 1):
                with st.container():
                    cols = st.columns([3, 1, 1, 1])
                    
                    with cols[0]:
                        # Category emoji
                        category = item.get('category', '').lower()
                        emoji = {
                            'starter': '🥗',
                            'main': '🍝',
                            'dessert': '🍰',
                            'beverage': '🥤',
                            'side': '🍟'
                        }.get(category, '🍽️')
                        
                        st.markdown(f"### {emoji} {item['name']}")
                        
                        if 'category' in item and pd.notna(item['category']):
                            st.markdown(f"**Category:** {item['category'].title()}")
                        
                        if 'dietary' in item and pd.notna(item['dietary']):
                            st.markdown(f"**Dietary:** {item['dietary'].title()}")
                    
                    with cols[1]:
                        price = item['price']
                        st.metric("Price", f"रू {price:,.0f}")
                    
                    with cols[2]:
                        if 'calories' in item:
                            calories = item['calories']
                            st.metric("Calories", f"{calories:.0f} kcal")
                    
                    with cols[3]:
                        if criteria['budget_per_person'] > 0:
                            budget_pct = (price / criteria['budget_per_person']) * 100
                            st.progress(min(budget_pct / 100, 1.0))
                            st.caption(f"{budget_pct:.0f}% of budget")
                    
                    # Variety indicator
                    if variation_level > 0:
                        variety_stars = "★" * variation_level + "☆" * (3 - variation_level)
                        st.caption(f"Variety: {variety_stars}")
                    
                    st.divider()
            
            # ALTERNATIVES SECTION
            st.subheader("🔄 Want Different Options?")
            
            alt_col1, alt_col2, alt_col3 = st.columns(3)
            
            with alt_col1:
                if st.button("🔄 Get Alternative Set", use_container_width=True):
                    # Trigger alternative generation
                    st.session_state.show_alternatives = True
                    st.rerun()
            
            with alt_col2:
                # Quick alternative with different budget
                alt_budget = int(criteria['budget_per_person'] * 0.8)  # 80% of current
                if st.button(f"Try रू {alt_budget:,.0f} Budget", use_container_width=True):
                    st.session_state.budget_per_person = alt_budget
                    st.rerun()
            
            with alt_col3:
                # Quick alternative with different dietary
                current_diet = criteria['dietary']
                alt_diets = ['vegetarian', 'non-vegetarian', 'vegan', 'any']
                alt_diets = [d for d in alt_diets if d != current_diet]
                if alt_diets:
                    if st.button(f"Try {alt_diets[0].title()}", use_container_width=True):
                        st.session_state.dietary = alt_diets[0]
                        st.rerun()
            
            # PREVIOUS RECOMMENDATIONS HISTORY
            if len(st.session_state.previous_recommendations) > 1:
                with st.expander("📋 View Previous Recommendation Sets"):
                    st.write(f"You have {len(st.session_state.previous_recommendations)} saved recommendation sets")
                    
                    for i, rec_set in enumerate(st.session_state.previous_recommendations[-3:], 1):
                        set_num = len(st.session_state.previous_recommendations) - 3 + i
                        st.markdown(f"**Set #{set_num}**")
                        
                        # Display summary
                        if 'set' in rec_set and isinstance(rec_set['set'], pd.DataFrame):
                            set_df = rec_set['set']
                            col_sum1, col_sum2, col_sum3 = st.columns(3)
                            with col_sum1:
                                st.metric("Items", len(set_df))
                            with col_sum2:
                                total_price = set_df['price'].sum()
                                st.metric("Total", f"रू {total_price:,.0f}")
                            with col_sum3:
                                if st.button(f"Load Set #{set_num}", key=f"load_set_{set_num}"):
                                    st.session_state.current_recommendation_set = set_df
                                    st.rerun()
                        
                        st.divider()
            
            # SMART SUGGESTIONS FOR VARIETY
            st.subheader("💡 Smart Suggestions for Variety")
            
            suggestion_cols = st.columns(3)
            
            with suggestion_cols[0]:
                st.markdown("**Try Different Categories:**")
                menu_df = st.session_state.current_menu
                categories = menu_df['category'].unique()
                for cat in categories[:3]:
                    cat_count = len(recommendations[recommendations['category'] == cat])
                    if cat_count == 0:
                        st.caption(f"• Add a {cat} item")
            
            with suggestion_cols[1]:
                st.markdown("**Price Range:**")
                current_avg = recommendations['price'].mean()
                min_price = menu_df['price'].min()
                max_price = menu_df['price'].max()
                
                if current_avg > (min_price + max_price) / 2:
                    st.caption("• Try more budget-friendly options")
                else:
                    st.caption("• Try some premium items")
            
            with suggestion_cols[2]:
                st.markdown("**Calorie Balance:**")
                if 'calories' in recommendations.columns:
                    current_cal = recommendations['calories'].sum()
                    target_min = calorie_target['min']
                    target_max = calorie_target['max']
                    
                    if current_cal < target_min:
                        st.caption("• Add heartier items")
                    elif current_cal > target_max:
                        st.caption("• Try lighter options")
                    else:
                        st.caption("• Perfectly balanced!")
            
            # RANDOMIZER FEATURE
            st.subheader("🎲 Randomizer")
            
            rand_col1, rand_col2 = st.columns(2)
            
            with rand_col1:
                if st.button("🎲 Surprise Me!", use_container_width=True):
                    # Randomize criteria slightly
                    new_budget = random.choice([
                        int(criteria['budget_per_person'] * 0.7),
                        int(criteria['budget_per_person'] * 1.3),
                        random.randint(500, 2000)
                    ])
                    st.session_state.budget_per_person = new_budget
                    
                    # Random dietary if not strict
                    if criteria['dietary'] == 'any':
                        diets = ['vegetarian', 'non-vegetarian', 'vegan', 'pescatarian']
                        st.session_state.dietary = random.choice(diets)
                    
                    st.rerun()
            
            with rand_col2:
                if st.button("🔀 Shuffle Current Set", use_container_width=True):
                    # Keep same items but shuffle quantities/combinations
                    if len(recommendations) > 1:
                        # Create new combination from same items
                        shuffled = recommendations.sample(frac=1).reset_index(drop=True)
                        st.session_state.current_recommendation_set = shuffled
                        st.rerun()
            
            # DOWNLOAD CURRENT SET
            st.divider()
            if st.button("💾 Save Current Recommendation Set", use_container_width=True):
                st.session_state.previous_recommendations.append({
                    'set': recommendations.copy(),
                    'criteria': criteria.copy(),
                    'timestamp': datetime.now()
                })
                st.success(f"✅ Set #{len(st.session_state.previous_recommendations)} saved!")
        
        elif st.session_state.current_recommendation_set is not None and len(st.session_state.current_recommendation_set) == 0:
            st.error("❌ No items match your criteria with current variation settings.")
            st.markdown("""
            **Try:**
            - Lower the variation level
            - Increase budget
            - Relax dietary restrictions
            - Click 'Get Alternative Set' for completely different options
            """)