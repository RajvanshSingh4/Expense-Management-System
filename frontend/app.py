import streamlit as st
from datetime import datetime
import requests
import time
import pandas as pd
from decouple import config


API_host = config('API_HOST', default='http://127.0.0.1:8000')
st.title('Expense Management System')
categories = ['Entertainment','Shopping','Food','Other','Rent']

tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics By Date", "Analytics By Month"])    #CREATING TABS

with tab1:       #THIS WILL ADD ELEMeNTS IN THE ADD/UPDATE PAGE
    selected_date = st.date_input('Enter Date', datetime(2024, 8, 1))    #ADDING A DATE INPUT FIELD
    response = requests.get(f"{API_host}/expenses/{selected_date}")

    if response.status_code == 200:
         existing_expenses = response.json()
    else:
        existing_expenses = []

    expenses = []

    # THIS WILL CREATE A FORM WiTH TABLE AND SUBMIT BUTTON
    with st.form(key="expense_form"):           #THE KEY HELPS UNIQULY IDENTIFY FORMS

        # This will create column headers
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Amount")
        with col2:
            st.subheader("Category")
        with col3:
            st.subheader("Notes")

        for i in range(5):
            if i < len(existing_expenses):
                amount, category, note = existing_expenses[i].values()
            else:
                amount = 0.0
                category = "Shopping"
                note = ""

            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input = st.number_input('Amount', min_value=0.0, step=1.0, value= amount, key=f'Amount{i + 1}', label_visibility='hidden')
            with col2:
               category_input = st.selectbox('Category', options= categories, index= categories.index(category), key= f'Category{i + 1}', label_visibility='hidden')
            with col3:
               notes_input = st.text_input('Notes', value= note, placeholder= "Add Note" ,key=f'Notes{i + 1}', label_visibility='hidden')


            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input,
            })


        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0.0 and  expense['category'] is not None]
            response = requests.post(f"{API_host}/expenses/{selected_date}", json= filtered_expenses)

            if response.status_code == 200:
                st.success(f"Expense(s) Added/Updated for {selected_date}")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Failed to Add/Update expenses for {selected_date}")


with tab2:
    with st.form(key="date_input_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Start Date")
        with col2:
            st.subheader("End Date")

        with col1:
            start_date = st.date_input('Enter Start Date', datetime(2024, 8, 1), label_visibility='hidden', key='StartDate')
        with col2:
            end_date = st.date_input('Enter End Date', datetime(2024, 8, 1), label_visibility='hidden', key='EndDate')

        submit = st.form_submit_button('Get Analytics')
        if submit:
            payload = {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
            }

            response = requests.post(f"{API_host}/analytics", json=payload)


            if response.status_code == 200:
                st.success(f"Fetched Summary from {start_date} - {end_date}")
                summary = response.json()
                df = pd.DataFrame({
                    'Category': [data['category'] for data in summary],
                    'Total': [data['total'] for data in summary],
                    'Percentage': [data['percentage'] for data in summary]
                })


                st.bar_chart(df, x='Category', y='Percentage', color= "#3888cf",  height=0, width= 0, use_container_width=True )

                df['Total'] = df['Total'].apply(lambda x: f"${x:.2f}")
                df['Percentage'] = df['Percentage'].apply(lambda x: f"{x:.2f}%")

                st.table(df)
            else:
                st.error(f"Failed to Fetch Summary from {start_date} - {end_date}")


with tab3:
    st.header("Expense Breakdown By Months")

    response = requests.get(f"{API_host}/monthly/analytics")

    if response.status_code == 200:
        summary = response.json()
        df = pd.DataFrame({
            'Number': [data['month_number'] for data in summary],
            'Month': [data['month_name'] for data in summary],
            'Total': [data['total'] for data in summary]
        })

        # Define month order
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']

        # Convert Month to categorical with proper order
        df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)

        df = df.sort_values('Number')

        st.bar_chart(df, x='Month', y='Total', color= "#3888cf",  height=0, width= 0, use_container_width=True )

        df['Total'] = df['Total'].apply(lambda x: f"${x:.2f}")
        st.table(df.set_index('Number'))
    else:
        st.error(f"Failed to Fetch Monthly Summary")










