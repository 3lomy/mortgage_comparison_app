#!/usr/bin/env python
# coding: utf-8

# In[3]:


# packages for data manipulation
import pandas as pd


# In[4]:


# packages for data visualization
import plotly
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.subplots as sp


# In[ ]:


# packages for dash components
from dash import dash_table


# In[ ]:





# In[ ]:


def create_schedule_table(schedule_df):
      
    # List of columns to format
    columns_to_format = ['Loan Balance', 'Principal Paid', 'Interest Paid', 'Total Payment']

    # Apply the formatting function to each column in the list
    for column in columns_to_format:
        schedule_df[column] = schedule_df[column].apply(lambda x: '{:,.2f}'.format(x))

    table_layout = dash_table.DataTable(
    id='datatable-interactivity',
    columns=[
        {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False}
        if i == "Payment Date" or i == "Loan Balance" 
        else {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
        for i in schedule_df.columns
    ],

    data=schedule_df.to_dict('records'),  # the contents of the table
    editable=True,              # allow editing of data inside all cells
    filter_action="native",     # allow filtering of data by user ('native') or not ('none')
    sort_action="native",       # enables data to be sorted per-column by user or not ('none')
    sort_mode="single",         # sort across 'multi' or 'single' columns
    column_selectable="multi",  # allow users to select 'multi' or 'single' columns
    row_selectable="multi",     # allow users to select 'multi' or 'single' rows
    row_deletable=True,         # choose if user can delete a row (True) or not (False)
    selected_columns=[],        # ids of columns that user selects
    selected_rows=[],           # indices of rows that user selects
    page_action="native",       # all data is passed to the table up-front or not ('none')
    page_current=0,             # page number that user is on
    page_size=15,               # number of rows visible per page
    style_cell={                # ensure adequate header width when text is shorter than cell's text
        'minWidth': 95, 'maxWidth': 95, 'width': 95
    },
    style_cell_conditional=[    # align text columns to left. By default they are aligned to right
        {'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Country Name', 'Country Code']
    ],

    style_data={                # overflow cells' content into multiple lines
        'whiteSpace': 'normal',
        'height': 'auto'
    },

    style_table={
                'overflowX': 'auto',  # Enable horizontal scrolling if needed
                'height': '400px',    # Set the desired height of the table
                'width': '100%',      # Set the width of the table to 100% of the container
            },)

    return table_layout


# In[ ]:





# In[ ]:


def create_waterfall_chart(df):
    
    if df.empty:  # Check if the DataFrame is empty
        return {'data': [], 'layout': {}}

    # Reverse the order of categories
    categories = ['Total Payment', 'Principal Paid', 'Interest Paid', 'Loan Amount']

    # Create subplots
    waterfall_chart = make_subplots(rows=len(df['Mortgage Lender'].unique()), cols=1, shared_xaxes=True, vertical_spacing=0.05)

    # Add Waterfall charts for each mortgage lender
    for i, lender in enumerate(df['Mortgage Lender'].unique(), start=1):
        lender_data = df[df['Mortgage Lender'] == lender]

        # Add Total Payment block
        waterfall_chart.add_trace(go.Waterfall(
            x=categories,
            y=[lender_data['Total Payment'].iloc[0], 
               -lender_data['Total Principal Paid'].iloc[0], 
               -lender_data['Total Interest Paid'].iloc[0], 
               lender_data['Loan Amount'].iloc[0]],
            name='',
            orientation='v',
            textposition='inside',
            text=[f"{amount:,.2f}" for amount in [lender_data['Total Payment'].iloc[0], 
                                                  -lender_data['Total Principal Paid'].iloc[0], 
                                                  -lender_data['Total Interest Paid'].iloc[0], 
                                                  lender_data['Loan Amount'].iloc[0]]],  # Labels for each block
            connector={'line': {'color': 'red'}},
            increasing={'marker': {'color': 'red'}},
            decreasing={'marker': {'color': 'green'}},  # Change to green for decreasing (Loan Amount)
        ), row=i, col=1)

        # Add title for each subplot
        title_text = lender
        title_y = -0.05  # Adjust this value to control the vertical position of the title
        waterfall_chart.add_annotation(
            go.layout.Annotation(
                text=title_text,
                xref='paper', yref='paper',
                x=0.2, y=title_y,
                showarrow=False,
                font=dict(size=16, family="Arial"),
                align='right',  # Align the annotation to the right
                xanchor='right',  # Anchor the annotation to the right
                yanchor='bottom'  # Anchor the annotation to the bottom
            ),
            row=i, col=1
        )

    # Update layout with chart title
    waterfall_chart.update_layout(
        title_text="Loan Amortization Summary",  # Add chart title
        title_font=dict(size=20),  # Adjust title font size
        height=350 * len(df['Mortgage Lender'].unique()),  # Adjust height based on the number of banks
        showlegend=False,
    )

   # Ensure the images directory exists
    images_dir = 'images'
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    # Save the image to the directory
    image_path = os.path.join(images_dir, 'waterfall_chart.png')
    waterfall_chart.write_image(image_path)
    
    # waterfall_chart.write_image(r'images\waterfall_chart.png')
    
    return waterfall_chart


# In[ ]:





# In[ ]:


def create_pie_chart(df):
    
    pie_chart = sp.make_subplots(rows=1, cols=2, 
                                 subplot_titles=df['Mortgage Lender'].unique(), 
                                 specs=[[{'type':'domain'}, {'type':'domain'}]])

    # Pie chart for Interest vs. Principal Breakdown
    for i, lender in enumerate(df['Mortgage Lender'].unique(), start=1):
        lender_data = df[df['Mortgage Lender'] == lender]

        pie_chart.add_trace(go.Pie(
            labels=['Interest', 'Principal'],
            values=[lender_data['Total Interest Paid'].iloc[0], lender_data['Total Principal Paid'].iloc[0]],
            hole=0.3,
            textinfo='label+percent',
            name=lender
        ), row=1, col=i)

    pie_chart.update_layout(title='Total Payment Breakdown: Interest vs. Principal', 
                            title_font=dict(size=20),  # Adjust title font size
                            showlegend=False)
    
    pie_chart.write_image(r'images\pie_chart.png')

    
    return pie_chart


# In[ ]:





# In[ ]:


def create_radar_chart(df):
    
    radar_chart = go.Figure()
    for lender in df['Mortgage Lender'].unique():
        lender_data = df[df['Mortgage Lender'] == lender]
        radar_chart.add_trace(go.Scatterpolar(r=lender_data.iloc[0][['Loan Amount', 'Total Interest Paid', 'Total Principal Paid', 'Total Payment']],
                                             theta=['Loan Amount', 'Total Interest Paid', 'Total Principal Paid', 'Total Payment'],
                                             fill='toself', name=lender))
        
    radar_chart.update_layout(title='Comparison of Key Metrics', 
                              title_font=dict(size=20),  # Adjust title font size
                              polar=dict(radialaxis=dict(visible=True, range=[0, max(df['Loan Amount'].max(), 
                              df['Total Payment'].max())])))
    
    radar_chart.write_image(r'images\radar_chart.png')
    
    return radar_chart

