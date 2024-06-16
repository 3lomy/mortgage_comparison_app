#!/usr/bin/env python
# coding: utf-8

# Project: Mortgage Comparison App
# 
# Author: Elom Kwamin, FRM
# 
# Date: 04.01.2024

# In[1]:


# packages for frontend
from jupyter_dash import JupyterDash 
from dash import Dash 
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dash import dash_table
from dash.dash import no_update
from dash.dependencies import ALL, MATCH
from dash import callback_context


# In[2]:


# packages for processing
import i18n
# import dash_i18n


# In[3]:


# import local packages
from utils.amortiser import *
import utils.ids as ids
from utils.layout import *
from utils.charts import *


# In[4]:


# datetime
from datetime import date, datetime


# In[5]:


# packages for data visualization
import plotly
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.subplots as sp


# In[6]:


# packages for lotties implementation
import dash_extensions as de


# In[7]:


# setup internationalization


# In[8]:


LOCALE = "en"
i18n.set("locale", LOCALE)
i18n.load_path.append("locale")


# In[9]:


external_stylesheets = [
    dbc.themes.MORPH, #dbc.themes.BOOTSTRAP, 
    "https://use.fontawesome.com/releases/v5.15.4/css/all.css",  # Font Awesome CSS link
    dbc.icons.BOOTSTRAP
]


# In[10]:


# app = JupyterDash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)

# required line before upload to render
server = app.server 

# Set the title of the app
app.title = 'Mortgage Comparison App'


# In[11]:


# Create references with a fixed header style

socials_header_section = dbc.Row([
    html.Div([
        html.A(html.I(className="bi bi-youtube text-danger text-center", style={'font-size': '20px', 'margin': '10px'}),
               href="https://www.youtube.com/@DatawithElom", 
               target="_blank",
        ),
        
        html.A(html.I(className="bi bi-instagram text-danger text-center", style={'font-size': '20px', 'margin': '10px'}),
               href="http://instagram.com/data.with.elom",
               target="_blank", 
        ),
        
        html.A(html.I(className="bi bi-linkedin text-primary text-center", style={'font-size': '20px', 'margin': '10px'}),
               href="http://linkedin.com/in/elom-tettey-kwamin-frm®-53029468",
               target="_blank", 
        ),
           
    ], style={"display": "flex", "justify-content": "center", "align-items": "center"}), 

], 
justify='center')


# In[12]:


# Create references with a fixed footer style

socials_footer_section = dbc.Row([
    html.Div([
        html.A(html.I(className="bi bi-youtube text-danger text-center", style={'font-size': '20px', 'margin': '10px'}),
               href="https://www.youtube.com/@DatawithElom", 
               target="_blank",
        ),
        
        html.A(html.I(className="bi bi-instagram text-danger text-center", style={'font-size': '20px', 'margin': '10px'}),
               href="http://instagram.com/data.with.elom",
               target="_blank", 
        ),
        
        html.A(html.I(className="bi bi-linkedin text-primary text-center", style={'font-size': '20px', 'margin': '10px'}),
               href="http://linkedin.com/in/elom-tettey-kwamin-frm®-53029468",
               target="_blank", 
        ),
           
    ], style={"display": "flex", "justify-content": "center", "align-items": "center", "background-color": "#000000",
             "border": "0px royal blue", 'box-shadow': '12px 12px 12px 12px rgba(0, 0, 0, 0.2)', "padding": "10px"}), 

], 
justify='center')


# In[13]:


# header
header_section = html.Div([
        
        html.H1("Mortgage Comparison App", 
                style={"color":"white", 'fontWeight': 'bold'}, 
                className="text-center mt-3 mb-3"),
    
        socials_header_section,
        
        html.Div(style={"border-bottom": "10px groove black", "padding": "5px", }),     
], 
        
style={"background-color": "#000000", #8B0000
       "color": "white",
       "border": "0px royal blue",  # 2px border with black color
       'box-shadow': '12px 12px 12px 12px rgba(0, 0, 0, 0.2)',
       "padding": "10px"},

className="header")  # Use the "header" class for styling


