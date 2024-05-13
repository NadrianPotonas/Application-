

# Load the trained model
model = joblib.load("./artifacts/model_2.pkl")

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    style={'backgroundColor': '#f2f2f2', 'padding': '20px'},
    children=[
        html.H1("Loan Eligibility Predictor", style={'textAlign': 'center', 'fontSize': '36px', 'color': '#333333'}),
        html.Div(
            style={'margin-bottom': '20px'},
            children=[
                html.H2("Personal Information", style={'fontSize': '24px', 'color': '#333333'}),
                html.Div([
                    html.Label('Gender:', style={'fontSize': '18px'}),
                    dcc.Dropdown(
                        id='gender',
                        options=[
                            {'label': 'Male', 'value': 'Male'},
                            {'label': 'Female', 'value': 'Female'}
                        ],
                        value='Male',
                    ),
                ]),
                html.Div([
                    html.Label('Married:', style={'fontSize': '18px'}),
                    dcc.Dropdown(
                        id='married',
                        options=[
                            {'label': 'Yes', 'value': 'Yes'},
                            {'label': 'No', 'value': 'No'}
                        ],
                        value='Yes',
                    ),
                ]),
                html.Div([
                    html.Label('Dependents:', style={'fontSize': '18px'}),
                    dcc.Input(
                        id='dependents',
                        type='number',
                        value=0,
                    ),
                ]),
                html.Div([
                    html.Label('Education:', style={'fontSize': '18px'}),
                    dcc.Dropdown(
                        id='education',
                        options=[
                            {'label': 'Graduate', 'value': 'Graduate'},
                            {'label': 'Not Graduate', 'value': 'Not Graduate'}
                        ],
                        value='Graduate',
                    ),
                ]),
                html.Div([
                    html.Label('Self Employed:', style={'fontSize': '18px'}),
                    dcc.Dropdown(
                        id='self_employed',
                        options=[
                            {'label': 'Yes', 'value': 'Yes'},
                            {'label': 'No', 'value': 'No'}
                        ],
                        value='No',
                    ),
                ]),
            ],
        ),
        html.Div(
            style={'margin-bottom': '20px'},
            children=[
                html.H2("Financial Information", style={'fontSize': '24px', 'color': '#333333'}),
                html.Div([
                    html.Label('Applicant Income:', style={'fontSize': '18px'}),
                    dcc.Input(
                        id='applicant_income',
                        type='number',
                        value=5000,
                    ),
                ]),
                html.Div([
                    html.Label('Coapplicant Income:', style={'fontSize': '18px'}),
                    dcc.Input(
                        id='coapplicant_income',
                        type='number',
                        value=0,
                    ),
                ]),
                html.Div([
                    html.Label('Loan Amount:', style={'fontSize': '18px'}),
                    dcc.Input(
                        id='loan_amount',
                        type='number',
                        value=100000,
                    ),
                ]),
                html.Div([
                    html.Label('Loan Amount Term:', style={'fontSize': '18px'}),
                    dcc.Input(
                        id='loan_amount_term',
                        type='number',
                        value=360,
                    ),
                ]),
                html.Div([
                    html.Label('Credit History:', style={'fontSize': '18px'}),
                    dcc.Dropdown(
                        id='credit_history',
                        options=[
                            {'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0}
                        ],
                        value=1,
                    ),
                ]),
                html.Div([
                    html.Label('Property Area:', style={'fontSize': '18px'}),
                    dcc.Dropdown(
                        id='property_area',
                        options=[
                            {'label': 'Urban', 'value': 'Urban'},
                            {'label': 'Semiurban', 'value': 'Semiurban'},
                            {'label': 'Rural', 'value': 'Rural'}
                        ],
                        value='Urban',
                    ),
                ]),
            ],
        ),
        html.Button('Check Eligibility', id='submit-val', n_clicks=0, style={'width': '100%', 'fontSize': '20px'}),
        html.Div(id='output-state', style={'margin-top': '20px', 'fontSize': '24px', 'textAlign': 'center'})
    ]
)

# Define callback to predict loan eligibility
@app.callback(
    Output('output-state', 'children'),
    [
        Input('submit-val', 'n_clicks'),
        Input('gender', 'value'),
        Input('married', 'value'),
        Input('dependents', 'value'),
        Input('education', 'value'),
        Input('self_employed', 'value'),
        Input('applicant_income', 'value'),
        Input('coapplicant_income', 'value'),
        Input('loan_amount', 'value'),
        Input('loan_amount_term', 'value'),
        Input('credit_history', 'value'),
        Input('property_area', 'value'),
    ]
)
def update_output(n_clicks, gender, married, dependents, education, self_employed, applicant_income, coapplicant_income, loan_amount, loan_amount_term, credit_history, property_area):
    # Convert input values to appropriate data types
    dependents = str(dependents) if dependents is not None else None
    applicant_income = int(applicant_income) if applicant_income is not None else None
    coapplicant_income = int(coapplicant_income) if coapplicant_income is not None else None
    loan_amount = float(loan_amount) if loan_amount is not None else None
    loan_amount_term = float(loan_amount_term) if loan_amount_term is not None else None
    credit_history = float(credit_history) if credit_history is not None else None

    df = pd.DataFrame({
        'Gender': [gender],
        'Married': [married],
        'Dependents': [dependents],
        'Education': [education],
        'Self_Employed': [self_employed],
        'ApplicantIncome': [applicant_income],
        'CoapplicantIncome': [coapplicant_income],
        'LoanAmount': [loan_amount],
        'Loan_Amount_Term': [loan_amount_term],
        'Credit_History': [credit_history],
        'Property_Area': [property_area]
    })

    # Create 'Total_Income'
    df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']

    # Calculate 'Loan to Income Ratio'
    df['Loan_to_Income_Ratio'] = df['LoanAmount'] / df['Total_Income']

    # Loan_Percentage: Calculate the percentage of LoanAmount with respect to the TotalIncome
    df['Loan_Percentage'] = (df['LoanAmount'] / df['Total_Income']) * 100

    # Predict loan eligibility
    prediction = model.predict(df[['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Property_Area', 'Total_Income', 'Loan_to_Income_Ratio', 'Loan_Percentage']])


    if prediction[0] == 'Y':
        return html.Span('Congratulations! You are eligible for a loan.', style={'color': 'green'})
    else:
        return html.Span('Sorry! You are not eligible for a loan.', style={'color': 'red'})


if __name__ == '__main__':
    app.run_server(debug=True)
