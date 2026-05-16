import pandas as pd
import streamlit as st
import altair as alt

# ======================
# PAGE SETUP
# ======================
st.set_page_config(
    page_title="Vacature Dashboard",
    layout="wide"
)

# ======================
# DATA
# ======================
df = pd.read_csv("vacatures.csv")
df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")

# ======================
# TITLE
# ======================
st.title("💼 Vacature Analyse Dashboard")
st.caption("Python • Pandas • Streamlit • Data Analysis")

st.divider()

# ======================
# SIDEBAR FILTERS
# ======================
st.sidebar.header("🔎 Filters")

stad = st.sidebar.text_input("Stad")
functie = st.sidebar.text_input("Functie")

min_salary = int(df["Salary"].min(skipna=True))
max_salary = int(df["Salary"].max(skipna=True))

salary_range = st.sidebar.slider(
    "Salaris range",
    min_salary,
    max_salary,
    (min_salary, max_salary)
)

# ======================
# FILTERING
# ======================
filtered_df = df.copy()

if stad:
    filtered_df = filtered_df[
        filtered_df["location"].str.contains(stad, case=False, na=False)
    ]

if functie:
    filtered_df = filtered_df[
        filtered_df["job_title"].str.contains(functie, case=False, na=False)
    ]

filtered_df = filtered_df[
    (filtered_df["Salary"] >= salary_range[0]) &
    (filtered_df["Salary"] <= salary_range[1])
]

# ======================
# KPI'S
# ======================
col1, col2, col3 = st.columns(3)

col1.metric("Vacatures", len(filtered_df))

col2.metric(
    "Gemiddeld salaris",
    f"€ {filtered_df['Salary'].mean():,.0f}" if len(filtered_df) > 0 else "N/A"
)

col3.metric(
    "Hoogste salaris",
    f"€ {filtered_df['Salary'].max():,.0f}" if len(filtered_df) > 0 else "N/A"
)

st.divider()

# ======================
# VACATURES
# ======================
st.subheader("📄 Vacatures")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# ======================
# TOP 5
# ======================
st.subheader("🔥 Top 5 best betaalde vacatures")

top5 = filtered_df.sort_values(by="Salary", ascending=False).head(5)

st.dataframe(
    top5,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ======================
# GRAFIEK
# ======================
st.subheader("📊 Salaris per locatie")

if len(filtered_df) > 0:
    chart_data = filtered_df.groupby("location", as_index=False)["Salary"].mean()

    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X("location:N", title="Locatie"),
        y=alt.Y("Salary:Q", title="Gemiddeld salaris")
    )

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Geen data beschikbaar voor grafiek")

# ======================
# DOWNLOAD
# ======================
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download gefilterde vacatures",
    data=csv,
    file_name="vacatures_portfolio.csv",
    mime="text/csv"
)

# ======================
# FOOTER
# ======================
st.caption("Portfolio project • Python • Pandas • Streamlit")