# In[ ]:





# In[16]:


# Define language options
languages = [{'label': 'English', 'value': 'en'}, {'label': 'German', 'value': 'de'}]


# In[17]:


user_input_section = html.Div([
    
    dbc.Row([
        
        dbc.Col([
        
        # language selection
        html.Div([
                dcc.Dropdown(
                    id='language-select-dropdown',
                    options=languages,
                    value='en',
                    style={'width': '150px'}
                ),
                html.Div(id='language-output-content')
            
        ], style={'margin-left': '20px'})
            
            
        ], style={'display': 'flex', 'flexDirection': 'column', "padding": "10px",}),
        
    ]),
    
    # user input section
    dbc.Row([    
    
        dbc.Col([
            
            html.Div([
                
                html.H4(i18n.t('input_mask.mortgage_lender') + " 1", 
                        style={'text-align': 'center', 'fontWeight': 'bold', "color":"white"}, 
                        id='mortgage-lender-1-label'),
                
                dcc.Dropdown(id='mortgage-type-lender-1-select-dropdown',
                                     className='dropdown',
                                     style = {"color":"black"},
                                     multi=False,
                        ),
                
                html.Br(),
                
                # populate with selected mortgage mask - shown based on user selection
                html.Div(id = 'fixed-mortgage-input-mask-1'),
                
                # populate with selected mortgage mask - shown based on user selection
                html.Div(id = 'balloon-mortgage-input-mask-1'),
                  
            ], style={'margin-bottom': '20px', 'text-align': 'center', "border": "5px ridge silver",  # 2px border with black color
                            'box-shadow': '12px 12px 12px 12px rgba(0, 0, 0, 0.2)',
                            "padding": "10px", 
                            'background-color':'#36454F', #00008B #778899
                            "color": "white",
                            'align':'center', ##E5ECF6
                            }),
            
                # populate results of validation
                html.Div(id='validation-error-message-lender-1', style={"color":"white"}),
                html.Div(id='bm-validation-error-message-lender-1', style={"color":"white"}),
            
                # Hidden input component to store validated message
                dcc.Input(id='validated-message-lender-1', type='hidden'),
                dcc.Input(id='bm-validated-message-lender-1', type='hidden'),
            
                # store amortisation schedule key data for mortgage lender 1 - printed in output file
                dcc.Store(id="stored-amortisation-schedule-lender-1", storage_type="memory", data={}),
                dcc.Store(id="bm-stored-amortisation-schedule-lender-1", storage_type="memory", data={}),
            
                # store amortisation schedule details data for mortgage lender 1 - printed in output file
                dcc.Store(id="stored-amortisation-schedule-details-lender-1", storage_type="local", data={}),
                dcc.Store(id="bm-stored-amortisation-schedule-details-lender-1", storage_type="local", data={}),
            
        ], width=4, style={'display': 'flex', 'flexDirection': 'column', "padding": "10px",}),
        
        dbc.Col([
            
            html.Div([
                
                html.H4(i18n.t('input_mask.mortgage_lender') + " 2", 
                        style={'text-align': 'center', 'fontWeight': 'bold', "color":"white"}, 
                        id='mortgage-lender-2-label'),
                
                dcc.Dropdown(id='mortgage-type-lender-2-select-dropdown',
                                     className='dropdown',
                                     style = {"color":"black"},
                                     multi=False,
                                     value='Fixed-Rate-Mortgage'
                        ),
            
                html.Br(),

                # populate with selected mortgage mask - shown based on selected user input mask
                html.Div(id = 'fixed-mortgage-input-mask-2'),
                
                # populate with selected mortgage mask - shown based on selected user input mask
                html.Div(id = 'balloon-mortgage-input-mask-2')
                
            ], style={'margin-bottom': '20px', 'text-align': 'center', "border": "5px ridge silver",  # 2px border with black color
                            'box-shadow': '12px 12px 0px 0px rgba(0, 0, 0, 0.2)',
                            "padding": "10px", 
                            'background-color':'#36454F', #191970
                            "color": "white",
                            'align':'center'}),
            
                # populate results of validation
                html.Div(id='validation-error-message-lender-2', style={"color":"white"}),
            
                # Hidden input component to store validated message
                dcc.Input(id='validated-message-lender-2', type='hidden'),
            
                # store amortisation schedule data for mortgage lender 2
                dcc.Store(id="stored-amortisation-schedule-lender-2", storage_type="memory", data={}),
            
                # store amortisation schedule details data for mortgage lender 1
                dcc.Store(id="stored-amortisation-schedule-details-lender-2", storage_type="local", data={}),
            
 
        ], width=4, style={'display': 'flex', 'flexDirection': 'column', "padding": "10px",}),
            
    ], justify='center'),
    
    # compare button
    dbc.Row([
        
        dbc.Col([
            
            dbc.Button([html.I(className="fas fa-balance-scale"), i18n.t('input_mask.compare')], # Font Awesome icon for compare
                       size="md", 
                       color="primary", 
                       className="mx-auto", 
                       style={'padding': '10px', 'fontSize': '18px', 'width': '180px', 'height': '50px'},
                       id = ids.COMPARE_BUTTON),   
        ], width = 4, style={'textAlign': 'center'})
        
    ], justify='center'),
    
])


