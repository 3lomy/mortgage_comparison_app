#!/usr/bin/env python
# coding: utf-8

# ### import required packages

# In[1]:


import pandas as pd
from datetime import datetime, timedelta, date
import calendar
import pandas as pd
import numpy_financial as npf


# In[2]:


from pydantic import BaseModel, ValidationError, field_validator


# In[3]:


### data input validation


# In[4]:


class LoanAmountError(Exception):
    
    def __init__(self, value, message):
        self.value = value
        self.message = message
        super().__init__(message)


# In[5]:


class InterestAmountError(Exception):
    
    def __init__(self, value, message):
        self.value = value
        self.message = message
        super().__init__(message)


# In[6]:


class TermError(Exception):
    
    def __init__(self, value, message):
        self.value = value
        self.message = message
        super().__init__(message)


# In[7]:


class BalloonAmountError(Exception):
    
    def __init__(self, value, message):
        self.value = value
        self.message = message
        super().__init__(message)


# In[ ]:





# In[8]:


class FixedMortgageAmortizerInputValidation(BaseModel):
    loan_amount: float
    interest_rate: float
    loan_term: float
    start_date: str  #date
        
        
    @field_validator("loan_amount")
    def validate_loan_amount(cls, value):
        if value <= 0:
            raise LoanAmountError(value= value, message = "Loan amount must be greater than zero")
            #raise LoanAmountError(value= value, message = "Field: loan_amount, Message: Loan amount must be greater than zero")
        return value
    
    @field_validator("interest_rate")
    def validate_interest_amount(cls, value):
        if value <= 0:
#             raise InterestAmountError(value= value, message = "Interest amount must be greater than zero")
              raise LoanAmountError(value= value, message = "Field: interest_amount, Message: Interest amount must be greater than zero")
        return value
    
    @field_validator("loan_term")
    def validate_term(cls, value):
        if value <= 0:
              raise TermError(value= value, message = "Field: loan_term, Message: Loan term must be greater than zero")
        return value
   


# In[20]:


# FixedMortgageAmortizerInputValidation(loan_amount=10, interest_rate=-2.5, 
#                                                              loan_term=20, start_date='2023-01-01')


# In[11]:


class BalloonMortgageAmortizerInputValidation(BaseModel):
    loan_amount: float
    interest_rate: float
    loan_term: float
    balloon_amount: float
    start_date: str  #date
        
        
    @field_validator("loan_amount")
    def validate_loan_amount(cls, value):
        if value <= 0:
            raise LoanAmountError(value= value, message = "Field: loan_amount, Message: Loan amount must be greater than zero")
        return value
    
    @field_validator("interest_rate")
    def validate_interest_amount(cls, value):
        if value <= 0:
            raise InterestAmountError(value= value, message = "Field: interest_amount, Message: Interest amount must be greater than zero")
            #raise LoanAmountError(value= value, message = "Field: loan_amount, Message: Loan amount must be greater than zero")
        return value
    
    @field_validator("loan_term")
    def validate_loan_term(cls, value):
        if value <= 0:
              raise LoanTermError(value= value, message = "Field: loan_term, Message: Loan term must be greater than zero")
        return value
    
    @field_validator("balloon_amount")
    def validate_balloon_amount(cls, value):
        if value <= 0:
              raise BalloonAmountError(value= value, message = "Field: balloon_amount, Message: Balloon amount must be greater than zero")
        return value


# In[24]:


# BalloonMortgageAmortizerInputValidation(loan_amount=10, interest_rate=2.5, 
#                                                              loan_term=20, balloon_amount=-10000, start_date='2023-01-01')


# In[ ]:





# In[12]:


class FixedMortgageAmortizer:

    def __init__(self, lender, loan_amount, initial_interest_rate, loan_term, start_date):
        # Constructor to initialize instance variables
        self.lender = lender
        self.loan_amount = loan_amount
        self.initial_interest_rate = initial_interest_rate
        self.loan_term = loan_term
        self.start_date = start_date

    def generate_amortization_schedule(self):
        # Number of payments
