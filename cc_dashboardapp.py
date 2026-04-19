import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(layout="wide")

# TITLE
st.title("India State-wise Cyber Crime Cases Dashboard")


# LOAD DATA

df_summary = pd.read_csv("cleaned_data.csv")
df_long = pd.read_csv("data_long.csv")

df_summary.columns = df_summary.columns.str.strip()
df_long.columns = df_long.columns.str.strip()

df_summary.rename(columns={'STATE/UT': 'State'}, inplace=True)
df_long.rename(columns={'STATE/UT': 'State'}, inplace=True)

df_summary['State'] = df_summary['State'].str.title()
df_long['State'] = df_long['State'].str.title()

# SIDEBAR FILTERS

selected_states = st.sidebar.multiselect(
    "Select States",
    df_long['State'].unique(),
    default=df_long['State'].unique()[:5]
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df_long['Year'].min()),
    int(df_long['Year'].max()),
    (2002, 2020)
)

filtered_df = df_long[
    (df_long['State'].isin(selected_states)) &
    (df_long['Year'].between(year_range[0], year_range[1]))
]

kpi_df = filtered_df if not filtered_df.empty else df_long

# 1. OVERALL KPIs

st.subheader("Overall Cyber Crime Cases in India (2002–2020)")

col1, col2, col3 = st.columns(3)

col1.metric("Total Cases", int(df_long['Cases'].sum()))
col2.metric("Max Cases", int(df_long['Cases'].max()))
col3.metric("Min Cases", int(df_long['Cases'].min()))

st.divider()

# 2. TOP 5 STATES (OVERALL)

top5_df = (
    df_long.groupby('State')['Cases']
    .sum()
    .nlargest(5)
    .reset_index()
)

peak_info = df_long.loc[
    df_long.groupby('State')['Cases'].idxmax(),
    ['State', 'Year', 'Cases']
].copy()

peak_info.rename(columns={
    'Year': 'Peak_Year',
    'Cases': 'Peak_Cases'
}, inplace=True)

top5_df = top5_df.merge(peak_info, on='State').sort_values(by='Cases', ascending=False)

st.subheader("Top 5 States (Highest Cases - Overall)")

top_cols = st.columns(5)

for i, row in top5_df.iterrows():
    top_cols[i].metric(
        label=row['State'],
        value=int(row['Cases']),
        delta=f"Peak: {int(row['Peak_Cases'])} in {int(row['Peak_Year'])}"
    )

st.divider()

# 3. FILTERED KPIs

st.subheader("Filtered Cyber Crime Cases (Selected States & Year Range)")

fcol1, fcol2, fcol3 = st.columns(3)

fcol1.metric("Total Cases", int(kpi_df['Cases'].sum()))
fcol2.metric("Max Cases", int(kpi_df['Cases'].max()))
fcol3.metric("Min Cases", int(kpi_df['Cases'].min()))
# Line chart
st.subheader("Growth Trend")
fig = px.line(
    filtered_df,
    x='Year',
    y='Cases',
    color='State'
)
st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)

col1.metric("Total Cases", int(filtered_df['Cases'].sum()))
if filtered_df.empty:
    col2.metric("Max Cases", "No data")
else:
    col2.metric("Max Cases", int(filtered_df['Cases'].max()))
if filtered_df.empty:
    col3.metric("Min Cases", "No data")
else:
    col3.metric("Min Cases", int(filtered_df['Cases'].min()))

top_states = (
    df_long.groupby('State')['Cases']
    .sum()
    .nlargest(10)
    .reset_index()
)

fig = px.bar(
    top_states,
    x='Cases',
    y='State',
    orientation='h',
    title="Top 10 States"
)


state_summary = df_long.groupby('State').agg(
    Total_Cases=('Cases', 'sum'),
    Max_Cases=('Cases', 'max'),
    Max_Year=('Year', lambda x: x.iloc[x.argmax()]),
    Min_Cases=('Cases', 'min'),
    Min_Year=('Year', lambda x: x.iloc[x.argmin()])
).reset_index()

state_summary = df_long.sort_values('Cases').groupby('State').agg(
    Total_Cases=('Cases', 'sum'),
    Min_Cases=('Cases', 'first'),
    Min_Year=('Year', 'first')
)

