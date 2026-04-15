# menu_planner_csv.py
# Enhanced Streamlit app with calorie tracking, beverages, and intelligent recommendations

import streamlit as st
import pandas as pd
import io
from datetime import datetime

# ======================
# 1. CONSTANTS & DEFAULTS
# ======================

# Calorie guidelines for different occasions (per person)
CALORIE_GUIDELINES = {
    'casual': {'min': 400, 'max': 700, 'description': 'Light meal'},
    'business': {'min': 500, 'max': 800, 'description': 'Moderate meal'},
    'birthday': {'min': 600, 'max': 1000, 'description': 'Celebration meal'},
    'wedding': {'min': 700, 'max': 1200, 'description': 'Festive feast'},
    'family': {'min': 600, 'max': 900, 'description': 'Family gathering'},
    'festival': {'min': 700, 'max': 1100, 'description': 'Festival special'},
    'dashain': {'min': 800, 'max': 1300, 'description': 'Dashain feast'},
    'tihar': {'min': 750, 'max': 1200, 'description': 'Tihar celebration'},
    'healthy': {'min': 300, 'max': 600, 'description': 'Healthy option'}
}

# Beverage categories
BEVERAGE_CATEGORIES = ['soft drink', 'hot beverage', 'cold beverage', 'alcoholic', 'juice']

# ======================
# 2. SESSION STATE INIT
# ======================

if 'current_menu' not in st.session_state:
    st.session_state.current_menu = None
if 'menu_uploaded' not in st.session_state:
    st.session_state.menu_uploaded = False
if 'menu_filename' not in st.session_state:
    st.session_state.menu_filename = None

# ======================
# 3. CSV VALIDATION & PROCESSING
# ======================

def validate_menu_csv(df):
    """Check if uploaded CSV has required columns"""
    required_columns = ['name', 'price']
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    # Check price column is numeric
    try:
        df['price'] = pd.to_numeric(df['price'])
    except:
        return False, "Price column must contain numbers"
    
    # Check calories if column exists
    if 'calories' in df.columns:
        try:
            df['calories'] = pd.to_numeric(df['calories'], errors='coerce').fillna(0)
        except:
            return False, "Calories column must contain numbers"
    
    # Add default values for optional columns if missing
    optional_columns = {
        'category': 'main',
        'allergens': 'none',
        'dietary': 'regular',
        'tags': '',
        'calories': 0,
        'beverage_type': 'none'
    }
    
    for col, default_value in optional_columns.items():
        if col not in df.columns:
            df[col] = default_value
    
    return True, "CSV validated successfully"

def process_uploaded_csv(uploaded_file):
    """Process the uploaded CSV file"""
    try:
        df = pd.read_csv(uploaded_file)
        is_valid, message = validate_menu_csv(df)
        
        if not is_valid:
            return None, message
        
        df = df.fillna('')
        df['name'] = df['name'].astype(str).str.strip()
        
        return df, "File processed successfully!"
        
    except Exception as e:
        return None, f"Error processing file: {str(e)}"

# ======================
# 4. ENHANCED MATCHING ALGORITHM WITH CALORIES
# ======================

