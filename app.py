import streamlit as st
import business_recommender as br

st.set_page_config(page_title="Business Recommendation System", layout="wide")

st.title("📊 Business Recommendation System")
st.write("Type an area name to find profitable business opportunities.")

@st.cache_data
def load_data():
    return br.load_dataset("Final_Business_Data.xlsx")

df = load_data()

# User input: area name only
selected_area = st.text_input("🏙 Enter Area Name", "Koregaon Park")

if st.button("🔍 Get Recommendations"):
    results = br.recommend_top(df, selected_area, top_n=8)  # Fixed at 8
    if results.empty:
        st.warning("No recommendations found for this area.")
    else:
        st.success(f"Top business opportunities in {selected_area}:")
        st.dataframe(results)
