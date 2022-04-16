import streamlit as st
import pickle
import numpy as np
import pandas as pd
import sklearn

model = pickle.load(open('prediction_model.p', 'rb'))



def main():
    
    # Batch Upload Prediction

    st.title('Salary Prediction')
    option = st.selectbox('How would you like to predict the salary of Data Scientists?', ('Manual Input', 'Batch Upload'))

    if option == 'Batch Upload':
        data_file = st.file_uploader('Upload processed data file', type = ['csv', 'xlsx'])
        if data_file is not None:
            df = pd.read_csv(data_file)
            df = df.drop(df[df.type_of_ownership == 'Nonprofit Organization'].index)
            st.dataframe(df)
            df_model = df[['rating', 'company_size', 'type_of_ownership', 'industry', 'revenue', 'hourly', 'employer_provided', 'job_state', 'age', 'tool_python', 'tool_r_studio', 'tool_spark', 'tool_aws', 'tool_excel', 'tool_matlab', 'tool_tableau', 'tool_powerbi', 'tool_sql', 'job_simplified', 'seniority', 'avg_salary']]
            df_dummy = pd.get_dummies(df_model)
            final_df = df_dummy.drop('avg_salary', axis = 1)
            if st.button('Predict'):
                predicted_salary = model.predict(final_df)
                predicted_salary = pd.DataFrame(predicted_salary, columns = ['Predicted Salary'])
                final_df = pd.concat([df_model, predicted_salary], axis = 1)
                final_df = pd.concat([df.loc[:, 'job_title'], final_df], axis = 1)
                final_df['Percent Diff'] = (final_df['Predicted Salary'] - final_df['avg_salary']) / final_df['Predicted Salary'] * 100
                st.write(final_df)
        else:
            st.write('No data file chosen.')
         
    # Manual Input Prediction
    else:
        rating = st.slider('Company Rating (default -1.0 as Unknown)', min_value = -1.0, max_value = 5.0, step = 0.1)
        company_size = st.selectbox('Company Size', ("1+", "51+", "201+", "501+", "1001+", "5001+", "10000+", "Unknown"))
        st.caption('Description: \n - 1+: 1 to 50 Employees\n - 51+: 51 to 200 Employees\n- 201+: 201 to 500 Employees\n - 501+: 501 to 1000 Employees\n - 1001+: 1000 to 5000 Employees\n - 5001+: 5001 to 10000 Employees\n - 10000+: Over 10000 Employees')
        type_of_ownership = st.selectbox('Type of ownership', ('Company - Public', 'Company - Private', 'Subsidiary or Business Segment', 'Government', 'College / University', 'Contract', 'Unknown'))
        industry = st.selectbox('Industry (default -1 as Unknown)', ('-1', 'Investment Banking & Asset Management', 'Internet',
       'Computer Hardware & Software', 'Staffing & Outsourcing',
       'Energy', 'Enterprise Software & Network Solutions', 'Lending',
       'IT Services', 'Travel Agencies',
       'Financial Transaction Processing',
       'Consumer Products Manufacturing',
       'Transportation Equipment Manufacturing', 'Video Games',
       'Colleges & Universities', 'Insurance Carriers',
       'Health Care Services & Hospitals', 'Federal Agencies',
       'Biotech & Pharmaceuticals', 'Gas Stations', 'Aerospace & Defense',
       'Gambling', 'TV Broadcast & Cable Networks',
       'Insurance Agencies & Brokerages', 'Real Estate',
       'Financial Analytics & Research', 'Food & Beverage Manufacturing',
       'Advertising & Marketing', 'Department, Clothing, & Shoe Stores',
       'Brokerage Services', 'Grocery Stores & Supermarkets',
       'Telecommunications Services',
       'Motion Picture Production & Distribution', 'Sports & Recreation',
       'Audiovisual', 'Oil & Gas Services'))
        
        revenue = st.selectbox('Company Revenue', ('-1', '$50 to $100 million ', 'Unknown / Non-Applicable', 'Less than $1 million ', '$100 to $500 million ',
       '$2 to $5 billion ', '$10 to $25 million ', '$5 to $10 million ',
       '$25 to $50 million ', '$10+ billion ',
       '$500 million to $1 billion ', '$1 to $5 million ',
       '$5 to $10 billion ', '$1 to $2 billion '))

        hourly = 0
        hourly_wage = st.radio('Hourly Wage', ('Yes', 'No'))
        if hourly_wage == 'Yes':
            hourly = 1
        else:
            hourly = 0
            
        employer_provided = 0
        employer_wage = st.radio('Employer Provided Wage', ('Yes', 'No'))
        if employer_wage == 'Yes':
            employer_provided = 1
        else:
            employer_provided = 0
        
        age = st.slider('Company age (default -1 as Unknown)', -1, 200, 1)
        
        tool = st.multiselect('Tools and Technologies', ['python', 'r_studio', 'spark', 'aws', 'excel', 'matlab', 'tableau', 'powerbi', 'sql'])

        job_simplified = st.selectbox('Choose job title', ('na', 'data scientist', 'machine learning engineer', 'manager', 'data engineer', 'director'))
        seniority = st.selectbox('Choose experience level', ('na', 'junior', 'senior', 'entry'))
        
        job_state = st.selectbox('Choose job state', ('CA', 'TN', 'GA', 'Remote', 'FL', 'MA', 'NJ', 'VT', 'VA', 'CO', 'NY', 'MO', 'TX', 'OR', 'KY', 'MD', 'ME', 'WA', 'AZ', 'LA', 'NC', 'NV', 'IL', 'Unknown', 'DC', 'PA'))
        
        predict = pd.DataFrame([{
            'rating': rating,
            'hourly': hourly,
            'employer_provided': employer_provided,
            'age': age,
            'tool': tool,
            'company_size': company_size,
            'type_of_ownership': type_of_ownership,
            'industry': industry,
            'revenue': revenue,
            'job_state': job_state,
            'job_simplified': job_simplified,
            'seniority': seniority,
            
        }])
        # for i in tool:
        #     predict['tool_{}'.format(i)] = 1
        tool_list = ['python', 'r_studio', 'spark', 'aws', 'excel', 'matlab', 'tableau', 'powerbi', 'sql']
        for x in tool_list:
            if x in tool:
                predict['tool_{}'.format(x)] = 1
                # st.write(x)
            else:
                predict['tool_{}'.format(x)] = 0
        size_list = ['1+', '10000+', '1001+', '201+', '5001+', '501+', '51+', 'Unknown']
        for x in size_list:
            if x == company_size:
                predict['company_size_{}'.format(x)] = 1
            else:
                predict['company_size_{}'.format(x)] = 0
                
        ownership_list = ['College / University', 'Company - Private', 'Company - Public', 'Contract', 'Government', 'Subsidiary or Business Segment', 'Unknown']
        for x in ownership_list:
            if x == type_of_ownership:
                predict['type_of_ownership_{}'.format(x)] = 1
            else:
                predict['type_of_ownership_{}'.format(x)] = 0
                
        industry_list = ['-1', 'Advertising & Marketing', 'Aerospace & Defense', 'Audiovisual', 'Biotech & Pharmaceuticals', 'Brokerage Services', 'Colleges & Universities', 'Computer Hardware & Software', 'Consumer Products Manufacturing', 'Department, Clothing, & Shoe Stores', 'Energy', 'Enterprise Software & Network Solutions', 'Federal Agencies', 'Financial Analytics & Research', 'Financial Transaction Processing', 'Food & Beverage Manufacturing', 'Gambling', 'Gas Stations', 'Grocery Stores & Supermarkets', 'Health Care Services & Hospitals', 'IT Services', 'Insurance Agencies & Brokerages', 'Insurance Carriers', 'Internet', 'Investment Banking & Asset Management', 'Lending', 'Motion Picture Production & Distribution', 'Oil & Gas Services', 'Real Estate', 'Sports & Recreation', 'Staffing & Outsourcing', 'TV Broadcast & Cable Networks', 'Telecommunications Services', 'Transportation Equipment Manufacturing', 'Travel Agencies', 'Video Games']   
        for x in industry_list:
            if x == industry:
                predict['industry_{}'.format(x)] = 1
            else:
                predict['industry_{}'.format(x)] = 0
                
        revenue_list = ['$1 to $2 billion ', '$1 to $5 million ', '$10 to $25 million ', '$10+ billion ', '$100 to $500 million ', '$2 to $5 billion ', '$25 to $50 million ', '$5 to $10 billion ', '$5 to $10 million ', '$50 to $100 million ', '$500 million to $1 billion ', '-1', 'Less than $1 million ', 'Unknown / Non-Applicable']
        for x in revenue_list:
            if x == revenue:
                predict['revenue_{}'.format(x)] = 1
            else:
                predict['revenue_{}'.format(x)] = 0
                
        state_list = ['AZ', 'CA', 'CO', 'DC', 'FL', 'GA', 'IL', 'KY', 'LA', 'MA', 'MD', 'ME', 'MO', 'NC', 'NJ', 'NV', 'NY', 'OR', 'PA', 'Remote', 'TN', 'TX', 'Unknown', 'VA', 'VT', 'WA']
        for x in state_list:
            if x == job_state:
                predict['job_state_{}'.format(x)] = 1
            else:
                predict['job_state_{}'.format(x)] = 0
        
        title_list = ['data engineer', 'data scientist', 'director', 'machine learning engineer', 'manager', 'na']
        for x in title_list:
            if x == job_simplified:
                predict['job_simplified_{}'.format(x)] = 1
            else:
                predict['job_simplified_{}'.format(x)] = 0
                
        experience_list = ['entry', 'junior', 'na', 'senior']
        for x in experience_list:
            if x == seniority:
                predict['seniority_{}'.format(x)] = 1
            else:
                predict['seniority_{}'.format(x)] = 0
        
        predict = predict.drop(['tool', 'company_size', 'type_of_ownership', 'industry', 'revenue', 'job_state', 'job_simplified', 'seniority'], axis = 1)
        
        # st.write(predict)

        # predict = predict.drop('tool', axis = 1)
        # dummy_df = pd.get_dummies(predict)
        # st.write(dummy_df)
        if st.button('Predict'):
            result = model.predict(predict)
            st.success('The salary for this position is: {} dollars.'.format(round(float(result), 2)))
    

if __name__ == '__main__':
    main()
