import datetime
import calendar

import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

from datetime import datetime

#Data Preparation
file = 'https://services1.arcgis.com/qAo1OsXi67t7XgmS/arcgis/rest/services/Building_Permits/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'

building_permit_original = gpd.read_file(file)

columns_to_keep = [
    'PERMITNO',
    'PERMIT_TYPE',
    'FOLDERNAME',
    'PERMIT_STATUS',
    'ISSUE_DATE',
    'ISSUE_YEAR',
    'SUB_WORK_TYPE',
    'WORK_TYPE',
    'CONSTRUCTION_VALUE',
    'PERMIT_FEE'
    ]

building_permit_v1 = building_permit_original[columns_to_keep]

correct_date = building_permit_v1['ISSUE_DATE']

for i in range(len(correct_date)):
    date_first = correct_date[i]
    unix_timestamp_seconds = date_first / 1000  # Convert to seconds
    date_object = datetime.utcfromtimestamp(unix_timestamp_seconds)
    formatted_date = date_object.strftime('%Y/%m/%d %H:%M:%S')
    correct_date[i] = formatted_date

building_permit_v1['MONTH'] = pd.to_datetime(correct_date).dt.month

building_permit_v1['MONTH'] = [calendar.month_abbr[month] for month in building_permit_v1['MONTH']]

st.title('City of Kitchener - Building Permits')

st.subheader('Raw data')

st.write(building_permit_v1)
"""
year = 2023
filtered_data = building_permit_v1[building_permit_v1['ISSUE_YEAR'] == year]
st.subheader(f'Building Permits in {year}')
st.write(filtered_data)

st.title("Construction Value Visualization")
"""
# Create a bar chart
st.subheader("Bar Chart of Construction Value by Month")
construction_value_by_month = building_permit_v1.groupby('ISSUE_YEAR')['CONSTRUCTION_VALUE'].sum()
fig, ax = plt.subplots()
construction_value_by_month.plot(kind='bar', ax=ax)
ax.set_ylabel('Construction Value')
st.pyplot(fig)

st.title("Building Permits Issued By Year")

# Create a bar chart
st.subheader("Bar Chart of Building Permits by Year")
building_permit_by_year = building_permit_v1.groupby(['ISSUE_YEAR'])['PERMITNO'].count()
fig, ax = plt.subplots()
building_permit_by_year.plot(kind='bar', ax=ax)
ax.set_ylabel('Building Permits')
st.pyplot(fig)