def get_recommendations(criteria, menu_df):
    """Generate intelligent recommendations based on criteria including calories"""
    if menu_df is None or len(menu_df) == 0:
        return pd.DataFrame()
    
    filtered = menu_df.copy()
    
    # 1. Budget filter
    if criteria['budget_per_person'] > 0:
        filtered = filtered[filtered['price'] <= criteria['budget_per_person']]
    
    # 2. Dietary restrictions
    if criteria['dietary'] != 'any':
        if criteria['dietary'] == 'vegetarian':
            filtered = filtered[filtered['dietary'].str.contains('vegetarian|vegan', case=False, na=False)]
        elif criteria['dietary'] == 'vegan':
            filtered = filtered[filtered['dietary'].str.contains('vegan', case=False, na=False)]
        elif criteria['dietary'] == 'pescatarian':
            filtered = filtered[filtered['dietary'].str.contains('pescatarian|fish', case=False, na=False)]
        elif criteria['dietary'] == 'gluten-free':
            filtered = filtered[~filtered['allergens'].str.contains('gluten', case=False, na=False)]
        elif criteria['dietary'] == 'non-vegetarian':
            filtered = filtered[filtered['dietary'].str.contains('regular|non-vegetarian', case=False, na=False)]
    
    # 3. Allergen avoidance
    if criteria['allergens']:
        for allergen in criteria['allergens']:
            filtered = filtered[~filtered['allergens'].str.contains(allergen, case=False, na=False)]
    
    # 4. Beverage preference filter
    if criteria['include_beverage'] != 'any':
        if criteria['include_beverage'] == 'none':
            filtered = filtered[~filtered['category'].str.contains('beverage|drink', case=False, na=False)]
        else:
            beverage_filtered = filtered[filtered['category'].str.contains('beverage|drink', case=False, na=False)]
            if 'beverage_type' in filtered.columns:
                beverage_filtered = beverage_filtered[beverage_filtered['beverage_type'] == criteria['include_beverage']]
            filtered = beverage_filtered if criteria['beverage_only'] else filtered
    
    # 5. Sort by smart scoring
    filtered = filtered.sort_values('price', ascending=True)
    
    # 6. Intelligent meal composition
    occasion = criteria['occasion']
    calorie_target = CALORIE_GUIDELINES.get(occasion, CALORIE_GUIDELINES['casual'])
    
    final_items = []
    remaining_budget = criteria['budget_per_person']
    total_calories = 0
    min_calories = calorie_target['min']
    max_calories = calorie_target['max']
    
    # Separate food and beverages
    food_items = filtered[~filtered['category'].str.contains('beverage|drink', case=False, na=False)]
    beverage_items = filtered[filtered['category'].str.contains('beverage|drink', case=False, na=False)]
    
    # Build balanced meal with calorie consideration
    categories_priority = ['starter', 'main', 'dessert', 'side']
    
    for category in categories_priority:
        if category in food_items['category'].unique():
            category_items = food_items[food_items['category'] == category].copy()
            
            # Score items based on multiple factors
            category_items['score'] = 0
            
            # Score by calories appropriateness
            if 'calories' in category_items.columns:
                # Ideal calorie range for this category
                if category == 'starter':
                    cat_cal_range = (100, 300)
                elif category == 'main':
                    cat_cal_range = (300, 700)
                elif category == 'dessert':
                    cat_cal_range = (150, 400)
                elif category == 'side':
                    cat_cal_range = (50, 200)
                else:
                    cat_cal_range = (100, 400)
                
                # Score items whose calories are within ideal range
                category_items['calorie_score'] = category_items['calories'].apply(
                    lambda x: 3 if cat_cal_range[0] <= x <= cat_cal_range[1] else 
                             2 if x < cat_cal_range[0] else 
                             1 if x <= cat_cal_range[1] + 100 else 0
                )
                category_items['score'] += category_items['calorie_score']
            
            # Score by price (cheaper is better within budget)
            category_items['price_score'] = (1 - (category_items['price'] / remaining_budget)).clip(0, 1) * 2
            category_items['score'] += category_items['price_score']
            
            # Sort by score
            category_items = category_items.sort_values('score', ascending=False)
            
            for _, item in category_items.iterrows():
                if item['name'] not in [i['name'] for i in final_items]:
                    item_calories = item.get('calories', 0)
                    
                    # Check if adding this item keeps us within calorie and budget limits
                    if (total_calories + item_calories <= max_calories and 
                        item['price'] <= remaining_budget):
                        
                        # For main courses, ensure minimum calories
                        if category == 'main' and total_calories + item_calories < min_calories * 0.4:
                            continue
                            
                        final_items.append(item)
                        total_calories += item_calories
                        remaining_budget -= item['price']
                        break
    
    # Add beverages if requested and budget allows
    if criteria['include_beverage'] != 'none' and len(beverage_items) > 0:
        beverage_items = beverage_items.sort_values('price', ascending=True)
        for _, beverage in beverage_items.iterrows():
            if beverage['price'] <= remaining_budget:
                final_items.append(beverage)
                total_calories += beverage.get('calories', 0)
                remaining_budget -= beverage['price']
                break
    
    # Ensure minimum calorie requirement
    if total_calories < min_calories and len(food_items) > 0:
        # Add additional side or starter
        additional_items = food_items[~food_items['name'].isin([i['name'] for i in final_items])]
        additional_items = additional_items.sort_values('price', ascending=True)
        
        for _, item in additional_items.iterrows():
            if (item['price'] <= remaining_budget and 
                total_calories + item.get('calories', 0) <= max_calories):
                final_items.append(item)
                total_calories += item.get('calories', 0)
                remaining_budget -= item['price']
                break
    
    return pd.DataFrame(final_items), total_calories

