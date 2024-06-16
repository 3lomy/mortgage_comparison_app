#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# packages
from dash import Dash 
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dash import dash_table
import i18n
from datetime import date, datetime


# In[ ]:





# In[ ]:


def create_tabs():
    
    waterfall_card = html.Div([dcc.Graph(id='waterfall-chart'),
    ],style={"border": "0px ridge silver",  # outset, groove
                 'box-shadow': '10px 10px 10px 10px rgba(0, 0, 0, 0.2)',
                 'background':'light grey',
                 "padding": "10px"  }
    )

    pie_chart_card = html.Div([dcc.Graph(id='pie-chart'),
    ],style={"border": "0px ridge silver",  # outset, groove
                 'box-shadow': '10px 10px 10px 10px rgba(0, 0, 0, 0.2)',
                 'background':'light grey',
                 "padding": "10px"  }
    )

    radar_chart_card = html.Div([dcc.Graph(id='radar-chart'),
    ],style={"border": "0px ridge silver",  # outset, groove
                 'box-shadow': '10px 10px 10px 10px rgba(0, 0, 0, 0.2)',
                 'background':'light grey',
                 "padding": "10px"  }
    )
    
    # Define the content for each tab
    tab_summary_content = dbc.Card(
        html.Div([
            dbc.Row([waterfall_card]),
            dbc.Row(),
            dbc.Row([pie_chart_card]),
            html.Br(),
            dbc.Row([radar_chart_card]),  
        ]),
    )

    tab_mortgage_lender_1_content = dbc.Card(
        html.Div([
            dcc.Loading(
                 html.Div(id='datatable-container-mortgage-lender-1'),
                 type="circle"
            ), 
            dcc.Loading(
                 html.Div(id='bm-datatable-container-mortgage-lender-1'),
                 type="circle"
            ),
        ]) 
    )

    tab_mortgage_lender_2_content = dbc.Card(

        html.Div([
            dcc.Loading(
                 html.Div(id='datatable-container-mortgage-lender-2'),
                 type="circle"
            ), 
            dcc.Loading(
                 html.Div(id='bm-datatable-container-mortgage-lender-2'),
                 type="circle"
            ), 
        ])

    )
    
    # Update tab labels with translated text
    tab_summary_content_label = i18n.t('general.summary')
    tab_mortgage_lender_1_label = i18n.t('general.mortgage_lender_1')
    tab_mortgage_lender_2_label = i18n.t('general.mortgage_lender_2')
    
    # Construct updated tabs with translated labels
    updated_tabs = dbc.Tabs(
        [
            dbc.Tab(tab_summary_content, 
                    label=tab_summary_content_label,
                    className="mt-10", 
                    activeTabClassName="fw-bold fst-italic",
                    style={"color": "white",}),
            dbc.Tab(tab_mortgage_lender_1_content, 
                    label=tab_mortgage_lender_1_label, 
                    className="mt-10", 
                    activeTabClassName="fw-bold fst-italic",
                    style={"color": "blue",}),
            dbc.Tab(tab_mortgage_lender_2_content, 
                    label=tab_mortgage_lender_2_label, 
                    className="mt-10", 
                    activeTabClassName="fw-bold fst-italic",
                    style={"color": "blue",}), 
        ]
    )
    
    return updated_tabs


# In[ ]:





# In[ ]:


def create_fixed_mortgage_input_mask(frm_id, loan_amount_input_id, loan_amount_label_id,
                                     interest_rate_input_id, interest_rate_label_id,
                                     term_input_id, term_label_id,
                                     start_date_input_id, start_date_label_id):
    return html.Div([
                    # loan input
                    dbc.Row([
                        dbc.Col([
                            dbc.Label(i18n.t('input_mask.loan_amount') + ":", 
                                      html_for="1000000.00", 
                                      id=loan_amount_label_id
                                     ),
                        ], width=4, align='center'),

                        dbc.Col([
                            dbc.Input(type="number", 
                                      id=loan_amount_input_id, 
                                      placeholder=i18n.t('input_mask.enter_loan_amount')),
                        ], width=5, align='center'),

                    ],justify = 'center', style={'margin-bottom': '3px'}),
                    
                    # interest rate input
                    dbc.Row([
                        dbc.Col([
                            dbc.Label(i18n.t('input_mask.interest_rate') + ":", 
                                      id=interest_rate_label_id),
                        ], width=4, align='center'),

                        dbc.Col([
                            dbc.Input(type="number", 
                                      id=interest_rate_input_id, 
                                      placeholder=i18n.t('input_mask.enter_interest_rate')),
                        ], width=5, align='center'),

                    ],justify = 'center', style={'margin-bottom': '3px'}),
                    
                    # term input
                    dbc.Row([

                        dbc.Col([
                            dbc.Label(i18n.t('input_mask.term') + ":", id=term_label_id),
                        ], width=4, align='center'),

                        dbc.Col([
                            dbc.Input(type="number", 
                                      id=term_input_id, 
                                      placeholder=i18n.t('input_mask.enter_loan_term')),
                        ], width=5, align='center'),

                    ],justify = 'center', style={'margin-bottom': '3px'}),
                    
                    # start date input
                    dbc.Row([

                        dbc.Col([
                            dbc.Label(i18n.t('input_mask.start_date') + ":", id=start_date_label_id),
                        ], width=4, align='center'),

                        dbc.Col([
                            dcc.DatePickerSingle(id=start_date_input_id, min_date_allowed=date.today(), display_format='YYYY-MM-DD',
                                                 max_date_allowed=date(2100, 12, 31), initial_visible_month=date.today(),
                                                 date=date.today()),
                            
                        ], width=5, align='center'),

                    ],justify = 'center', style={'margin-bottom': '2px'}),
    ], id=frm_id, style={'display': 'none'} )


# In[ ]:





# In[ ]:


def create_balloon_mortgage_input_mask(bm_id, loan_amount_id, interest_rate_id, 
                                       term_id, balloon_pmt_id, 
                                       start_date_input_id, start_date_label_id):
    
    return html.Div([
                    # loan input
                    dbc.Row([
                        dbc.Col([
                            dbc.Label(i18n.t('input_mask.loan_amount') + ":", 
                                      html_for="1000000.00", 
                                      id='bm-loan-amount-label-1'),
                        ], width=4, align='center'),

                        dbc.Col([
                            dbc.Input(type="number", 
                                      id=loan_amount_id, 
                                      placeholder=i18n.t('input_mask.enter_loan_amount')),
                        ], width=5, align='center'),

                    ],justify = 'center', style={'margin-bottom': '3px'}),
                    
                    # interest rate input
                    dbc.Row([
                        dbc.Col([
                            dbc.Label(i18n.t('input_mask.interest_rate') + ":", id='bm-interest-rate-label-1'),
                        ], width=4, align='center'),

                        dbc.Col([
                            dbc.Input(type="number", 
                                      id=interest_rate_id, 
                                      placeholder=i18n.t('input_mask.enter_interest_rate')),
                        ], width=5, align='center'),

                    ],justify = 'center', style={'margin-bottom': '3px'}),
    
                    # terms
                    dbc.Row([
                        dbc.Col([
                            dbc.Label(i18n.t('input_mask.term') + ":", id='bm-term-label-1'),
                        ], width=4, align='center'),

                        dbc.Col([
                            dbc.Input(type="number", 
                                      id=term_id, 
                                      placeholder=i18n.t('input_mask.enter_index_rate')),
                        ], width=5, align='center'),

                    ],justify = 'center', style={'margin-bottom': '3px'}),
    
                    # balloon payment amount
                    dbc.Row([
                        dbc.Col([
                            dbc.Label(i18n.t('input_mask.balloon_payment') + ":", id='bm-ballon-amount-label-1'),
                        ], width=4, align='center'),

                        dbc.Col([
                            dbc.Input(type="number", 
                                      id=balloon_pmt_id, 
                                      placeholder=i18n.t('input_mask.enter_balloon_amount'))
                        ], width=5, align='center'),

                    ],justify = 'center', style={'margin-bottom': '3px'}),   
                    
                    dbc.Row([

                        dbc.Col([
                            dbc.Label(i18n.t('input_mask.start_date') + ":", id=start_date_label_id),
                        ], width=4, align='center'),

                        dbc.Col([
                            dcc.DatePickerSingle(id=start_date_input_id, min_date_allowed=date.today(), display_format='YYYY-MM-DD',
                                                 max_date_allowed=date(2100, 12, 31), initial_visible_month=date.today(),
                                                 date=date.today()),
                            
                            
                        ], width=5, align='center'),

                    ],justify = 'center', style={'margin-bottom': '2px'}),
                    
    ], id=bm_id, style={'display': 'none'})


# In[ ]:




