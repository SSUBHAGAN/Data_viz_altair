import pandas as pd
import numpy as np
import altair as alt
import streamlit as st


alt.data_transformers.disable_max_rows()
# Load the Superstore dataset

df = pd.read_excel("output.xlsx")

region_list = list(df['Region'].unique())
segment_list = list(df['Segment'].unique())
category_list = list(df['Category'].unique())
category_list.insert(0, "All Categories")
df['YYYY'] = df['Order Date'].apply(lambda x: x.year)

min_year = df['YYYY'].min()
max_year = df['YYYY'].max()

# Create the Streamlit app
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Superstore Sales Dashboard</h1>", unsafe_allow_html=True)
#st.title("Superstore Sales Dashboard")
#st.markdown("---") 

# Sidebar filters
st.sidebar.title("Filters")
start_year, end_year = st.sidebar.slider("Period", min_value=int(min_year), max_value=int(max_year),
    value=(int(min_year),int(max_year)))
segment = st.sidebar.selectbox('Segments', segment_list)
region = st.sidebar.multiselect("Region", df['Region'].unique(),default =region_list)
category = st.sidebar.selectbox("Category", category_list)
if category != "All Categories":
    filtered_data = df[(df['YYYY'] >= start_year) & (df['YYYY'] <= end_year) & (df['Category'] == category) & (df['Region'].isin(region)) &(df['Segment'] == segment)]
else:
    filtered_data = df[(df['YYYY'] >= start_year) & (df['YYYY'] <= end_year) & (df['Region'].isin(region))]


# Filter the data based on the selected filters
#filtered_data = df[(df['YYYY'] >= start_year) & (df['YYYY'] <= end_year) & (df['Category'] == category) & (df['Region'].isin(region))]

 
# Calculate total sales and profit
total_sales = round(filtered_data['Sales'].sum(),2)
total_profit = round(filtered_data['Profit'].sum(),2)
total_returns = round(filtered_data.loc[filtered_data['Returned'] == 'Yes', 'Sales'].sum(), 2)
Average_discount = round(filtered_data['Discount'].mean(),2)

# Display total sales and profit
col1, col2,col3,col4 = st.columns(4)
with col1:
    st.markdown(
        f"""
        <div style='border: 1px solid black; padding: 10px;'>
            <h3>Total Sales: $ {total_sales}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style='border: 1px solid black; padding: 10px;'>
            <h3>Total Returns: $ {total_returns}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        f"""
        <div style='border: 1px solid black; padding: 10px;'>
            <h3>Total Profit: $ {total_profit}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
with col4:
    st.markdown(
        f"""
        <div style='border: 1px solid black; padding: 10px;'>
            <h3>Avg Discount Rate: {Average_discount*100:.2f} %</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

#col1.markdown(f"### Total Sales: $ {total_sales}")
#col2.markdown(f"### Total Profit: $ {total_profit}")

#col3.markdown(f"### Total Returns: $ {total_returns}")
#col4.markdown(f"### Avg Discount: {Average_discount*100:.2f} %")
#st.write("### Total Sales:", total_sales)
#st.write("### Total Profit:", total_profit)
#st.write("### Total Returns:", total_returns)
#st.write("### Average Discounts Rate:", Average_discount)
#st.markdown("<br>", unsafe_allow_html=True)


# Bar chart showing sales by sub-category
col1, col2 = st.columns(2)

# Bar chart showing sales by sub-category
subcat_sales_chart = alt.Chart(filtered_data).mark_bar().encode(
    x=alt.X('Sub-Category:N', title= 'Sub-Category'),
    y=alt.Y('sum(Profit):Q', title = 'Profit'),
    color=alt.Color('Region:N', legend=None),
    tooltip=['Sub-Category:N', 'sum(Sales):Q', 'sum(Profit):Q']
).properties(
    width=600,
    height=400
)
# Display the charts
col1, col2 = st.columns(2)
scatter_chart= alt.Chart(filtered_data).mark_circle(size=60).encode(
    x=alt.X('Sales', title='Sales'),
    y=alt.Y('Profit', title='Profit'),
    color=alt.Color('Region:N', legend=alt.Legend(title='Region')),
    tooltip=['Sales', 'Profit', 'Region']
).properties(
    width=600,
    height=400
)
trendlines1 = scatter_chart.transform_regression(
    on='Sales',
    regression='Profit',
    groupby=['Region']
).mark_line()




# Line chart showing sales over time
profit_over_time_chart = alt.Chart(filtered_data).mark_area(interpolate='basis').encode(
    x=alt.X('yearmonth(Order Date):T', title='Month'),
    y=alt.Y('sum(Sales):Q', title=f'Sales'),
    color=alt.Color('Region:N', legend=alt.Legend(orient='top'))
).properties(
    width=600,
    height=400
)

# Bar chart showing returns by sub-category
category_returns_chart = alt.Chart(filtered_data[filtered_data['Returned'] == 'Yes']).mark_bar().encode(
    y=alt.X('Sub-Category:N', title='Sub-Category'),
    x=alt.Y('sum(Sales):Q', title='Returns'),
    color=alt.Color('Region:N', legend=alt.Legend(orient='top'))
).properties(
    width=600,
    height=400
)

col1.write(f" **Profits by Sub-Category**")
col1.altair_chart(subcat_sales_chart)
col2.write(f" **Sales vs. Profit**")
col2.altair_chart(scatter_chart+trendlines1)

col1.write(f" **Sales Over Time**")
col1.altair_chart(profit_over_time_chart)

col2.write(f" **Returns by Sub-Category**")
col2.altair_chart(category_returns_chart)