# In[ ]:





# In[19]:


tabs = html.Div(id='output-tabs') 


# In[20]:


results_section = html.Div([   
    
    html.Br(),
    
    html.Br(),
    
    dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        [html.I(className="fas fa-download"), i18n.t('input_mask.download')],
                        size="md",
                        color="primary",
                        className="mx-auto",
                        style={'padding': '10px', 'fontSize': '18px', 'width': '180px', 'height': '50px'},
                        id='download-button'
                    ),
                    
                     width = 10, style={'textAlign': 'right'}
                ),
            ]
        ),
    
    dcc.Download(id='download-amortisation-component'),
    
    html.Br(),
    
    dbc.Row([
        
        dbc.Col([tabs], lg={'size':8, 'offset':2}, sm=12)
    ]), 
])


# In[ ]:





# In[21]:


app.layout = html.Div([ 
    
    html.Div([
    
    header_section,
    
    html.Br(),
    
    user_input_section,
    
    results_section,
        
    html.Br(),
        
    html.Br(),
    
    socials_footer_section,
        
    ]),

], style={"background-color": "#708090", "position": "relative", "min-height": "100vh"} ) ##1E90FF, fluid=True,)


# In[ ]:





# In[22]:


# callback to setup internationalization

@app.callback(
   [Output('mortgage-lender-1-label', 'children'),
    Output('mortgage-lender-2-label', 'children'),
    Output(ids.COMPARE_BUTTON, 'children'),
    Output(ids.DOWNLOAD_BUTTON, 'children'),
#     Output('download-button', 'children'),
   ],
    Input('language-select-dropdown', 'value'),
    suppress_callback_exceptions=True
)
def update_language_mortgage_lender_header(selected_language):
    
    # Set the selected language
    if selected_language == 'de':
        LOCALE = "de"
        i18n.set('locale', selected_language)
        i18n.load_path.append("locale")

        updated_labels = [i18n.t('input_mask.mortgage_lender') + " 1 ",
                          i18n.t('input_mask.mortgage_lender') + " 2 ",
                          i18n.t('input_mask.compare'),
                          i18n.t('input_mask.download'),
                         ] 
        return updated_labels

    else:
        LOCALE = "en"
        i18n.set('locale', selected_language)
        i18n.load_path.append("locale")

        updated_labels = [i18n.t('input_mask.mortgage_lender') + " 1 ",
                          i18n.t('input_mask.mortgage_lender') + " 2 ",
                          i18n.t('input_mask.compare'),
                          i18n.t('input_mask.download'),
                         ] 
        return updated_labels
    


# In[ ]:





# In[23]:


@app.callback(
    Output('fixed-mortgage-input-mask-1', 'children'),
    Output('balloon-mortgage-input-mask-1', 'children'),
    Output('fixed-mortgage-input-mask-2', 'children'),
    Output('balloon-mortgage-input-mask-2', 'children'),
    Input('language-select-dropdown', 'value'),
)
def update_input_masks(selected_language):
    
    # Load translations for the selected language
    i18n.set('locale', selected_language)  

    fixed_mortgage_input_mask_1 = create_fixed_mortgage_input_mask('frm-mortgage-lender-1-input-mask', ids.FRM_LENDER_1_LOAN_AMOUNT, ids.FRM_LENDER_1_LOAN_AMOUNT_LABEL,
                                                   ids.FRM_LENDER_1_INTEREST_RATE, ids.FRM_LENDER_1_INTEREST_RATE_LABEL,
                                                   ids.FRM_LENDER_1_TERM, ids.FRM_LENDER_1_TERM_LABEL,
                                                   ids.FRM_LENDER_1_START_DATE, ids.FRM_LENDER_1_START_DATE_LABEL)

    fixed_mortgage_input_mask_2 = create_fixed_mortgage_input_mask('frm-mortgage-lender-2-input-mask', ids.FRM_LENDER_2_LOAN_AMOUNT, ids.FRM_LENDER_2_LOAN_AMOUNT_LABEL,
                                                   ids.FRM_LENDER_2_INTEREST_RATE, ids.FRM_LENDER_2_INTEREST_RATE_LABEL,
                                                   ids.FRM_LENDER_2_TERM, ids.FRM_LENDER_2_TERM_LABEL,
                                                   ids.FRM_LENDER_2_START_DATE, ids.FRM_LENDER_2_START_DATE_LABEL)

    balloon_mortgage_input_mask_1 = create_balloon_mortgage_input_mask('bm-mortgage-lender-1-input-mask', ids.BM_LENDER_1_LOAN_AMOUNT,
                                                   ids.BM_LENDER_1_INTEREST_RATE,
                                                   ids.BM_LENDER_1_TERM,
                                                   ids.BM_LENDER_1_BALLOON_PMT_AMOUNT,
                                                   ids.BM_LENDER_1_START_DATE, ids.BM_LENDER_1_START_DATE_LABEL)

    balloon_mortgage_input_mask_2 = create_balloon_mortgage_input_mask('bm-mortgage-lender-2-input-mask', ids.BM_LENDER_2_LOAN_AMOUNT,
                                                   ids.BM_LENDER_2_INTEREST_RATE,
                                                   ids.BM_LENDER_2_TERM,
                                                   ids.BM_LENDER_2_BALLOON_PMT_AMOUNT,
                                                   ids.BM_LENDER_2_START_DATE, ids.BM_LENDER_2_START_DATE_LABEL)
    
    return fixed_mortgage_input_mask_1, balloon_mortgage_input_mask_1, fixed_mortgage_input_mask_2, balloon_mortgage_input_mask_2


# In[ ]:





# In[24]:


@app.callback(
    Output('output-tabs', 'children'),
    Input('language-select-dropdown', 'value'),
)
def update_tabs(selected_language):
    # Load translations for the selected language
    i18n.set('locale', selected_language)
    
    updated_tabs = create_tabs()

    return updated_tabs


# In[25]:


@app.callback(
    Output('frm-mortgage-lender-1-input-mask', 'style'),
    Output('bm-mortgage-lender-1-input-mask', 'style'),
    [Input('mortgage-type-lender-1-select-dropdown', 'value'),
    Input('language-select-dropdown', 'value'),]
)
def toggle_mortgage_inputs_lender_1(mortgage_type, selected_language):
    
    i18n.set('locale', selected_language)
    i18n.load_path.append("locale")
    
    if mortgage_type == 'Fixed-Rate-Mortgage':
        return {'display': 'block'}, {'display': 'none'}
    elif mortgage_type == 'Balloon-Mortgage':
        return {'display': 'none'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'}


# In[26]:


@app.callback(
    Output('frm-mortgage-lender-2-input-mask', 'style'),
    Output('bm-mortgage-lender-2-input-mask', 'style'),
    [Input('mortgage-type-lender-2-select-dropdown', 'value'),
    Input('language-select-dropdown', 'value'),]
)
def toggle_mortgage_inputs_lender_2(mortgage_type, selected_language):
    
    i18n.set('locale', selected_language)
    i18n.load_path.append("locale")
    
    if mortgage_type == 'Fixed-Rate-Mortgage':
        return {'display': 'block'}, {'display': 'none'}
    elif mortgage_type == 'Balloon-Mortgage':
        return {'display': 'none'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'}


# In[ ]:





# In[27]:


# Update mortgage type dropdown options based on selected language
@app.callback(
    [Output('mortgage-type-lender-1-select-dropdown', 'options'),
     Output('mortgage-type-lender-1-select-dropdown', 'value'),
     Output('mortgage-type-lender-2-select-dropdown', 'options'),
     Output('mortgage-type-lender-2-select-dropdown', 'value')],
    Input('language-select-dropdown', 'value')
)
def update_mortgage_type_dropdown(selected_language):
    i18n.set('locale', selected_language)  # Set selected language
    i18n.load_path.append("locale")

    translated_options = [
        {'label': i18n.t('input_mask.fixed_rate_mortgage'), 'value': 'Fixed-Rate-Mortgage'},
        {'label': i18n.t('input_mask.balloon_mortgage'), 'value': 'Balloon-Mortgage'}
    ]
    
    # Set default value
    default_value = 'Fixed-Rate-Mortgage'

    return translated_options, default_value, translated_options, default_value


# In[29]:


@app.callback(
    [
        Output('validation-error-message-lender-1', 'children'),
        Output('datatable-container-mortgage-lender-1', 'children'),
        Output("stored-amortisation-schedule-lender-1", 'data'),
        Output("stored-amortisation-schedule-details-lender-1", 'data')
    ],
    [
        Input('compare-button', "n_clicks")
    ],
    [
        State('mortgage-type-lender-1-select-dropdown', "value"),
        State('frm-loan-amount-input-1', "value"),
        State('frm-interest-rate-input-1', "value"),
        State('frm-term-input-1', "value"),
        State('frm-start-date-input-1', "date"),
        State('bm-loan-amount-input-1', "value"),
        State('bm-interest-rate-input-1', "value"),
        State('bm-term-input-1', "value"),
        State('bm-balloon-pmt-amount-input-1', "value"),
        State('bm-start-date-input-1', "date")
    ],
    prevent_initial_call=True
)
def compute_schedule_lender_1(n_clicks, mortgage_type, *args):
    if n_clicks is None:
        raise PreventUpdate
    
    # Get the triggered input ID
    ctx = callback_context
    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_input == 'compare-button':
        selected_mortgage_type = mortgage_type
        
        # Check the selected mortgage type and process accordingly
        if selected_mortgage_type == 'Fixed-Rate-Mortgage':
            # Extract arguments for fixed-rate mortgage
            frm_loan_amount, frm_interest_rate, frm_term, frm_start_date = args[0:4]
            
            if None in [frm_loan_amount, frm_interest_rate, frm_term, frm_start_date]:
                raise PreventUpdate
            
            # Your logic for fixed-rate mortgage calculation
            
            try:
                input_data = {
                    'loan_amount': frm_loan_amount,
                    'interest_rate': frm_interest_rate,
                    'loan_term': frm_term,
                    'start_date': frm_start_date
                }

                FixedMortgageAmortizerInputValidation(**input_data)

                frm_start_date = pd.to_datetime(frm_start_date)
                fixed_rate_amortiser = FixedMortgageAmortizer('Mortgage Lender 1', frm_loan_amount, frm_interest_rate, 
                                                              frm_term, frm_start_date)
                schedule_df, key_info_df = fixed_rate_amortiser.generate_amortization_schedule()

                table_layout = create_schedule_table(schedule_df)

                return html.Div("Input validation successful!"), [table_layout], key_info_df.to_dict('records'), schedule_df.to_dict('records')

            except LoanAmountError as e:
                error_message = html.Div([html.Div(str(e))]), html.Div()
                return error_message, None, None, None

            except InterestAmountError as e:
                error_message = html.Div([html.Div(str(e))]), html.Div()
                return error_message, None, None, None

            except LoanTermError as e:
                error_message = html.Div([html.Div(str(e))]), html.Div()
                return error_message, None, None, None

            except ValidationError as e:
                error_message = html.Div([html.Div(f"Field: {error['loc'][0]}, Message: {error['msg']}") for error in e.errors()])
                return error_message, None, None, None

        elif selected_mortgage_type == 'Balloon-Mortgage':
            # Extract arguments for balloon mortgage
            bm_loan_amount, bm_interest_rate, bm_loan_term, bm_balloon_amount, bm_start_date = args[4:]
            
            if None in [bm_loan_amount, bm_interest_rate, bm_loan_term, bm_balloon_amount, bm_start_date]:
                raise PreventUpdate
            
            # Your logic for balloon mortgage calculation
            
            try:
                input_data = {
                    'loan_amount': bm_loan_amount,
                    'interest_rate': bm_interest_rate,
                    'loan_term': bm_loan_term,
                    'balloon_amount': bm_balloon_amount,
                    'start_date': bm_start_date
                }

                BalloonMortgageAmortizerInputValidation(**input_data)

                bm_start_date = pd.to_datetime(bm_start_date)
                balloon_amortiser = BalloonMortgageAmortizer('Mortgage Lender 1', bm_loan_amount, bm_interest_rate, 
                                                              bm_loan_term, bm_balloon_amount, bm_start_date)
                
                schedule_df, key_info_df = balloon_amortiser.generate_amortization_schedule()
                
                table_layout = create_schedule_table(schedule_df)

                return html.Div("Input validation successful!"), [table_layout], key_info_df.to_dict('records'), schedule_df.to_dict('records')
        
            except LoanAmountError as e:
                error_message = html.Div([html.Div(str(e))]), html.Div()
                return error_message, None, None, None
        
            except InterestAmountError as e:
                error_message = html.Div([html.Div(str(e))]), html.Div()
                return error_message, None, None, None

            except LoanTermError as e:
                error_message = html.Div([html.Div(str(e))]), html.Div()
                return error_message, None, None, None

            except ValidationError as e:
                error_message = html.Div([html.Div(f"Field: {error['loc'][0]}, Message: {error['msg']}") for error in e.errors()])
                return error_message, None, None, None

    else:
        raise PreventUpdate  # No other inputs triggered the callback


# In[30]:


@app.callback(
    [
        Output('validation-error-message-lender-2', 'children'),
        Output('datatable-container-mortgage-lender-2', 'children'),
        Output("stored-amortisation-schedule-lender-2", 'data'),
        Output("stored-amortisation-schedule-details-lender-2", 'data')
    ],
    [
        Input('compare-button', "n_clicks")
    ],
    [
        State('mortgage-type-lender-2-select-dropdown', "value"),
        State('frm-loan-amount-input-2', "value"),
        State('frm-interest-rate-input-2', "value"),
        State('frm-term-input-2', "value"),
        State('frm-start-date-input-2', "date"),
        State('bm-loan-amount-input-2', "value"),
        State('bm-interest-rate-input-2', "value"),
        State('bm-term-input-2', "value"),
        State('bm-balloon-pmt-amount-input-2', "value"),
        State('bm-start-date-input-2', "date")
    ],
    prevent_initial_call=True
)
def compute_schedule_lender_2(n_clicks, mortgage_type, *args):
    if n_clicks is None:
        raise PreventUpdate
    
    # Get the triggered input ID
    ctx = callback_context
    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_input == 'compare-button':
        selected_mortgage_type = mortgage_type
        
        # Check the selected mortgage type and process accordingly
        if selected_mortgage_type == 'Fixed-Rate-Mortgage':
            # Extract arguments for fixed-rate mortgage
            frm_loan_amount, frm_interest_rate, frm_term, frm_start_date = args[0:4]
            
            if None in [frm_loan_amount, frm_interest_rate, frm_term, frm_start_date]:
                raise PreventUpdate
            
            # Your logic for fixed-rate mortgage calculation
            
            try:
                input_data = {
                    'loan_amount': frm_loan_amount,
                    'interest_rate': frm_interest_rate,
                    'loan_term': frm_term,
                    'start_date': frm_start_date
                }

                FixedMortgageAmortizerInputValidation(**input_data)

                frm_start_date = pd.to_datetime(frm_start_date)
                fixed_rate_amortiser = FixedMortgageAmortizer('Mortgage Lender 2', frm_loan_amount, frm_interest_rate, 
                                                              frm_term, frm_start_date)
                schedule_df, key_info_df = fixed_rate_amortiser.generate_amortization_schedule()

                table_layout = create_schedule_table(schedule_df)

                return html.Div("Input validation successful!"), [table_layout], key_info_df.to_dict('records'), schedule_df.to_dict('records')

            except LoanAmountError as e:
                error_message = html.Div([html.Div(str(e))]), html.Div()
                return error_message, None, None, None

            except InterestAmountError as e:
                error_message = html.Div([html.Div(str(e))]), html.Div()
                return error_message, None, None, None

            except LoanTermError as e:
                error_message = html.Div([html.Div(str(e))]), html.Div()
                return error_message, None, None, None

            except ValidationError as e:
                error_message = html.Div([html.Div(f"Field: {error['loc'][0]}, Message: {error['msg']}") for error in e.errors()])
                return error_message, None, None, None

        elif selected_mortgage_type == 'Balloon-Mortgage':
            # Extract arguments for balloon mortgage
            bm_loan_amount, bm_interest_rate, bm_loan_term, bm_balloon_amount, bm_start_date = args[4:]
            
            if None in [bm_loan_amount, bm_interest_rate, bm_loan_term, bm_balloon_amount, bm_start_date]:
                raise PreventUpdate
            
            # Your logic for balloon mortgage calculation
            
            try:
                input_data = {
                    'loan_amount': bm_loan_amount,
                    'interest_rate': bm_interest_rate,
                    'loan_term': bm_loan_term,
                    'balloon_amount': bm_balloon_amount,
                    'start_date': bm_start_date
                }

                BalloonMortgageAmortizerInputValidation(**input_data)

                bm_start_date = pd.to_datetime(bm_start_date)
                balloon_amortiser = BalloonMortgageAmortizer('Mortgage Lender 2', bm_loan_amount, bm_interest_rate, 
                                                              bm_loan_term, bm_balloon_amount, bm_start_date)
                
                schedule_df, key_info_df = balloon_amortiser.generate_amortization_schedule()
                
                table_layout = create_schedule_table(schedule_df)

                return html.Div("Input validation successful!"), [table_layout], key_info_df.to_dict('records'), schedule_df.to_dict('records')
        
            except LoanAmountError as e:
                error_message = html.Div([html.Div(str(e))]), html.Div()
                return error_message, None, None, None
        
            except InterestAmountError as e:
                error_message = html.Div([html.Div(str(e))]), html.Div()
                return error_message, None, None, None

            except LoanTermError as e:
                error_message = html.Div([html.Div(str(e))]), html.Div()
                return error_message, None, None, None

            except ValidationError as e:
                error_message = html.Div([html.Div(f"Field: {error['loc'][0]}, Message: {error['msg']}") for error in e.errors()])
                return error_message, None, None, None

    else:
        raise PreventUpdate  # No other inputs triggered the callback


# In[ ]:





# In[34]:


# plot key information 


# In[35]:


@app.callback(
    Output('waterfall-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Output("radar-chart", 'figure'),
    Input('compare-button', "n_clicks"),
    State('stored-amortisation-schedule-lender-1', "data"),
    State('stored-amortisation-schedule-lender-2', "data"),
    prevent_initial_call=True
#     suppress_callback_exceptions=True
)

def update_comparison_charts(n_clicks, stored_data_lender_1, stored_data_lender_2):
        
    # Define the columns
    columns = ["Mortgage Lender", "Interest Rate", "Loan Amount", "Loan Term", "Monthly Payment",
              "Total Interest Paid", "Total Principal Paid", "Total Payment" ]

    # Create an empty DataFrame
    df = pd.DataFrame(columns=columns)
    
    if stored_data_lender_1 is not None:
        # Convert stored data to a DataFrame
        lender_1_df = pd.DataFrame(stored_data_lender_1)
        
        df = pd.concat([df, lender_1_df])
        
#         print('im in storage data lender 1')
        
#         print(df)
        
    if stored_data_lender_2 is not None:
        # Convert stored data to a DataFrame
        lender_2_df = pd.DataFrame(stored_data_lender_2)
        
        df = pd.concat([df, lender_2_df])
        
#         print('im in storage data lender 2')
        
#         print(df)
             
    # Create waterfall chart for comparison
    waterfall_chart = create_waterfall_chart(df)
    
    # Create pie chart for comparison
    pie_chart = create_pie_chart(df)
    
    # Create radar chart for Comparison of key metrics
    radar_chart = create_radar_chart(df)
    
    return waterfall_chart, pie_chart, radar_chart


# In[36]:


@app.callback(
    Output('download-amortisation-component', 'data'),
    State('stored-amortisation-schedule-lender-1', 'data'),
    State('stored-amortisation-schedule-details-lender-1', 'data'),
    State("stored-amortisation-schedule-lender-2", "data"),
    State('stored-amortisation-schedule-details-lender-2', 'data'),
    Input('download-button', 'n_clicks'),
    prevent_initial_call = True,
)


def download_amortisation(stored_amortisation_lender_1, stored_amortisation_details_lender_1,
                          stored_amortisation_lender_2, stored_amortisation_details_lender_2, 
                          n_clicks):
    if not n_clicks:
        raise PreventUpdate 
        
    # Convert stored data to DataFrames
    df_amortisation_lender_1 = pd.DataFrame(stored_amortisation_lender_1)  
    df_amortisation_lender_2 = pd.DataFrame(stored_amortisation_lender_2)
    df_stored_amortisation_details_lender_1 = pd.DataFrame(stored_amortisation_details_lender_1) 
    df_stored_amortisation_details_lender_2 = pd.DataFrame(stored_amortisation_details_lender_2) 

    # Create a summary DataFrame
    df_amortisation_summary = pd.concat([df_amortisation_lender_1, df_amortisation_lender_2], axis=0)
    
    # Create a dictionary of DataFrames
    dict_df_download = {'Summary': df_amortisation_summary, 
                        'Mortgage Lender 1': df_stored_amortisation_details_lender_1,
                        'Mortgage Lender 2': df_stored_amortisation_details_lender_2}
    
    # Create an Excel writer
    writer = pd.ExcelWriter("mortgage_comparison.xlsx", engine='xlsxwriter')
    
    # Iterate over the DataFrames and write to Excel
    for df_name , df in dict_df_download.items():
        df.to_excel(writer, sheet_name=df_name, index=False)
        
        # Get the worksheet
        worksheet = writer.sheets[df_name]
        
        # Insert the chart image if the worksheet is 'Summary'
        if df_name == 'Summary':
            worksheet.insert_image('B5', 'images\\waterfall_chart.png')
            worksheet.insert_image('J5', 'images\\radar_chart.png')
            worksheet.insert_image('B45', 'images\\pie_chart.png')

    # Save the Excel file
    writer.save()
    
    # Return the Excel file for download
    return dcc.send_file("mortgage_comparison.xlsx")   


# In[ ]:





# In[37]:


if __name__ == '__main__':
#     app.run_server(debug=True, mode='external', port=8095)
    app.run_server(debug=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




