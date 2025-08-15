# Business-Recommendation-System



**Technologies:** Python, Pandas, NumPy, Streamlit, Web Scraping

---

## Project Overview
The **Business Recommendation System** is a data-driven application that identifies **profitable and underserved business opportunities** in selected areas of Pune. The system helps entrepreneurs make informed decisions by analyzing market demand, competition gaps, and customer review insights.

---

## Key Features
- **Data Collection & Cleaning:** Scraped and processed business data including name, address, type, geolocation, ratings, and review counts.
- **Market Analysis:** Implemented area-based filtering, business density analysis, gap detection, and profitability scoring to rank business opportunities.
- **Interactive Dashboard:** Developed a **Streamlit UI** for dynamic selection of area and business type, displaying top recommended business types.
- **Opportunity Scoring:** Combines market gap and profitability metrics into a **final ranking score** for actionable recommendations.

---

## Workflow
1. **Data Cleaning:** Standardize addresses and remove noise.
2. **Area Filtering:** Identify businesses in the selected area using text matching and variations.
3. **Density & Gap Analysis:** Detect underserved business types with high demand elsewhere.
4. **Profitability Scoring:** Rank business types using average ratings and review counts.
5. **Final Recommendations:** Combine inverse density and profitability scores for top opportunities.

---

## Installation & Usage
1. Clone the repository:
```bash
git clone https://github.com/yourusername/business-recommendation-system.git
Navigate to the project folder:

bash
Copy
Edit
cd business-recommendation-system
Install required packages:

bash
Copy
Edit
pip install -r requirements.txt
Run the Streamlit app:

bash
Copy
Edit
streamlit run app.py
Open the browser and select a location and business type to get top recommendations.

Dataset
The dataset contains scraped business information from Pune, including:

Business Name

Address

Business Type

Latitude & Longitude

Ratings & Number of Reviews

Note: Dataset cleaning and preprocessing is included in the code.

Outcome
Provides data-driven insights for entrepreneurs.

Identifies high-potential business types in specific localities.

Offers an interactive and user-friendly interface for exploration and recommendation.



Author
Faizal Mistry


