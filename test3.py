# menu_planner_csv.py
# Streamlit app that reads user-uploaded CSV menu files - Nepali Rupees Version

import streamlit as st
import pandas as pd
import io
from datetime import datetime

# ======================
# 1. NO DEFAULT MENU - User MUST upload CSV
# ======================

# Initialize empty menu in session state
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = None
if 'menu_uploaded' not in st.session_state:
    st.session_state.menu_uploaded = False
if 'menu_filename' not in st.session_state:
    st.session_state.menu_filename = None

# ======================
# 2. CSV VALIDATION & PROCESSING
# ======================

def validate_menu_csv(df):
    """Check if uploaded CSV has required columns"""
    required_columns = ['name', 'price']
    
    # Check for required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    # Check price column is numeric
    try:
        df['price'] = pd.to_numeric(df['price'])
    except:
        return False, "Price column must contain numbers"
    
    # Add default values for optional columns if missing
    optional_columns = {
        'category': 'main',
        'allergens': 'none',
        'dietary': 'regular',
        'tags': ''
    }
    
    for col, default_value in optional_columns.items():
        if col not in df.columns:
            df[col] = default_value
    
    return True, "CSV validated successfully"

def process_uploaded_csv(uploaded_file):
    """Process the uploaded CSV file"""
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        
        # Validate
        is_valid, message = validate_menu_csv(df)
        
        if not is_valid:
            return None, message
        
        # Clean data
        df = df.fillna('')
        df['name'] = df['name'].astype(str).str.strip()
        
        return df, "File processed successfully!"
        
    except Exception as e:
        return None, f"Error processing file: {str(e)}"

# ======================
# 3. MATCHING ALGORITHM
# ======================

def get_recommendations(criteria, menu_df):
    """Generate recommendations based on user criteria"""
    if menu_df is None or len(menu_df) == 0:
        return pd.DataFrame()
    
    filtered = menu_df.copy()
    
    # 1. Budget filter (in Nepali Rupees)
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
    
    # 4. Sort by price (cheapest first within budget)
    filtered = filtered.sort_values('price', ascending=True)
    
    # 5. Create balanced meal plan
    final_items = []
    remaining_budget = criteria['budget_per_person']
    
    # Try to get one from each category if available
    if 'category' in filtered.columns:
        categories = filtered['category'].unique()
        for category in categories[:3]:  # Limit to first 3 categories
            category_items = filtered[filtered['category'] == category]
            if len(category_items) > 0:
                cheapest_in_category = category_items.iloc[0]
                if cheapest_in_category['price'] <= remaining_budget:
                    final_items.append(cheapest_in_category)
                    remaining_budget -= cheapest_in_category['price']
    
    # Add more items if budget allows
    for _, item in filtered.iterrows():
        if item['name'] not in [i['name'] for i in final_items]:
            if item['price'] <= remaining_budget:
                final_items.append(item)
                remaining_budget -= item['price']
    
    return pd.DataFrame(final_items)

# ======================
# 4. STREAMLIT UI
# ======================