# ======================
# 5. STREAMLIT UI
# ======================

st.set_page_config(
    page_title="Smart Menu Planner - Calories & Beverages",
    page_icon="🥗",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #003893;
        text-align: center;
        margin-bottom: 1rem;
    }
    .calorie-info {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .beverage-card {
        background-color: #f0f8ff;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🥗 Smart Menu Planner with Calorie Tracking</h1>', unsafe_allow_html=True)
st.markdown("Upload your menu CSV with calorie information and get intelligent recommendations!")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📤 Upload Menu", "⚙️ Set Criteria", "📋 Get Recommendations"])

# TAB 1: UPLOAD MENU
with tab1:
    st.header("📤 Upload Your Menu CSV")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a CSV file with your menu (include calories column)",
            type=['csv'],
            help="CSV should have: name, price, category, calories (optional), allergens, dietary, tags, beverage_type"
        )
        
        if uploaded_file is not None:
            with st.spinner("Processing your menu file..."):
                processed_df, message = process_uploaded_csv(uploaded_file)
                
                if processed_df is not None:
                    st.session_state.current_menu = processed_df
                    st.session_state.menu_uploaded = True
                    st.session_state.menu_filename = uploaded_file.name
                    st.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        else:
            if not st.session_state.menu_uploaded:
                st.warning("⚠️ Please upload a CSV file to continue")
    
    with col2:
        st.subheader("CSV Format Guide")
        
        with st.expander("Enhanced CSV Format", expanded=True):
            st.markdown("""
            **Required columns:**
            - `name`: Item name
            - `price`: Price in रू
            
            **Recommended columns:**
            - `calories`: Approx calories per serving
            - `category`: starter/main/dessert/side/beverage
            - `beverage_type`: soft drink/hot beverage/cold beverage/juice/alcoholic
            - `allergens`: comma-separated
            - `dietary`: vegetarian/vegan/non-vegetarian
            - `tags`: descriptive tags
            """)
        
        # Enhanced template with calories and beverages
        enhanced_template = pd.DataFrame([
            {"name": "Momo", "price": 150, "category": "starter", "calories": 250, 
             "allergens": "none", "dietary": "non-vegetarian", "tags": "dumpling,spicy", "beverage_type": "none"},
            {"name": "Dal Bhat", "price": 300, "category": "main", "calories": 450, 
             "allergens": "none", "dietary": "vegetarian", "tags": "traditional,rice", "beverage_type": "none"},
            {"name": "Coca Cola", "price": 80, "category": "beverage", "calories": 140, 
             "allergens": "none", "dietary": "vegan", "tags": "soft-drink,cold", "beverage_type": "soft drink"},
            {"name": "Masala Tea", "price": 60, "category": "beverage", "calories": 80, 
             "allergens": "dairy", "dietary": "vegetarian", "tags": "hot,spicy", "beverage_type": "hot beverage"},
            {"name": "Sel Roti", "price": 50, "category": "dessert", "calories": 180, 
             "allergens": "gluten", "dietary": "vegetarian", "tags": "sweet,festive", "beverage_type": "none"},
        ])
        
        template_csv = enhanced_template.to_csv(index=False)
        st.download_button(
            label="📥 Download Enhanced Template",
            data=template_csv,
            file_name="enhanced_menu_template.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Display menu stats if uploaded
    if st.session_state.menu_uploaded and st.session_state.current_menu is not None:
        st.divider()
        st.subheader(f"📋 Menu Analysis: {st.session_state.menu_filename}")
        
        menu_df = st.session_state.current_menu
        
        # Calculate statistics
        col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
        
        with col_stats1:
            st.metric("Total Items", len(menu_df))
        
        with col_stats2:
            avg_price = menu_df['price'].mean()
            st.metric("Avg Price", f"रू {avg_price:,.0f}")
        
        with col_stats3:
            if 'calories' in menu_df.columns and menu_df['calories'].sum() > 0:
                avg_calories = menu_df[menu_df['calories'] > 0]['calories'].mean()
                st.metric("Avg Calories", f"{avg_calories:.0f} kcal")
            else:
                st.metric("Calories Data", "Not Available")
        
        with col_stats4:
            beverage_count = len(menu_df[menu_df['category'].str.contains('beverage|drink', case=False, na=False)])
            st.metric("Beverages", beverage_count)
        
        # Show data preview
        with st.expander("📊 View Menu Data"):
            display_df = menu_df.copy()
            if 'price' in display_df.columns:
                display_df['price'] = display_df['price'].apply(lambda x: f"रू {x:,.0f}")
            if 'calories' in display_df.columns:
                display_df['calories'] = display_df['calories'].apply(lambda x: f"{x:.0f} kcal" if x > 0 else "N/A")
            
            st.dataframe(display_df, use_container_width=True, height=300)

# TAB 2: SET CRITERIA
with tab2:
    if not st.session_state.menu_uploaded:
        st.warning("⚠️ Please upload a menu CSV file first.")
        st.info("Go to the first tab to upload your menu file.")
    else:
        st.header("⚙️ Set Your Event Criteria")
        
        # Main criteria columns
        col1, col2 = st.columns(2)
        
        with col1:
            # Basic criteria
            num_people = st.number_input(
                "👥 Number of Guests",
                min_value=1,
                max_value=500,
                value=4,
                key="num_people"
            )
            
            budget_per_person = st.slider(
                "💰 Budget per Person (रू)",
                min_value=0,
                max_value=10000,
                value=1000,
                step=100,
                key="budget_per_person"
            )
            
            total_budget = num_people * budget_per_person
            st.info(f"**Total Event Budget:** रू {total_budget:,.0f}")
            
            # Occasion with calorie info
            occasion = st.selectbox(
                "🎉 Event Type",
                list(CALORIE_GUIDELINES.keys()),
                key="occasion",
                help="Select event type for calorie recommendations"
            )
            
            # Show calorie guideline for selected occasion
            if occasion in CALORIE_GUIDELINES:
                calorie_info = CALORIE_GUIDELINES[occasion]
                st.markdown(f"""
                <div class="calorie-info">
                <strong>Calorie Guideline for {occasion}:</strong><br>
                {calorie_info['description']}<br>
                <em>Recommended: {calorie_info['min']} - {calorie_info['max']} calories per person</em>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Dietary and preferences
            dietary = st.selectbox(
                "🥦 Dietary Preference",
                ["any", "vegetarian", "vegan", "pescatarian", "non-vegetarian", "gluten-free"],
                key="dietary"
            )
            
            # Allergens
            if st.session_state.menu_uploaded:
                all_allergens = set()
                if 'allergens' in st.session_state.current_menu.columns:
                    for allergens_str in st.session_state.current_menu['allergens']:
                        if isinstance(allergens_str, str):
                            items = [a.strip().lower() for a in allergens_str.split(',')]
                            all_allergens.update(items)
                all_allergens = [a for a in all_allergens if a and a != 'none']
            
            allergens = st.multiselect(
                "🚫 Allergens to Avoid",
                sorted(list(all_allergens)) if st.session_state.menu_uploaded else ["nuts", "dairy", "gluten", "seafood"],
                key="allergens"
            )
            
            # Beverage preferences
            st.subheader("🥤 Beverage Preferences")
            
            include_beverage = st.selectbox(
                "Include Beverage?",
                ["any", "soft drink", "hot beverage", "cold beverage", "juice", "alcoholic", "none"],
                key="include_beverage"
            )
            
            beverage_only = st.checkbox(
                "Show beverages only",
                value=False,
                key="beverage_only",
                help="Check to see only beverage recommendations"
            )
            
            # Calorie adjustment
            st.subheader("⚖️ Calorie Adjustment")
            calorie_adjustment = st.slider(
                "Calorie preference",
                min_value=-300,
                max_value=300,
                value=0,
                step=50,
                help="Adjust calorie target (-300 for lighter, +300 for heartier)"
            )
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            col_adv1, col_adv2 = st.columns(2)
            
            with col_adv1:
                max_items = st.slider("Max items per person", 1, 8, 4)
                prioritize_low_cal = st.checkbox("Prioritize lower calorie options", value=False)
            
            with col_adv2:
                include_dessert = st.checkbox("Include dessert", value=True)
                force_beverage = st.checkbox("Always include beverage", value=False)
        
        # Compatibility analysis
        st.divider()
        st.subheader("📊 Menu Compatibility Analysis")
        
        menu_df = st.session_state.current_menu
        compat_cols = st.columns(5)
        
        with compat_cols[0]:
            total_items = len(menu_df)
            st.metric("Total Items", total_items)
        
        with compat_cols[1]:
            if budget_per_person > 0:
                budget_match = len(menu_df[menu_df['price'] <= budget_per_person])
                st.metric("Within Budget", budget_match)
        
        with compat_cols[2]:
            if 'calories' in menu_df.columns:
                items_with_calories = len(menu_df[menu_df['calories'] > 0])
                st.metric("With Calories", items_with_calories)
        
        with compat_cols[3]:
            beverage_count = len(menu_df[menu_df['category'].str.contains('beverage|drink', case=False, na=False)])
            st.metric("Beverages", beverage_count)
        
        with compat_cols[4]:
            calorie_info = CALORIE_GUIDELINES.get(occasion, CALORIE_GUIDELINES['casual'])
            st.metric("Calorie Target", f"{calorie_info['min']}-{calorie_info['max']}")

# TAB 3: GET RECOMMENDATIONS
with tab3:
    st.header("📋 Get Intelligent Recommendations")
    
    if not st.session_state.menu_uploaded:
        st.warning("⚠️ Please upload a menu CSV file first.")
    elif st.session_state.current_menu is None:
        st.error("❌ No menu data available.")
    else:
        # Prepare enhanced criteria
        criteria = {
            'num_people': st.session_state.get('num_people', 4),
            'budget_per_person': st.session_state.get('budget_per_person', 1000),
            'dietary': st.session_state.get('dietary', 'any'),
            'allergens': st.session_state.get('allergens', []),
            'occasion': st.session_state.get('occasion', 'casual'),
            'include_beverage': st.session_state.get('include_beverage', 'any'),
            'beverage_only': st.session_state.get('beverage_only', False)
        }
        
        if st.button("🧠 Generate Intelligent Recommendations", type="primary", use_container_width=True):
            with st.spinner("Analyzing menu with calorie intelligence..."):
                recommendations, total_calories = get_recommendations(criteria, st.session_state.current_menu)
            
            if len(recommendations) > 0:
                st.success(f"✅ Found {len(recommendations)} perfectly balanced recommendations!")
                
                # Get calorie guidelines
                calorie_target = CALORIE_GUIDELINES.get(criteria['occasion'], CALORIE_GUIDELINES['casual'])
                
                # Display calorie summary
                col_cal1, col_cal2, col_cal3 = st.columns(3)
                
                with col_cal1:
                    st.metric("Total Calories", f"{total_calories:.0f} kcal")
                
                with col_cal2:
                    target_min = calorie_target['min']
                    target_max = calorie_target['max']
                    calorie_status = "🟢 Perfect" if target_min <= total_calories <= target_max else \
                                    "🟡 Light" if total_calories < target_min else "🔴 Heavy"
                    st.metric("Calorie Status", calorie_status)
                
                with col_cal3:
                    if total_calories > 0:
                        calorie_pct = (total_calories / target_max) * 100
                        st.metric("Target Usage", f"{calorie_pct:.0f}%")
                
                # Display each recommendation with enhanced info
                total_cost_per_person = recommendations['price'].sum()
                total_event_cost = total_cost_per_person * criteria['num_people']
                
                st.subheader("🍽️ Recommended Meal Plan")
                
                for idx, (_, item) in enumerate(recommendations.iterrows(), 1):
                    with st.container():
                        cols = st.columns([3, 1, 1, 1])
                        
                        with cols[0]:
                            # Item details with emoji based on category
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
                            
                            if 'tags' in item and pd.notna(item['tags']):
                                st.caption(f"Tags: {item['tags']}")
                        
                        with cols[1]:
                            # Price
                            price = item['price']
                            st.metric("Price", f"रू {price:,.0f}")
                        
                        with cols[2]:
                            # Calories
                            calories = item.get('calories', 0)
                            if calories > 0:
                                st.metric("Calories", f"{calories:.0f} kcal")
                                # Visual indicator
                                if calories < 200:
                                    st.caption("Light")
                                elif calories < 400:
                                    st.caption("Moderate")
                                else:
                                    st.caption("Heavy")
                        
                        with cols[3]:
                            # Budget usage
                            if criteria['budget_per_person'] > 0:
                                budget_pct = (price / criteria['budget_per_person']) * 100
                                st.progress(min(budget_pct / 100, 1.0))
                                st.caption(f"{budget_pct:.0f}% of budget")
                        
                        # Allergen warning
                        if 'allergens' in item and pd.notna(item['allergens']) and item['allergens'] not in ['none', '']:
                            st.warning(f"⚠️ Contains: {item['allergens']}")
                        
                        st.divider()
                
                # SUMMARY SECTION
                st.subheader("📈 Comprehensive Summary")
                
                summary_cols = st.columns(4)
                with summary_cols[0]:
                    st.metric("Items per Person", len(recommendations))
                    food_items = len(recommendations[~recommendations['category'].str.contains('beverage|drink', case=False, na=False)])
                    beverage_items = len(recommendations) - food_items
                    st.caption(f"({food_items} food, {beverage_items} beverage)")
                
                with summary_cols[1]:
                    st.metric("Cost per Person", f"रू {total_cost_per_person:,.0f}")
                    budget_used = (total_cost_per_person / criteria['budget_per_person']) * 100
                    st.caption(f"{budget_used:.0f}% of budget")
                
                with summary_cols[2]:
                    st.metric("Total Event Cost", f"रू {total_event_cost:,.0f}")
                
                with summary_cols[3]:
                    st.metric("Calories per Person", f"{total_calories:.0f} kcal")
                    if total_calories > 0:
                        calorie_status = "✅ Good" if calorie_target['min'] <= total_calories <= calorie_target['max'] else \
                                        "⚠️ Adjust" if total_calories < calorie_target['min'] else "⚠️ High"
                        st.caption(calorie_status)
                
                # MEAL COMPOSITION ANALYSIS
                st.subheader("🥗 Meal Composition")
                
                if 'category' in recommendations.columns:
                    # Group by category
                    categories = recommendations['category'].unique()
                    
                    for category in categories:
                        category_items = recommendations[recommendations['category'] == category]
                        if len(category_items) > 0:
                            with st.expander(f"{category.title()}s ({len(category_items)} items)"):
                                for _, item in category_items.iterrows():
                                    calories_info = f" ({item.get('calories', 0):.0f} kcal)" if item.get('calories', 0) > 0 else ""
                                    st.markdown(f"- **{item['name']}** - रू {item['price']:,.0f}{calories_info}")
                
                # NUTRITIONAL BREAKDOWN
                if 'calories' in recommendations.columns and recommendations['calories'].sum() > 0:
                    st.subheader("⚖️ Nutritional Breakdown")
                    
                    # Calculate calories by category
                    if 'category' in recommendations.columns:
                        calorie_by_category = recommendations.groupby('category')['calories'].sum()
                        
                        col_nut1, col_nut2 = st.columns(2)
                        
                        with col_nut1:
                            st.markdown("**Calories by Category:**")
                            for category, cal in calorie_by_category.items():
                                if cal > 0:
                                    cal_pct = (cal / total_calories) * 100
                                    st.markdown(f"- {category.title()}: {cal:.0f} kcal ({cal_pct:.0f}%)")
                        
                        with col_nut2:
                            # Pie chart visualization
                            import matplotlib.pyplot as plt
                            
                            if len(calorie_by_category) > 0:
                                fig, ax = plt.subplots(figsize=(3, 3))
                                categories = calorie_by_category.index.tolist()
                                calories = calorie_by_category.values.tolist()
                                
                                # Filter out zero values
                                valid_data = [(cat, cal) for cat, cal in zip(categories, calories) if cal > 0]
                                if valid_data:
                                    cats, cals = zip(*valid_data)
                                    ax.pie(cals, labels=cats, autopct='%1.0f%%', startangle=90)
                                    ax.axis('equal')
                                    st.pyplot(fig)
                
                # DOWNLOAD OPTIONS
                st.divider()
                st.subheader("📥 Download Options")
                
                col_d1, col_d2, col_d3 = st.columns(3)
                
                with col_d1:
                    # Basic recommendations
                    rec_csv = recommendations.to_csv(index=False)
                    st.download_button(
                        label="Download Recommendations",
                        data=rec_csv,
                        file_name=f"recommendations_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col_d2:
                    # Event plan with quantities
                    event_plan = recommendations.copy()
                    event_plan['quantity'] = criteria['num_people']
                    event_plan['total_cost'] = event_plan['price'] * event_plan['quantity']
                    
                    event_csv = event_plan.to_csv(index=False)
                    st.download_button(
                        label="Download Event Plan",
                        data=event_csv,
                        file_name=f"event_plan_{criteria['num_people']}_guests.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col_d3:
                    # Nutritional summary
                    if 'calories' in recommendations.columns:
                        nutrition_summary = recommendations[['name', 'category', 'calories', 'price']].copy()
                        nutrition_summary['calories_pct'] = (nutrition_summary['calories'] / total_calories * 100).round(1)
                        nutrition_csv = nutrition_summary.to_csv(index=False)
                        st.download_button(
                            label="Download Nutrition Summary",
                            data=nutrition_csv,
                            file_name="nutrition_summary.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                
                # TIPS AND SUGGESTIONS
                st.markdown("---")
                st.subheader("💡 Tips & Suggestions")
                
                if total_calories < calorie_target['min']:
                    st.info("**Consider adding:** A side dish or larger portion to meet calorie needs")
                elif total_calories > calorie_target['max']:
                    st.warning("**Consider reducing:** Opt for lighter options or smaller portions")
                else:
                    st.success("**Perfect balance!** Your meal plan meets the calorie target for this occasion.")
                
                # Beverage suggestion
                beverage_included = len(recommendations[recommendations['category'].str.contains('beverage|drink', case=False, na=False)]) > 0
                if not beverage_included and criteria['include_beverage'] != 'none':
                    st.info("**Beverage suggestion:** Consider adding a beverage to complete the meal")
            
            else:
                st.error("❌ No items match all your criteria. Try:")
                st.markdown("""
                - Increase your budget per person
                - Relax dietary restrictions
                - Adjust beverage preferences
                - Check allergen restrictions
                """)

# SIDEBAR
with st.sidebar:
    st.title("🥗 Smart Menu Planner")
    st.markdown("**with Calorie Tracking**")
    st.markdown("---")
    
    # Current status
    st.subheader("Current Status")
    
    if st.session_state.menu_uploaded and st.session_state.current_menu is not None:
        st.success("✅ Menu Loaded")
        st.write(f"**File:** {st.session_state.menu_filename}")
        st.write(f"**Items:** {len(st.session_state.current_menu)}")
        
        # Enhanced stats
        menu_df = st.session_state.current_menu
        if 'calories' in menu_df.columns:
            items_with_cal = len(menu_df[menu_df['calories'] > 0])
            st.write(f"**With Calories:** {items_with_cal}")
        
        beverage_count = len(menu_df[menu_df['category'].str.contains('beverage|drink', case=False, na=False)])
        st.write(f"**Beverages:** {beverage_count}")
    else:
        st.warning("⚠️ No Menu Loaded")
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("Quick Actions")
    
    if st.button("🔄 Clear & Start Over", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    st.markdown("---")
    
    # Calorie guide
    st.subheader("⚖️ Calorie Guidelines")
    
    with st.expander("View All Guidelines"):
        for occasion, info in CALORIE_GUIDELINES.items():
            st.write(f"**{occasion.title()}:** {info['min']}-{info['max']} kcal")
            st.caption(info['description'])
            st.divider()
    
    st.markdown("---")
    
    # Beverage guide
    st.subheader("🥤 Beverage Types")
    
    for beverage in BEVERAGE_CATEGORIES:
        with st.expander(beverage.title()):
            if beverage == 'soft drink':
                st.write("Coca Cola, Sprite, Fanta")
                st.caption("~140-150 calories per 330ml")
            elif beverage == 'hot beverage':
                st.write("Tea, Coffee, Hot Chocolate")
                st.caption("~50-200 calories per cup")
            elif beverage == 'cold beverage':
                st.write("Iced Tea, Cold Coffee, Smoothies")
                st.caption("~100-300 calories per serving")
            elif beverage == 'juice':
                st.write("Orange, Apple, Mango Juice")
                st.caption("~110-150 calories per glass")
            elif beverage == 'alcoholic':
                st.write("Beer, Wine, Spirits")
                st.caption("~100-200 calories per drink")
    
    st.markdown("---")
    
    # Project info
    st.subheader("About This Project")
    st.markdown("""
    **Enhanced Features:**
    - Calorie tracking & intelligent meal planning
    - Beverage category support
    - Occasion-based calorie targets
    - Nutritional balance analysis
    - Smart filtering with multiple criteria
    
    **CSV Columns:**
    - Required: name, price
    - Recommended: calories, category, beverage_type
    - Optional: allergens, dietary, tags
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #003893;'>🥗 Smart Menu Planner with Calorie Intelligence | Nepali Rupees | School Project</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: small;'>Upload menu CSV with calorie data for intelligent recommendations</p>", unsafe_allow_html=True)