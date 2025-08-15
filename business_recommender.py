import pandas as pd
import numpy as np
import re

# ----------------------
# Load Dataset
# ----------------------
def load_dataset(file_path):
    df = pd.read_excel(file_path)
    df["address_clean"] = df["address"].apply(clean_text)
    return df

# ----------------------
# Helper: Clean text
# ----------------------
def clean_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)  # remove punctuation
    text = re.sub(r'\s+', ' ', text).strip()  # remove extra spaces
    return text

# ----------------------
# Step 1: Area Filtering
# ----------------------
def filter_by_area(df, area_name):
    area_clean = clean_text(area_name)
    words = area_clean.split()
    variations = [area_clean]

    if len(words) > 1:
        abbreviations = ''.join(w[0] for w in words)
        variations.append(abbreviations)

    variations += [
        area_clean.replace("gaon", "goan"),
        area_clean.replace("goan", "gaon")
    ]

    mask = df["address_clean"].apply(lambda x: any(var in x for var in variations))
    return df[mask].copy()

# ----------------------
# Step 2: Business Density
# ----------------------
def business_density(data):
    density = data['business_type'].value_counts().reset_index()
    density.columns = ['business_type', 'count']
    return density

# ----------------------
# Step 3: Gap Analysis
# ----------------------
def gap_analysis(data, full_df, min_area_count=2, min_other_count=5):
    other_df = full_df[~full_df.index.isin(data.index)]
    area_counts = data['business_type'].value_counts().reset_index()
    area_counts.columns = ['business_type', 'count_in_area']

    other_counts = other_df['business_type'].value_counts().reset_index()
    other_counts.columns = ['business_type', 'count_elsewhere']

    merged = pd.merge(area_counts, other_counts, on='business_type', how='outer').fillna(0)

    gaps = merged[
        (merged['count_in_area'] <= min_area_count) &
        (merged['count_elsewhere'] >= min_other_count)
    ].sort_values(by='count_elsewhere', ascending=False)

    return gaps.reset_index(drop=True)

# ----------------------
# Step 4: Profitability Ranking
# ----------------------
def profitability_ranking(full_df, gap_df):
    agg = full_df.groupby('business_type').agg(
        avg_rating=('rating', 'mean'),
        avg_reviews=('user_rating_total', 'mean')
    ).reset_index()

    merged = pd.merge(gap_df, agg, on='business_type', how='left')
    merged['profitability_score'] = (
        merged['avg_rating'] * np.log1p(merged['avg_reviews'])
    )
    return merged.sort_values(by='profitability_score', ascending=False).reset_index(drop=True)

# ----------------------
# Step 5: Final Ranking
# ----------------------
def final_ranking(profit_df, top_n=8):
    df = profit_df.copy()
    df['inverse_density_score'] = 1 / (df['count_in_area'] + 1)

    df['inv_density_norm'] = (
        (df['inverse_density_score'] - df['inverse_density_score'].min()) /
        (df['inverse_density_score'].max() - df['inverse_density_score'].min())
    )
    df['profit_norm'] = (
        (df['profitability_score'] - df['profitability_score'].min()) /
        (df['profitability_score'].max() - df['profitability_score'].min())
    )

    df['final_score'] = (df['inv_density_norm'] * 0.5) + (df['profit_norm'] * 0.5)
    return df.sort_values(by='final_score', ascending=False).head(top_n).reset_index(drop=True)

# ----------------------
# Main Recommendation Function
# ----------------------
def recommend_top(df, area_name, top_n=8):
    df_area = filter_by_area(df, area_name)
    if df_area.empty:
        return pd.DataFrame()

    gap_df = gap_analysis(df_area, df)
    profit_df = profitability_ranking(df, gap_df)
    final_df = final_ranking(profit_df, top_n)
    return final_df