st.set_page_config(
    page_title="CSV Menu Planner - Nepali Rupees",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for Nepali theme
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #003893;
        text-align: center;
        margin-bottom: 1rem;
    }
    .nepali-flag {
        color: #DC143C;
    }
    .rupee-symbol {
        color: #003893;
        font-weight: bold;
    }
    .nepali-theme {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title with Nepali theme
st.markdown('<h1 class="main-header">📊 Menu Planner <span class="nepali-flag">(Nepali Rupees)</span></h1>', unsafe_allow_html=True)
st.markdown("Upload your menu as a CSV file and get personalized recommendations in Nepali Rupees!")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📤 Upload Menu", "⚙️ Set Criteria", "📋 Get Recommendations"])

# TAB 1: UPLOAD MENU (REQUIRED)
with tab1:
    st.header("📤 Upload Your Menu CSV")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload CSV File")
        
        uploaded_file = st.file_uploader(
            "Choose a CSV file with your menu",
            type=['csv'],
            help="Upload a CSV file with columns: name, price, category, allergens, dietary, tags"
        )
        
        if uploaded_file is not None:
            # Process the uploaded file
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
        
        with st.expander("Required Format", expanded=True):
            st.markdown("""
            **Required columns:**
            - `name`: Item name (text)
            - `price`: Price per item in Nepali Rupees (number)
            
            **Optional columns:**
            - `category`: starter/main/dessert/etc
            - `allergens`: comma-separated allergens
            - `dietary`: vegetarian/vegan/pescatarian/regular
            - `tags`: descriptive tags
            
            **Example CSV (Nepali Rupees):**
            ```
            name,price,category,allergens,dietary,tags
            "Momo",150,starter,none,non-vegetarian,"dumpling,spicy"
            "Dal Bhat",300,main,none,vegetarian,"traditional,rice"
            "Sel Roti",50,dessert,gluten,vegetarian,"sweet,festive"
            ```
            """)
        
        # Download template with Nepali examples
        nepali_template = pd.DataFrame([
            {"name": "Momo", "price": 150, "category": "starter", "allergens": "none", "dietary": "non-vegetarian", "tags": "dumpling,spicy,starter"},
            {"name": "Dal Bhat", "price": 300, "category": "main", "allergens": "none", "dietary": "vegetarian", "tags": "traditional,rice,main"},
            {"name": "Sel Roti", "price": 50, "category": "dessert", "allergens": "gluten", "dietary": "vegetarian", "tags": "sweet,festive,dessert"},
            {"name": "Thukpa", "price": 200, "category": "main", "allergens": "none", "dietary": "non-vegetarian", "tags": "noodle,soup,hot"},
            {"name": "Yomari", "price": 80, "category": "dessert", "allergens": "gluten", "dietary": "vegetarian", "tags": "sweet,traditional,newari"},
        ])
        
        template_csv = nepali_template.to_csv(index=False)
        st.download_button(
            label="📥 Download Nepali Menu Template",
            data=template_csv,
            file_name="nepali_menu_template.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Display current menu if uploaded
    if st.session_state.menu_uploaded and st.session_state.current_menu is not None:
        st.divider()
        st.subheader(f"📋 Current Menu: {st.session_state.menu_filename}")
        
        col_a, col_b = st.columns([3, 1])
        
        with col_a:
            # Format prices with Rs. symbol
            display_df = st.session_state.current_menu.copy()
            if 'price' in display_df.columns:
                display_df['price'] = display_df['price'].apply(lambda x: f"रू {x:,.2f}")
            
            st.dataframe(
                display_df,
                use_container_width=True,
                height=300
            )
        
        with col_b:
            menu_stats = st.session_state.current_menu
            st.metric("Items", len(menu_stats))
            avg_price = menu_stats['price'].mean()
            st.metric("Avg Price", f"रू {avg_price:,.2f}")
            
            if 'category' in menu_stats.columns:
                categories = menu_stats['category'].nunique()
                st.metric("Categories", categories)
            
            min_price = menu_stats['price'].min()
            max_price = menu_stats['price'].max()
            st.metric("Price Range", f"रू {min_price:,.0f}-रू {max_price:,.0f}")

# TAB 2: SET CRITERIA (Only accessible if menu uploaded)
with tab2:
    if not st.session_state.menu_uploaded:
        st.warning("⚠️ Please upload a menu CSV file in the 'Upload Menu' tab first.")
        st.info("Go to the first tab to upload your menu file.")
    else:
        st.header("⚙️ Set Your Event Criteria")
        
        # Create input columns
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
            
            # NEPALI RUPEE BUDGET RANGE: 0 - 10,000
            budget_per_person = st.slider(
                f"💰 Budget per Person (रू)",
                min_value=0,
                max_value=10000,
                value=1000,
                step=100,
                key="budget_per_person",
                help="Set budget in Nepali Rupees (रुपैयाँ)"
            )
            
            # Display budget in Nepali format
            total_budget = num_people * budget_per_person
            st.info(f"**Total Event Budget:** रू {total_budget:,.2f}")
            
            # Budget visualization
            if len(st.session_state.current_menu) > 0:
                avg_price = st.session_state.current_menu['price'].mean()
                if avg_price > 0:
                    items_possible = int(budget_per_person / avg_price)
                    st.caption(f"Based on average price (रू {avg_price:,.2f}), you could get ~{items_possible} items per person")
        
        with col2:
            # Dietary and preferences
            dietary = st.selectbox(
                "🥦 Dietary Preference",
                ["any", "vegetarian", "vegan", "pescatarian", "non-vegetarian", "gluten-free"],
                key="dietary"
            )
            
            # Get unique allergens from current menu for smart suggestions
            all_allergens = set()
            if 'allergens' in st.session_state.current_menu.columns:
                for allergens_str in st.session_state.current_menu['allergens']:
                    if isinstance(allergens_str, str):
                        items = [a.strip().lower() for a in allergens_str.split(',')]
                        all_allergens.update(items)
            
            # Remove 'none' from allergens
            all_allergens = [a for a in all_allergens if a and a != 'none']
            
            allergens = st.multiselect(
                "🚫 Allergens to Avoid",
                sorted(list(all_allergens)) or ["nuts", "dairy", "gluten", "seafood"],
                key="allergens"
            )
            
            occasion = st.selectbox(
                "🎉 Event Type",
                ["casual", "wedding", "business", "birthday", "family", "festival", "dashain", "tihar"],
                key="occasion"
            )
            
            # Advanced options
            with st.expander("Advanced Options"):
                max_items_per_person = st.slider(
                    "Maximum items per person",
                    min_value=1,
                    max_value=10,
                    value=3
                )
                
                prioritize_cheapest = st.checkbox(
                    "Prioritize cheaper items",
                    value=True,
                    help="Select cheaper items first to maximize variety"
                )
        
        # Quick stats based on criteria
        st.divider()
        st.subheader("📊 Menu Compatibility")
        
        # Calculate how many items match basic criteria
        temp_filtered = st.session_state.current_menu.copy()
        
        # Apply budget filter
        if budget_per_person > 0:
            budget_match = len(temp_filtered[temp_filtered['price'] <= budget_per_person])
        else:
            budget_match = len(temp_filtered)
        
        # Apply dietary filter
        diet_match = len(temp_filtered)
        if dietary != 'any':
            if dietary == 'vegetarian':
                diet_match = len(temp_filtered[temp_filtered['dietary'].str.contains('vegetarian|vegan', case=False, na=False)])
            elif dietary == 'vegan':
                diet_match = len(temp_filtered[temp_filtered['dietary'].str.contains('vegan', case=False, na=False)])
            elif dietary == 'pescatarian':
                diet_match = len(temp_filtered[temp_filtered['dietary'].str.contains('pescatarian|fish', case=False, na=False)])
            elif dietary == 'non-vegetarian':
                diet_match = len(temp_filtered[temp_filtered['dietary'].str.contains('regular|non-vegetarian', case=False, na=False)])
            elif dietary == 'gluten-free':
                diet_match = len(temp_filtered[~temp_filtered['allergens'].str.contains('gluten', case=False, na=False)])
        
        # Display compatibility metrics
        compat_cols = st.columns(4)
        with compat_cols[0]:
            st.metric("Total Items", len(temp_filtered))
        with compat_cols[1]:
            st.metric("Within Budget", budget_match)
        with compat_cols[2]:
            st.metric("Diet Match", diet_match)
        with compat_cols[3]:
            min_match = min(budget_match, diet_match)
            st.metric("Likely Matches", min_match)

# TAB 3: GET RECOMMENDATIONS
with tab3:
    st.header("📋 Get Recommendations")
    
    # Check if we have a menu
    if not st.session_state.menu_uploaded:
        st.warning("⚠️ Please upload a menu CSV file first in the 'Upload Menu' tab.")
    elif st.session_state.current_menu is None or len(st.session_state.current_menu) == 0:
        st.error("❌ No menu data available. Please upload a valid CSV file.")
    else:
        # Prepare criteria
        criteria = {
            'num_people': st.session_state.get('num_people', 4),
            'budget_per_person': st.session_state.get('budget_per_person', 1000),
            'dietary': st.session_state.get('dietary', 'any'),
            'allergens': st.session_state.get('allergens', []),
            'occasion': st.session_state.get('occasion', 'casual')
        }
        
        # Generate button
        if st.button("🎯 Generate Recommendations", type="primary", use_container_width=True):
            with st.spinner("Analyzing menu and generating recommendations..."):
                recommendations = get_recommendations(criteria, st.session_state.current_menu)
            
            if len(recommendations) > 0:
                st.success(f"✅ Found {len(recommendations)} recommendations for your event!")
                
                # Display recommendations
                total_cost_per_person = recommendations['price'].sum()
                total_event_cost = total_cost_per_person * criteria['num_people']
                
                # Show each recommendation
                for idx, (_, item) in enumerate(recommendations.iterrows(), 1):
                    with st.container():
                        cols = st.columns([3, 1, 1])
                        
                        with cols[0]:
                            # Item details
                            st.markdown(f"### {idx}. {item['name']}")
                            
                            # Show category if available
                            if 'category' in item and pd.notna(item['category']):
                                st.markdown(f"**Category:** {item['category'].title()}")
                            
                            # Show dietary if available
                            if 'dietary' in item and pd.notna(item['dietary']):
                                st.markdown(f"**Dietary:** {item['dietary'].title()}")
                            
                            # Show tags if available
                            if 'tags' in item and pd.notna(item['tags']):
                                st.caption(f"Tags: {item['tags']}")
                        
                        with cols[1]:
                            # Price in Nepali Rupees
                            price = item['price']
                            st.metric("Price", f"रू {price:,.2f}")
                            st.caption(f"रू {price * criteria['num_people']:,.0f} total")
                        
                        with cols[2]:
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
                st.subheader("💰 Cost Summary")
                
                summary_cols = st.columns(4)
                with summary_cols[0]:
                    st.metric("Items per Person", len(recommendations))
                with summary_cols[1]:
                    st.metric("Cost per Person", f"रू {total_cost_per_person:,.2f}")
                with summary_cols[2]:
                    st.metric("Total Event Cost", f"रू {total_event_cost:,.2f}")
                with summary_cols[3]:
                    if criteria['budget_per_person'] > 0:
                        budget_used = (total_cost_per_person / criteria['budget_per_person']) * 100
                        st.metric("Budget Used", f"{budget_used:.1f}%")
                
                # MEAL PLAN BREAKDOWN
                st.subheader("🍽️ Meal Plan Structure")
                
                if 'category' in recommendations.columns:
                    # Group by category
                    categories = recommendations['category'].unique()
                    
                    for category in categories:
                        category_items = recommendations[recommendations['category'] == category]
                        if len(category_items) > 0:
                            st.markdown(f"**{category.title()}s:**")
                            for _, item in category_items.iterrows():
                                st.markdown(f"- {item['name']} (रू {item['price']:,.2f})")
                else:
                    # No categories, just list items
                    st.markdown("**Selected Items:**")
                    for _, item in recommendations.iterrows():
                        st.markdown(f"- {item['name']} (रू {item['price']:,.2f})")
                
                # DOWNLOAD OPTIONS
                st.divider()
                st.subheader("📥 Download Options")
                
                col_d1, col_d2 = st.columns(2)
                
                with col_d1:
                    # Download recommendations
                    rec_csv = recommendations.to_csv(index=False)
                    st.download_button(
                        label="Download Recommendations (CSV)",
                        data=rec_csv,
                        file_name=f"menu_recommendations_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col_d2:
                    # Download full event plan
                    event_plan = recommendations.copy()
                    event_plan['quantity'] = criteria['num_people']
                    event_plan['total_cost'] = event_plan['price'] * event_plan['quantity']
                    
                    event_csv = event_plan.to_csv(index=False)
                    st.download_button(
                        label="Download Event Plan (CSV)",
                        data=event_csv,
                        file_name=f"event_plan_{criteria['num_people']}_guests.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                # SHARE RESULTS
                st.markdown("---")
                st.caption(f"*Generated for {criteria['num_people']} guests with रू {criteria['budget_per_person']:,.0f} per person budget*")
            
            else:
                st.error("❌ No items match all your criteria. Try:")
                st.markdown("""
                - Increase your budget per person
                - Relax dietary restrictions
                - Remove some allergen restrictions
                - Upload a menu with more options
                """)
                
                # Show what's available
                with st.expander("View available items that match some criteria"):
                    # Show items within budget
                    in_budget = st.session_state.current_menu[
                        st.session_state.current_menu['price'] <= criteria['budget_per_person']
                    ]
                    if len(in_budget) > 0:
                        st.write(f"**Items within budget (रू {criteria['budget_per_person']:,.0f}):**")
                        # Format for display
                        display_df = in_budget[['name', 'price', 'dietary']].copy()
                        display_df['price'] = display_df['price'].apply(lambda x: f"रू {x:,.2f}")
                        st.dataframe(display_df.head(10))

# SIDEBAR
with st.sidebar:
    st.title("📊 CSV Menu Planner")
    st.markdown("**Nepali Rupees Version**")
    st.markdown("---")
    
    # Current status
    st.subheader("Current Status")
    
    if st.session_state.menu_uploaded and st.session_state.current_menu is not None:
        st.success("✅ Menu Loaded")
        st.write(f"**File:** {st.session_state.menu_filename}")
        st.write(f"**Items:** {len(st.session_state.current_menu)}")
        
        # Quick stats
        menu_df = st.session_state.current_menu
        min_price = menu_df['price'].min()
        max_price = menu_df['price'].max()
        st.write(f"**Price Range:** रू {min_price:,.0f} - रू {max_price:,.0f}")
    else:
        st.warning("⚠️ No Menu Loaded")
        st.write("Please upload a CSV file")
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("Quick Actions")
    
    if st.button("🔄 Clear & Upload New", use_container_width=True):
        st.session_state.current_menu = None
        st.session_state.menu_uploaded = False
        st.session_state.menu_filename = None
        st.rerun()
    
    st.markdown("---")
    
    # Nepali currency info
    st.subheader("💰 Nepali Pricing Guide")
    st.markdown("""
    **Typical Nepali Restaurant Prices:**
    - Street food/tea shop: रू 50 - रू 200
    - Local restaurant: रू 200 - रू 500
    - Hotel/restaurant: रू 500 - रू 1,500
    - Fine dining: रू 1,500 - रू 3,000+
    
    **Budget Suggestions:**
    - Casual meal: रू 300-500/person
    - Business lunch: रू 500-1,000/person
    - Wedding/buffet: रू 800-2,000/person
    - Festival meal: रू 200-500/person
    """)
    
    # Nepali festival notes
    with st.expander("🎊 Nepali Festival Events"):
        st.markdown("""
        **Dashain/Tihar Special:**
        - Traditional feasts
        - Meat dishes common
        - Sweets and desserts
        - Family gatherings
        
        **Typical Festival Foods:**
        - Masu (meat curry)
        - Sel Roti
        - Mutton dishes
        - Sweets (laddu, barfi)
        """)
    
    st.markdown("---")
    
    # Project info
    st.subheader("About This Project")
    st.markdown("""
    **School Project Features:**
    - CSV file upload and processing
    - Nepali Rupee currency support (रू)
    - Budget range: रू 0 - रू 10,000/person
    - Dietary restriction handling
    - Event-based recommendations
    
    **Required CSV columns:**
    1. `name` (required)
    2. `price` in Nepali Rupees (required)
    3. `category` (optional)
    4. `allergens` (optional)
    5. `dietary` (optional)
    6. `tags` (optional)
    """)

# Footer with Nepali theme
st.markdown("---")
st.markdown("<p style='text-align: center; color: #003893;'>📊 CSV Menu Planner | Nepali Rupees (रुपैयाँ) | School Project</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: small;'>Upload your menu CSV file (prices in रू) to get started</p>", unsafe_allow_html=True)