import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from tensorflow.keras.models import load_model
import pandas as pd
import pdfplumber
import smtplib
from linker import bigboi
import PyPDF2
import os
import requests
import smtplib as s
from PIL import Image


# loading the saved models

# diabetes_model = pickle.load(open('C:\\Users\\nisha\\OneDrive\\Desktop\\projects\\Multiple diseases\\diabetes.sav','rb'))

heart_disease_model = pickle.load(open(r'heartdisease.pkl','rb'))

# kidney_disease_model = pickle.load(open('C:\\Users\\nisha\\OneDrive\\Desktop\\projects\\Multiple diseases\\kidneydisease.sav','rb'))





# sidebar for navigation
with st.sidebar:
    
    selected = option_menu('Multiple Disease Prediction System',
                          
                          ['Diabetes Prediction',
                           'Heart Disease Prediction',
                           'Chronic Kidney Disease Prediction','Mail Doctor',],
                          icons=['activity','heart','person','envelope','doctor'],
                          default_index=0)
    

name1 = ""
name2 = ""
diseases = []

invoice_pdf = open('blood_report1.pdf', 'rb')
with pdfplumber.open(invoice_pdf) as pdf:
    page1_name = pdf.pages[0]
    text1_name = page1_name.extract_text()
lines_name = text1_name.split('\n')
line_name = lines_name[4].split(' ')
name = line_name[1] + line_name[2]
#bigboi(name)

# Diabetes Prediction Page
if (selected == 'Diabetes Prediction'):
    
    # page title
    st.title('Diabetes Prediction')


    def main():
    
    
        st.title('Prediction')
        invoice_pdf = st.file_uploader("Choose a file",type='pdf')
        if invoice_pdf is not None:
        

            with pdfplumber.open(invoice_pdf) as pdf:
                page1 = pdf.pages[0]
                text1 = page1.extract_text()
                page2 = pdf.pages[1]
                text2 = page2.extract_text()

            lines1 = text1.split('\n')
            lines2 = text2.split("\n")

            for i in range(len(lines2)):
                lines1.append(lines2[i])

            def ocr(lines, columns):
                value = []
                for j in columns:
                    for i in lines[8:]:
                        i = i.split(' ')
                        if i[0] == j:
                            value.append(float(i[1]))
                return value
                
            columns1 = ['pregnancies', 'glucose', 'bloodpressure', 'skinthickness', 'insulin', 'BMI', 'diabetespredictionfunction', 'age']
            val = ocr(lines1, columns1)
            print(val)

            for i in range(len(val)):
                st.metric(label=columns1[i], value=val[i])
            for i in range(len(val)):
                columns1[i]=val[i]
            print(columns1)

        if st.button(label="Diabetes Test Result"):
            pred=model.predict([val])
            print(pred[0][0])
            if pred[0][0] > 0.5 :
                st.error("The Person is Diabetic")
                diseases.append("Diabetic")
            else:
                st.success("The Person is non-diabetic")

    if __name__== "__main__" :
        model= load_model("model.h5")
        main()
    
    
# Heart Disease Prediction Page


if (selected == 'Heart Disease Prediction'):
    
    # page title
    st.title('Heart Disease Prediction using ML')

    invoice_pdf = st.file_uploader("Choose a file",type='pdf')
    if invoice_pdf is not None:
        

        with pdfplumber.open(invoice_pdf) as pdf:
            page1 = pdf.pages[0]
            text1 = page1.extract_text()
            page2 = pdf.pages[1]
            text2 = page2.extract_text()

        lines3 = text1.split('\n')
        lines4 = text2.split("\n")

        for i in range(len(lines4)):
            lines3.append(lines4[i])

        def ocr(lines, columns):
            value = []
            for j in columns:
                for i in lines[8:]:
                    i = i.split(' ')
                    if i[0] == j:
                        value.append(float(i[1]))
            return value

        columns2 = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach','exang','oldpeak','slope','ca','thal']
        val = ocr(lines3, columns2)
        print(val)

        for i in range(len(val)):
            st.metric(label=columns2[i], value=val[i])
        for i in range(len(val)):
            columns2[i]=val[i]
        # print(columns)
         
     
    # code for Prediction
    heart_diagnosis = ''
    
    # creating a button for Prediction
    
    if st.button('Heart Disease Test Result'):
        heart_prediction = heart_disease_model.predict([val])                          
        
        if (heart_prediction[0] == 1):
            st.error("The person has heart disease")
            diseases.append("HeartDisease")
        #   heart_diagnosis = 'The person is having heart disease'
        else:
        #   heart_diagnosis = 'The person does not have any heart disease'
          st.success('The person does not have any heart disease')
        
    # st.success(heart_diagnosis)


# KIDNEY DISEASE

if (selected == 'Chronic Kidney Disease Prediction'):
    
#     # page title
    st.title('Chronic Kidney Disease Prediction')
    def main():
    
    
        st.title('Prediction')
        name = ""
        invoice_pdf = st.file_uploader("Choose a file",type='pdf')
        if invoice_pdf is not None:
        

            with pdfplumber.open(invoice_pdf) as pdf:
                page1 = pdf.pages[0]
                text1 = page1.extract_text()
                page2 = pdf.pages[1]
                text2 = page2.extract_text()

            lines = text1.split('\n')
            lines2 = text2.split("\n")

            for i in range(len(lines2)):
                lines.append(lines2[i])

            def ocr(lines, columns):
                value = []
                for j in columns:
                    for i in lines[8:]:
                        i = i.split(' ')
                        if i[0] == j:
                            value.append(float(i[1]))
                return value
            columns = ['sg', 'al', 'sc', 'hemo', 'pcv', 'wc', 'rc', 'htn']
            val = ocr(lines, columns)
            print(val)
            for i in range(len(val)):
                st.metric(label=columns[i], value=val[i])
            for i in range(len(val)):
                columns[i]=val[i]
            print(columns)
        
        

        if st.button(label="Chronic Kidney Disease Test Result"):
            pred=model.predict([val])
            # print(pred[0][0])
            if pred[0][0] == 1 :
                st.success("The person does not have any kidney disorder")
                
            else:
                st.error("The person has kidney disorder")
                diseases.append("ChronicKidneyDisease")
    if __name__== "__main__" :
        model= load_model("ckdmodel.h5")
        main()

                    
if (selected == 'Mail Doctor'):
    st.title("Email Sender")
    
        #st.image(img, width= 700)
    email_sender = st.text_input("Enter User Email-")
    password = st.text_input("Enter user password", type =  "password")
    email_receiver = st.text_input("Enter Receiver Email-")
    subject = st.text_input("Your email subject")
    body =  st.text_area("Your email")
    if st.button("Send email"):
        try:
            connection = s.SMTP("smtp.gmail.com",587)
            connection.starttls()
            connection.login(email_sender,password)
            body = "Subject:{}\n".format(subject,body)
            connection.sendmail(email_sender,email_receiver,body)
            connection.quit()
            st.success("Email sent successfully")
            #speak("Email sent successfully")
        except Exception as e:
            if email_sender == "":
                st.error("Please fill a mail- id")
                #speak("Please fill a mail- id")
            elif password =="":
                st.error("Please fill password field!")
                #("Please fill password field!")
            elif email_receiver == "":
                st.error("Please fill a mail- id")
                #("Please fill a mail- id")
            else:
                a = os.system("ping www.google.com")
            if a ==1:
                    st.error("Connect to the internet!")
                    #("Connect to the internet!")     
            else:
                    st.error("wrong password or mail-id!")


    