import joblib
import pandas as pd
import re
import streamlit as st

loaded_model = joblib.load('password_checker.pkl')

# Convart the 5 Column Funcation
def analyze_password(password):
    '''
    Analyzes a password and returns a dictionary containing various characteristics.
    '''
    password = str(password)
    
    result = {
        'length': len(password),
        'capital': sum(1 for char in password if char.isupper()),
        'small': sum(1 for char in password if char.islower()),
        'special': len(password) - len(re.findall('[\w]', password)),
        'numeric': sum(1 for char in password if char.isnumeric())
    }
    
    return result

def main():
    st.title("""Password Strenth checker App""")
    
    with st.form(key='myform', clear_on_submit=True):
        user_input = st.text_input("Enter your Password:")
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.info("**Prediction Result**")
        try:
            df = pd.DataFrame({"Password": [user_input]})
            df['password_analysis'] = df['Password'].apply(analyze_password)
            df = pd.concat([df, pd.DataFrame(df['password_analysis'].to_list())], axis=1)
            df = df.drop('password_analysis', axis=1)
            df.drop('Password', axis=1, inplace=True)
            prediction = loaded_model.predict(df)
            xy = prediction[0]
            abc = int(xy)
            if abc == 0:
                strength = "Weak"
            elif abc == 1:
                strength = "Medium"
            else:
               strength = "Strong" 
            st.write(f"**Your Password** => {strength}")
            #Deleted the dataframe
            del df
        except Exception as e:
            st.error(f"Error Password : {str(e)}")

if __name__ == "__main__":
    main()