import streamlit as st
import numpy as np
import pandas as pd
import math, time
from pathlib import Path
#Graph: 
import plotly.express as px


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Proof of concept animiated scatter chart',
    page_icon=':time:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------


# Sample DataFrame
# Generate sample data for 2023
np.random.seed(42)
months = pd.date_range('2023-01-01', '2023-12-31', freq='M').strftime('%Y-%m')
departments = ['HR', 'BU2', 'BU3', 'Finance', 'IT', 'Sales']
data = pd.DataFrame({
    'Department': np.repeat(departments, len(months)),
    'Month_Year': np.tile(months, len(departments)),
    'Revenue': np.random.randint(100, 1000, len(departments) * len(months)),
    'Margin(%)': np.random.uniform(5, 25, len(departments) * len(months)),  # Margin in percentages
    'Headcount': np.random.randint(50, 500, len(departments) * len(months))  # Headcount as size
})


data['Month_Year'] = pd.to_datetime(data['Month_Year'])

min_value = data['Month_Year'].min()
max_value = data['Month_Year'].max()


from_year, to_year = st.date_input(
    'Which month-years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

departmentss = data['Department'].unique()

if not len(departmentss):
    st.warning("Select at least one department")

selected_departmentss = st.multiselect(
    'Which departments would you like to view?',
    departmentss,
    ['HR', 'BU2', 'BU3', 'Finance', 'IT', 'Sales']
    )

# Filter the data
filtered_data = data[
    (data['Department'].isin(selected_departmentss))
    & (data['Month_Year'].dt.date <= to_year)
    & (from_year <= data['Month_Year'].dt.date)
]




# Create animated scatter plot using Plotly Express
fig = px.scatter(filtered_data, y='Revenue', x='Margin(%)', animation_frame='Month_Year',
                 animation_group='Department', size='Headcount', color='Department', 
                 text='Department', range_x=[0, 30], range_y=[0, 1500],
                 labels={'Revenue': 'Revenue', 'Margin(%)': 'Margin %'})

# Add annotation for Month_Year on each frame
 
fig.update_layout(
    updatemenus=[{
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 1000, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        'type': 'buttons',
        'showactive': False
    }],
    annotations=[
        dict(
            text='Month: ', x=0.5, y=1.15, xref='paper', yref='paper', showarrow=False, font=dict(size=16))
    ]
)


st.header('Animated Scatter Plot: Revenue vs Margin by Department', divider="rainbow")
# Show plot in Streamlit
st.plotly_chart(fig)

st.header('Random Data Generated', divider="grey")
st.dataframe(data, hide_index=True, use_container_width= True)