#         num_payments = self.loan_term * 12  # Assuming monthly payments
        num_payments = self.loan_term   # Assuming monthly payments and term in months
        
        data = [] 

        # Initialize lists to store schedule data
        payment_dates = []
        loan_balances = []
        principal_paid = []
        interest_paid = []
        total_payment = []  # Added for total payment

        # Initialize loan balance
        loan_balance = self.loan_amount

        # Loop through each payment period
        for i in range(num_payments):
            # Calculate monthly interest rate for the fixed-rate period
            monthly_interest_rate = self.initial_interest_rate / 12 / 100

            # Calculate monthly payment using the pmt function from numpy_financial
            monthly_payment = npf.pmt(monthly_interest_rate, num_payments - i, -loan_balance)

            # Calculate interest for the current period
            interest_payment = loan_balance * monthly_interest_rate

            # Calculate principal repayment for the current period
            principal_payment = monthly_payment - interest_payment

            # Update loan balance
            loan_balance -= principal_payment

            # Append data to lists
            payment_dates.append(self.start_date)
            loan_balances.append(loan_balance)
            principal_paid.append(principal_payment)
            interest_paid.append(interest_payment)

            # Calculate total payment
            total_payment.append(principal_payment + interest_payment)

            # Update date for the next payment
            self.start_date += pd.DateOffset(months=1)

        # Create a DataFrame for the amortization schedule
        amortization_schedule = pd.DataFrame({
            'Payment Date': payment_dates,
            'Loan Balance': loan_balances,
            'Principal Paid': principal_paid,
            'Interest Paid': interest_paid,
            'Total Payment': total_payment  # Added column for total payment
        })
        
        data.append(
        {
            "Mortgage Lender": self.lender,
            "Interest Rate": f"{self.initial_interest_rate}%",
            "Loan Amount": self.loan_amount,
            "Loan Term": self.loan_term,
            "Monthly Payment": amortization_schedule['Total Payment'][0],
            "Total Interest Paid": amortization_schedule['Interest Paid'].sum(),
            "Total Principal Paid": amortization_schedule['Principal Paid'].sum(),
            "Total Payment": amortization_schedule['Total Payment'].sum(),
        })
        
        df_key_info = pd.DataFrame(data)

        return amortization_schedule, df_key_info


# In[13]:


# # Example usage:
# loan_amount = 300000
# initial_interest_rate = 3.5
# loan_term = 30
# start_date = pd.to_datetime('2023-01-01')
# lender = 'Mortgage Lender 1'

# fixed_mortgage = FixedMortgageAmortizer(lender, loan_amount, initial_interest_rate, loan_term, start_date)
# schedule, key_info = fixed_mortgage.generate_amortization_schedule()

# schedule

# key_info


# In[ ]:





# In[14]:


class BalloonMortgageAmortizer:

    def __init__(self, lender, loan_amount, initial_interest_rate, loan_term, balloon_amount, start_date):
        # Constructor to initialize instance variables
        self.lender = lender
        self.loan_amount = loan_amount
        self.initial_interest_rate = initial_interest_rate
        self.loan_term = loan_term
        self.balloon_amount = balloon_amount
        self.start_date = start_date
        
        
    def generate_amortization_schedule(self):
        # Convert annual rate to monthly rate
        monthly_rate = self.initial_interest_rate / 12 / 100
        loan_balance = self.loan_amount
        balloon_amount = self.balloon_amount
        term_months = self.loan_term
        date = self.start_date
        
        data = [] 

        # Calculate monthly payment (without considering balloon payment)
        monthly_payment = (loan_balance * monthly_rate) / (1 - (1 + monthly_rate) ** -term_months)

        # Initialize variables
        amortization_schedule = []
        balance = loan_balance
        

        # Generate amortization schedule
        for month in range(1, term_months + 1):
            days_in_month = calendar.monthrange(date.year, date.month)[1]
            interest_payment = balance * monthly_rate 

            if month == term_months:
                principal_payment = balance  # Pay off the remaining balance
                balance = 0  # Set balance to zero after paying off the loan
            else:
                principal_payment = monthly_payment - interest_payment
                balance -= principal_payment

            amortization_schedule.append({
                'Payment Date': date,
                'Loan Balance': balance + principal_payment,
                'Principal Paid': principal_payment,
                'Interest Paid': interest_payment,
                'Total Payment': monthly_payment if month < term_months else monthly_payment + balloon_amount
#                 'Ending Balance': balance
            })

            # Increment the date by one month
            date += timedelta(days=days_in_month)

        df = pd.DataFrame(amortization_schedule)               
        
        data.append(
        {
            "Mortgage Lender": self.lender,
            "Interest Rate": f"{self.initial_interest_rate}%",
            "Loan Amount": self.loan_amount,
            "Loan Term": self.loan_term,
            "Monthly Payment": df['Total Payment'][0],
            "Total Interest Paid": df['Interest Paid'].sum(),
            "Total Principal Paid": df['Principal Paid'].sum(),
            "Total Payment": df['Total Payment'].sum(),
        })
        
        df_key_info = pd.DataFrame(data)

        return df, df_key_info


# In[15]:


# # Example usage:
# loan_amount = 300000
# initial_interest_rate = 3.5
# loan_term = 30
# balloon_amount = 100000
# start_date = pd.to_datetime('2023-01-01')
# lender = 'Mortgage Lender 1'

# balloon_mortgage = BalloonMortgageAmortizer(lender, loan_amount, initial_interest_rate, loan_term, balloon_amount, start_date)
# balloon_schedule, balloon_key_info = balloon_mortgage.generate_amortisation_schedule()

# balloon_schedule

# balloon_key_info

