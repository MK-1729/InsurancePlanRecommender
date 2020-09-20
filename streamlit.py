# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 21:58:46 2020

@author: Mohan
"""
import streamlit as st
import pandas as pd
import numpy as np
import time
import pickle



pickle_in = open("finalized_model_pp1.pkl","rb")
classifier_pp1=pickle.load(pickle_in)

pickle_in = open("finalized_model_pp2.pkl","rb")
classifier_pp2=pickle.load(pickle_in)

#def update_csv():
def savings(asy , fem):
    asm = asy/12 - fem 
    return asm 

def adjust_df_pp1(df,data):
    
    drop_p1 = ['Nationality_others', 'HighestEducation_PhD', 'HomeAddress_north_mal', 
           'ResidentialType_condominium', 'HomeAddress_east_mal', 'ResidentialType_bungalow', 
           'Occupation_employer']

    data['PurchasedPlan1'].replace(('SchoolAgain', 'COVIDFree', 'HomeSafe'), (1, 2, 3), inplace = True)
    
    
    # Drop the columns.
    data.drop(columns = ['PurchasedPlan1', 'PurchasedPlan2'], inplace = True)
    
    # Dummification
    X = pd.get_dummies(data)
    
    
    # Drop the columns.
    X.drop(columns = drop_p1, inplace = True) # Not optimized variables.
  
    value = list()
    value_cont = list()
    for i ,x in enumerate(df.columns): 
        if x in ['Age','MalaysiaPR','MovingToNewCompany','NoOfDependent','FamilyExpenses(month)','AnnualSalary','Saving(month)','MedicalComplication' ]:
              value_cont.append(df.iloc[0,i])
        else:
              str = df.columns[i] + '_' + df.iloc[0,i]
              value.append(str)
    value = [x for x in value if not(x in drop_p1)]    
    df = X.head(1).copy()
    df.values[:] =0
        
    for i in range(0,len(value_cont)):
         df.iloc[:,i] = value_cont[i]
    print(len(value))
    for i in range(0,len(value)):
        df.loc[:,value[i]]=1

    return df
    
def adjust_df_pp2(df, data):
    drop_p2 = ['Telco_celcom', 'LifeStyle_outdoor', 'SmokerStatus_sometimes', 
           'AgeGroup_18-26', 'HomeAddress_east_mal', 'Occupation_employer', 
           'HighestEducation_PhD']

    data['PurchasedPlan2'].replace(('NoMoneyDown', 'XEdu', 'KidsFlyUp'), (1, 2, 3), inplace = True)
    

    # Drop the columns.
    data.drop(columns = ['PurchasedPlan1', 'PurchasedPlan2'], inplace = True)
    
    # Dummification
    X = pd.get_dummies(data)
    
    
    # Drop the columns.
    X.drop(columns = drop_p2, inplace = True) # Not optimized variables.
    
    value = list()
    value_cont = list()

    for i ,x in enumerate(df.columns): 
        if x in ['Age','MalaysiaPR','MovingToNewCompany','NoOfDependent','FamilyExpenses(month)','AnnualSalary','Saving(month)','MedicalComplication' ]:
              value_cont.append(df.iloc[0,i])
              
        else:
              str = df.columns[i] + '_' + df.iloc[0,i]
              value.append(str)
    
     
    value = [x for x in value if not(x in drop_p2)]    
    df = X.head(1).copy()
    for col in df.columns:
        df[col].values[:] =0

    for i in range(0,len(value_cont)):
         df.iloc[:,i] = value_cont[i]
    print(len(value))
    for i in range(0,len(value)):
        df.loc[0:,value[i]]=1
    
    return df
    
    
def predict_pp1(df_pp1):
    
    df_pp1 = df_pp1.values
    prediction1  =classifier_pp1.predict(df_pp1) 
    if prediction1[0] == 1:
        return 'SchoolAgain'
    elif prediction1[0] ==2 :
        return 'COVIDFREE'
    else:
        return 'HomeSafe'

def predict_pp2(df_pp2):
    
    df_pp2 = df_pp2.values
    prediction2  =classifier_pp2.predict(df_pp2)
    
    if prediction2[0]==1:
        return 'NoMoneyDown'
    elif prediction2[0] ==2:
        return 'XEdu'
    else:
        return 'KidsFlyUp'


def main():
        st.title('Insurance Product Recommender')
        
        data = pd.read_csv('initial_preprocess.csv')
        
        
        AGE_MAX = 44
        AGE_MIN = 18
        DEPENDANT_MAX = 3
        DEPENDANT_MIN = 2
        ANNUAL_MAX = 199918 
        ANNUAL_MIN = 48127
        MAX_EXP= 10462
        MIN_EXP= 2514

        html_temp = """
        <div style="background-color:tomato;padding:10px">
        <h2 style="color:white;text-align:center;">Fill in your details and we'll find the best product for you! </h2>
        </div>
        """
        st.markdown(html_temp,unsafe_allow_html=True)
        age = st.number_input("Age")
        if age > AGE_MAX : AGE_MAX = age
        age = (age - AGE_MIN)/(AGE_MAX-AGE_MIN)
        
        if(age >=18 and age <=26):
            ageg = '18-26'
        elif (age >26 and age <= 36):
            ageg = '27-35'
        else:
            ageg = '36-44'
        
        gender = st.text_input("Gender","Type Here")
        if not gender in ['male', 'Male', 'female', 'Female']:
            st.write('either male or female')
            
        ms = st.text_input("MaritalStatus","Type Here")
        if not ms in ['single', 'married']:
            st.write('either single or married ')
        
        ss = st.text_input("SmokerStatus","Type Here")
        if not ss in ['frequent', 'once_in_a_while','sometimes']:
            st.write('either frequent , once_in_a_awhile or sometimes')
        
        ls = st.text_input("LifeStyle","Type Here")
        if not ls in ['home', 'outdoor','pub_goer']:
            st.write('home , outdoor or pub_goer')
        
        langS = st.text_input("LanguageSpoken","Type Here")
        if not langS in ['english', 'malay','mandarin']:
            st.write('either english,malay or mandarin ')
        
        
        he = st.text_input("HighestEducation","Type Here")
        if not he in ['Bachelor','Diploma', 'Master', 'PhD']:
            st.write('either Bachelors, Diploma, Master or PhD')
        
        race = st.text_input("Race","Type Here")
        if not race in ['malay', 'chinese','indian' , 'others']:
            st.write('either malay , chinese , indian or others ')
        
        
        nationality = st.text_input("Nationality","Type Here")
        if not nationality in ['Malaysian', 'others']:
            st.write('Malaysian or Others ')
        
        mpr = st.text_input("MalaysiaPR","Type Here")
        if mpr == 'yes' or mpr == 'Yes':
            mpr=1
        elif mpr == 'no' or mpr == 'No':
            mpr =0

            
        mtnc = st.text_input("MovingToNewCompany","Type Here")
        if mtnc == 'yes' or mtnc == 'Yes':
            mtnc =1 
        elif mtnc == 'no' or mtnc == 'No':
            mtnc =0

        occ = st.text_input("Occupation","Type Here")
        if not occ in ['employer', 'selfEmployed','privateEemployee', 'govServant']:
            st.write('either employer,selfEmployed,privateEemployee,govServant ')
            
        telco = st.text_input("Telco","Type Here")
        if not telco in ['maxis', 'umobile', 'celcom' ,'digi']:
            st.write('A plan that you are using like maxis, celcom, digi or umobile')
        
        ha = st.text_input("HomeAddress","Type Here")
        if not ha in ['north_mal' ,'east_mal', 'central_mal' ,'south_mal']:
            st.write('Which part of malaysia, in short write for example "south_mal"')
            
        rt = st.text_input("ResidentialType","Type Here")
        if not rt in ['terrace' ,'condominium' ,'flat' ,'bungalow']:
            st.write('either terrace , condominium , flat or bungalow')
        
        depend = st.number_input("NoOfDependent")
        if depend > DEPENDANT_MAX: DEPENDANT_MAX = depend
        depend = (depend-DEPENDANT_MIN)/(DEPENDANT_MAX-DEPENDANT_MIN)
        
        fe = st.number_input("FamilyExpenses(month)")
        if fe >MAX_EXP: fe = MAX_EXP;
        fe= (fe-MIN_EXP)/(MAX_EXP - MIN_EXP)
        
        ass = st.number_input("AnnualSalary")
        save = savings(ass,fe)
        if ass > ANNUAL_MAX: ANNUAL_MAX = ass
        ass = (ass-ANNUAL_MIN)/(ANNUAL_MAX-ANNUAL_MIN)
        
        cn1 = st.text_input("Customer_Needs_1","Type Here")
        if not cn1 in ['PersonalSaving' ,'PersonalRetirement' ,'PersonalMedical']:
            st.write('We have a variety of plans such as PersonalSaving, PersonalRetirement,PersonalMedical just for you')
            
        cn2 = st.text_input("Customer_Needs_2","Type Here")
        if not cn2 in ['KidMedical', 'KidSaving', 'KidEducation']:
            st.write('get a plan for your kid, choose from KidMedical,KidSaving or KidEducation ')
            
        t = st.text_input("Transport","Type Here")
        if not t in ['driving', 'publicTransport']:
            st.write('are you driving or taking publicTransport ')
            
        mc = st.text_input("MedicalComplication","Type Here")
        if mc == 'yes' or mc == 'Yes':
            mc = 1
        elif mc == 'no' or mc == 'No':
            mc = 0
        

        
        columns = ["Age","AgeGroup","Gender","MaritalStatus","SmokerStatus","LifeStyle","LanguageSpoken",
                   "HighestEducation","Race","Nationality","MalaysiaPR","MovingToNewCompany","Occupation",
                   "Telco","HomeAddress","ResidentialType","NoOfDependent","FamilyExpenses(month)","AnnualSalary",
                   "Saving(month)","Customer_Needs_1","Customer_Needs_2","Transport","MedicalComplication"]
        
        
        df = pd.DataFrame(data =np.array( [[age,ageg,gender,ms,ss,ls,langS,he,race,nationality,mpr,mtnc,occ,telco,ha,rt,depend,fe,ass,save,cn1,cn2,t,mc]]),
                     columns = columns)
        
        #for continous data
        #performing normalization on Age, AnnualSalary,FamilyExpenses(Month),NoOfDependent
        
        data['MalaysiaPR'].replace(('yes', 'no'), (1, 0), inplace = True)
        data['MovingToNewCompany'].replace(('yes', 'no'), (1, 0), inplace = True)
        data['MedicalComplication'].replace(('yes', 'no'), (1, 0), inplace = True)
        
       
        
        data_1 = data.copy()
        data_2 = data.copy()
        df_pp1 = adjust_df_pp1(df , data_1)
        #st.write(df_pp1)
        df_pp2 = adjust_df_pp2(df, data_2)
        #st.write(df_pp2)
        
        
        if st.button("Predict"):
            try:
                result1=predict_pp1(df_pp1)
                result2=predict_pp2(df_pp2)
                st.success('We recommend for your first choice {}'.format(result1))
                st.success('Highly recommended by our customers {}'.format(result2))
            except ValueError:
                st.write('Make sure all the boxes are filled in!')
            except:
                st.write('Something went wrong contact us to find out more.')
            

        if st.button("About"):
            st.text("Created by the team")
            st.text("Built with Streamlit")
        
        
        
        
if __name__ =='__main__':
           main()