state_summary_max = df_long.sort_values('Cases', ascending=False).groupby('State').agg(
    Max_Cases=('Cases', 'first'),
    Max_Year=('Year', 'first')
)

state_summary = state_summary.join(state_summary_max).reset_index()

top_bottom = df_long.groupby('State')['Cases'].sum()

top5 = top_bottom.nlargest(5)
bottom5 = top_bottom.nsmallest(5)

compare_df = pd.concat([top5, bottom5]).reset_index()

fig = px.bar(compare_df, x='Cases', y='State', orientation='h',
             title="Top vs Bottom States")
st.plotly_chart(fig, use_container_width=True)

yearly = df_long.groupby('Year')['Cases'].sum().reset_index()

fig = px.line(yearly, x='Year', y='Cases',
              title="Overall India Cyber Crime Growth Trend")
st.plotly_chart(fig, use_container_width=True)

fig = px.histogram(df_summary, x='Peak_year',
                   title="Peak Year Frequency")
st.plotly_chart(fig)

df_long['Growth'] = df_long.groupby('State')['Cases'].pct_change()

fig = px.line(df_long, x='Year', y='Growth', color='State',
              title="Growth Rate Trend")
st.plotly_chart(fig, use_container_width=True)

import json

with open("india_state.geojson") as f:
    india_geojson = json.load(f)

fig = px.choropleth(
    state_summary,
    geojson=india_geojson,
    featureidkey='properties.NAME_1', 
    locations='State',
    color='Total_Cases',
    hover_data=['Max_Cases', 'Max_Year', 'Min_Cases', 'Min_Year'],
    color_continuous_scale='Reds'
)

fig.update_geos(fitbounds="locations", visible=False)

st.subheader("India State-wise Analysis Map")
st.plotly_chart(fig, use_container_width=True)

state_mapping = {
    # Standard states
    "BIHAR": "Bihar",
    "ODISHA": "Odisha",
    "MADHYA PRADESH": "Madhya Pradesh",
    "MEGHALAYA": "Meghalaya",
    "GOA": "Goa",
    "PUDUCHERRY": "Puducherry",
    "HIMACHAL PRADESH": "Himachal Pradesh",
    "UTTAR PRADESH": "Uttar Pradesh",
    "WEST BENGAL": "West Bengal",
    "TRIPURA": "Tripura",
    "RAJASTHAN": "Rajasthan",
    "GUJARAT": "Gujarat",
    "ASSAM": "Assam",
    "KARNATAKA": "Karnataka",
    "ANDHRA PRADESH": "Andhra Pradesh",
    "TAMIL NADU": "Tamil Nadu",
    "HARYANA": "Haryana",
    "ARUNACHAL PRADESH": "Arunachal Pradesh",
    "MAHARASHTRA": "Maharashtra",
    "MIZORAM": "Mizoram",
    "PUNJAB": "Punjab",
    "KERALA": "Kerala",
    "TELANGANA": "Telangana",
    "MANIPUR": "Manipur",
    "JHARKHAND": "Jharkhand",
    "SIKKIM": "Sikkim",
    "NAGALAND": "Nagaland",
    "CHHATTISGARH": "Chhattisgarh",
    "UTTARAKHAND": "Uttarakhand",

    # Union Territories / tricky ones
    "DELHI": "Delhi",
    "CHANDIGARH": "Chandigarh",
    "LAKSHADWEEP": "Lakshadweep",

    # Special cases (VERY IMPORTANT)
    "A & N ISLANDS": "Andaman and Nicobar Islands",
    "DAMAN & DIU": "Daman and Diu",
    "D & N HAVELI": "Dadra and Nagar Haveli",

    # Combined UT (new structure in many GeoJSONs)
    "DADRA AND NAGAR HAVELI AND DAMAN AND DIU": "Dadra and Nagar Haveli and Daman and Diu",

    # Jammu & Kashmir split issue
    "JAMMU & KASHMIR": "Jammu and Kashmir",
    "LADAKH": "Ladakh"
}

df_summary['State'] = df_summary['State'].replace(state_mapping)
df_long['State'] = df_long['State'].replace(state_mapping)
