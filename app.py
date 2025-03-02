import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set page config for a wide layout and professional title
st.set_page_config(page_title="Assam Tourism Data Explorer", layout="wide")

# Custom CSS for professional styling
st.markdown(
    """
    <style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header text style */
    .header-title {
        font-size: 2.5rem;
        text-align: center;
        color: #003366;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    /* Subtitle styling */
    .header-subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #555;
        font-style: italic;
        margin-bottom: 2rem;
    }
    
    /* Card styling for content sections */
    .css-card {
        border-radius: 10px;
        padding: 20px;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    /* Make the filter section stand out */
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header with images using columns
col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    # Using local assets folder for images
    st.image("assets/india_flag.png", width=100)

with col2:
    st.markdown("<div class='header-title'>Assam Tourism Data Explorer</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-subtitle'>Discover the beauty and culture of Assam</div>", unsafe_allow_html=True)

with col3:
    # Using local assets folder for images
    st.image("assets/assam_state.png", width=100)

# Load the dataset
@st.cache_data
def load_data():
    try:
        data = pd.read_csv("Assam_TestData.csv")
        data = data.dropna(subset=["District", "Category"])
        return data
    except FileNotFoundError:
        # Create sample data for demonstration if file is not found
        sample_data = pd.DataFrame({
            'District': ['Guwahati', 'Kaziranga', 'Majuli', 'Tezpur', 'Sivasagar', 'Guwahati', 'Dibrugarh'],
            'Category': ['Temple', 'Wildlife', 'Culture', 'Heritage', 'Temple', 'Museum', 'River'],
            'Name': ['Kamakhya Temple', 'Kaziranga National Park', 'Majuli Island', 'Agnigarh Hill', 'Shiva Doul', 'Assam State Museum', 'Brahmaputra River'],
            'Description': ['Famous temple', 'Home to one-horned rhino', 'Largest river island', 'Historical site', 'Ancient temple', 'Cultural artifacts', 'Mighty river'],
            'Rating': [4.5, 4.8, 4.3, 4.0, 4.2, 3.9, 4.7]
        })
        st.warning("Assam_TestData.csv not found. Using sample data instead.")
        return sample_data

data = load_data()

# Create directories for CSV exports if they don't exist
os.makedirs('district_data', exist_ok=True)
os.makedirs('category_data', exist_ok=True)

# Sidebar filters
st.sidebar.markdown("<h2 style='text-align: center;'>Filter Options</h2>", unsafe_allow_html=True)

# Dropdown for Districts with "All" option
districts = sorted(data["District"].unique())
district_options = ["All Districts"] + districts
selected_district = st.sidebar.selectbox("Select District", district_options)

# Dropdown for Categories with "All" option
categories = sorted(data["Category"].unique())
category_options = ["All Categories"] + categories
selected_category = st.sidebar.selectbox("Select Category", category_options)

# Apply filters
if selected_district == "All Districts" and selected_category == "All Categories":
    filtered_data = data
elif selected_district == "All Districts":
    filtered_data = data[data["Category"] == selected_category]
elif selected_category == "All Categories":
    filtered_data = data[data["District"] == selected_district]
else:
    filtered_data = data[(data["District"] == selected_district) & (data["Category"] == selected_category)]

# Display download buttons for filtered data
st.sidebar.markdown("### Download Filtered Data")
if not filtered_data.empty:
    csv = filtered_data.to_csv(index=False)
    st.sidebar.download_button(
        label="Download as CSV",
        data=csv,
        file_name=f"assam_tourism_filtered.csv",
        mime="text/csv"
    )

# Optional: Add district and category download options
st.sidebar.markdown("### Export District/Category Data")
if st.sidebar.button("Export All District Data"):
    for district in districts:
        district_data = data[data["District"] == district]
        file_path = f"district_data/{district.replace(' ', '_')}_tourism.csv"
        district_data.to_csv(file_path, index=False)
    st.sidebar.success(f"Exported data for {len(districts)} districts to 'district_data' folder")

if st.sidebar.button("Export All Category Data"):
    for category in categories:
        category_data = data[data["Category"] == category]
        safe_category = category.replace('/', '_').replace(' ', '_')
        file_path = f"category_data/{safe_category}_tourism.csv"
        category_data.to_csv(file_path, index=False)
    st.sidebar.success(f"Exported data for {len(categories)} categories to 'category_data' folder")

# Display summary based on filters
st.markdown("<div class='css-card'>", unsafe_allow_html=True)
if selected_district == "All Districts" and selected_category == "All Categories":
    st.subheader("Showing all tourism attractions in Assam")
elif selected_district == "All Districts":
    st.subheader(f"Showing all {selected_category} attractions in Assam")
elif selected_category == "All Categories":
    st.subheader(f"Showing all attractions in {selected_district}")
else:
    st.subheader(f"Showing {selected_category} attractions in {selected_district}")

st.write(f"Total attractions found: {len(filtered_data)}")
st.markdown("</div>", unsafe_allow_html=True)

# Show filtered data in an expandable section
st.markdown("<div class='css-card'>", unsafe_allow_html=True)
st.subheader("Filtered Tourism Data")
with st.expander("Show/Hide Data Table", expanded=True):
    st.dataframe(filtered_data, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Visualizations
if not filtered_data.empty:
    st.markdown("<div class='css-card'>", unsafe_allow_html=True)
    st.subheader("Visualizations")
    
    # Create tabs for different visualizations
    tab1, tab2 = st.tabs(["Distribution by Category", "Ratings Analysis"])
    
    with tab1:
        # Category distribution
        fig, ax = plt.subplots(figsize=(10, 5))
        category_counts = filtered_data["Category"].value_counts()
        if not category_counts.empty:
            sns.barplot(x=category_counts.index, y=category_counts.values, ax=ax)
            plt.xticks(rotation=45, ha='right')
            plt.title("Number of Attractions by Category")
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("No category data available for the current selection.")
    
    with tab2:
        # Ratings visualization (if column exists)
        if "Rating" in filtered_data.columns and not filtered_data["Rating"].dropna().empty:
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            sns.histplot(filtered_data["Rating"].dropna(), bins=10, kde=True, ax=ax2)
            plt.title("Distribution of Attraction Ratings")
            plt.xlabel("Rating")
            plt.ylabel("Frequency")
            st.pyplot(fig2)
        else:
            st.info("No rating data available for visualization.")
    
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.warning("No data found matching the selected filters.")

# Map visualization (if coordinates exist)
if {"Latitude", "Longitude"}.issubset(filtered_data.columns) and not filtered_data.empty:
    st.markdown("<div class='css-card'>", unsafe_allow_html=True)
    st.subheader("Map of Tourism Attractions")
    map_data = filtered_data[["Latitude", "Longitude", "Name"]].dropna()
    if not map_data.empty:
        st.map(map_data)
    else:
        st.info("No geographic coordinates available for the selected attractions.")
    st.markdown("</div>", unsafe_allow_html=True)

# Footer with images
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding: 20px; background-color: #f0f2f6; border-radius: 10px;">
    <p>© 2025 Assam Tourism Data Explorer | Discover the beauty of Northeast India</p>
</div>
""", unsafe_allow_html=True)

# Add instructions at the bottom
st.markdown("""
### How to use this app:
1. Use the dropdowns in the sidebar to filter tourism attractions by District and Category
2. View the filtered data in the table
3. Explore visualizations to better understand the tourism landscape
4. Download the filtered data as a CSV file for further analysis
5. Use the export buttons to save all district or category data as separate CSV files
""")