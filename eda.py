import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Global Superstore EDA", layout="wide")

# Title
st.title("📊 Exploratory Data Analysis - Global Superstore Dataset")
df = pd.read_csv("Sample - Superstore.csv", encoding='ISO-8859-1')

# Data cleaning
df.drop_duplicates(inplace=True)
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to", ["Dataset Overview", "Univariate Analysis", "Bivariate Analysis", "Time Series", "Business Insights"])

# Overview
if option == "Dataset Overview":
    st.subheader("📁 Dataset Overview")
    st.write(df.head())
    st.write("Shape of dataset:", df.shape)
    st.write("Missing values:", df.isnull().sum().sum())
    st.write("Data Types:")
    st.write(df.dtypes)

# Univariate Analysis
elif option == "Univariate Analysis":
    st.subheader("📈 Univariate Analysis")
    
    num_cols = ['Sales', 'Quantity', 'Discount', 'Profit']
    cat_cols = ['Category', 'Sub-Category', 'Region', 'Segment', 'Ship Mode']

    st.markdown("**Numerical Distributions**")
    for col in num_cols:
        fig, ax = plt.subplots()
        sns.histplot(df[col], kde=True, ax=ax)
        st.pyplot(fig)

    st.markdown("**Categorical Distributions**")
    for col in cat_cols:
        fig, ax = plt.subplots()
        sns.countplot(data=df, x=col, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

# Bivariate Analysis
elif option == "Bivariate Analysis":
    st.subheader("🔁 Bivariate/Multivariate Analysis")
    
    st.markdown("**Correlation Heatmap**")
    fig, ax = plt.subplots()
    sns.heatmap(df[['Sales', 'Quantity', 'Discount', 'Profit']].corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    st.markdown("**Profit by Category**")
    fig = px.bar(df.groupby('Category')['Profit'].sum().reset_index(), x='Category', y='Profit', title="Profit by Category")
    st.plotly_chart(fig)

    st.markdown("**Sales by Region**")
    fig = px.bar(df.groupby('Region')['Sales'].sum().reset_index(), x='Region', y='Sales', title="Sales by Region")
    st.plotly_chart(fig)

# Time Series
elif option == "Time Series":
    st.subheader("📅 Time Series Analysis")

    df['Month-Year'] = df['Order Date'].dt.to_period('M').astype(str)
    monthly_sales = df.groupby('Month-Year')['Sales'].sum().reset_index()

    fig = px.line(monthly_sales, x='Month-Year', y='Sales', markers=True, title="Monthly Sales Trend")
    st.plotly_chart(fig)

# Business Insights
elif option == "Business Insights":
    st.subheader("💡 Key Business Insights")
    st.markdown("""
    - 🟢 **West and East regions** have the highest revenue. Focus efforts there.
    - 🟢 **Technology category** is the most profitable. Invest more in it.
    - 🔴 **Furniture category** incurs losses often. Review pricing/discount strategy.
    - 🔴 **Higher discounts** negatively affect profit margins.
    - 🟢 **Consumer segment** has the most orders—ideal for targeted marketing.
    - 🟡 **Same Day shipping** is underused—consider promoting it for high-value orders.
    - 🟢 **Sales peak in Q4**—plan marketing campaigns accordingly.
    """)

