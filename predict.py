from matplotlib.pyplot import sca
import streamlit as st
import numpy as np
import pandas as pd
import pickle

import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

file_id = '1DaAv2IkPBQyePQHWqNrgZ9H3iXlYzEwQ'
destination = 'pipeline.pkl'
download_file_from_google_drive(file_id, destination)


def load_model():
    data = pickle.load(open('pipeline.pkl', 'rb'))
    return data

data = load_model()

model = data['model']

def show_predict_page():
    html_temp_explore = """
    <div style ="background-color:rgb(60, 179, 113)";padding:10px">
    <h1 style="color:white;text-align:center;"> Batsman's Runs Prediction</h2>
    </div>
    """
    st.markdown(html_temp_explore,unsafe_allow_html=True)
    #st.title("Software Developer Salary Prediction")
    st.write('##')
    st.write("""### Enter the following Information to predict the runs""")
    Opponent = ('England', 'Sri Lanka', 'Pakistan', 'West Indies', 'South Africa',
       'Australia', 'Zimbabwe', 'New Zealand', 'U.A.E.', 'Bangladesh',
       'Kenya', 'Netherlands', 'Namibia', 'Bermuda', 'Ireland', 'India',
       'Canada', 'ICC World XI', 'Africa XI', 'Afghanistan', 'Scotland',
       'U.S.A.', 'Asia XI', 'Hong Kong', 'P.N.G.')

    Ground = ('Leeds', 'Nottingham', 'Nagpur', 'Pune', 'Margao', 'Cuttack',
       'Kolkata', 'Sharjah', 'Gwalior', 'New Delhi', 'Perth', 'Hobart',
       'Adelaide', 'Brisbane', 'Sydney', 'Melbourne', 'Hamilton',
       'Wellington', 'Dunedin', 'Harare', 'Cape Town', 'Port Elizabeth',
       'Centurion', 'Johannesburg', 'Bloemfontein', 'Durban',
       'East London', 'Jaipur', 'Chandigarh', 'Bengaluru', 'Jamshedpur',
       'Faridabad', 'Guwahati', 'Colombo (RPS)', 'Moratuwa', 'Kanpur',
       'Ahmedabad', 'Indore', 'Mohali', 'Rajkot', 'Hyderabad (Deccan)',
       'Jalandhar', 'Napier', 'Auckland', 'Christchurch', 'Colombo (SSC)',
       'Mumbai', 'Chennai', 'Vadodara', 'Delhi', 'Visakhapatnam',
       'Amritsar', 'Mumbai (BS)', 'Singapore', 'The Oval', 'Manchester',
       'Toronto', 'Paarl', 'Benoni', 'Bulawayo', 'Port of Spain',
       'Kingstown', 'Bridgetown', 'Hyderabad (Sind)', 'Karachi', 'Lahore',
       'Dhaka', 'Kochi', 'Taupo', 'Hove', 'Bristol', 'Taunton',
       'Birmingham', 'Galle', 'Nairobi (Gym)', 'Jodhpur', "Lord's",
       'Chester-le-Street', 'Pietermaritzburg', 'Rawalpindi', 'Peshawar',
       'Dambulla', 'Chattogram', 'Multan', 'Kuala Lumpur', 'Belfast',
       'Southampton', 'Canberra', 'Tangier', 'Kimberley',
       'Melbourne (Docklands)', 'Queenstown', 'Bogra', 'Amstelveen',
       'Providence', 'North Sound', "St George's", 'Kingston',
       'Colombo (PSS)', 'Gros Islet', 'Hambantota', 'Pallekele',
       'Dubai (DSC)', 'Abu Dhabi', 'Cardiff', 'Fatullah', 'Nelson',
       'Georgetown', 'Worcester', 'Potchefstroom', 'Cairns', 'Darwin',
       'Canterbury', 'Basseterre', 'Dublin', 'Sargodha', 'New Plymouth',
       'Ballarat', 'Kandy', 'Patna', 'Gujranwala', 'Faisalabad',
       'Nairobi (Club)', 'Northampton', 'Edinburgh', 'Ranchi',
       'Dharamsala', 'Thiruvananthapuram', 'Mount Maunganui', 'Sialkot',
       'Sheikhupura', 'Derby', "St John's", 'Chelmsford', 'Roseau',
       'Leicester', 'Vijayawada', 'Glasgow', 'Nairobi', 'King City (NW)',
       'Khulna', 'Whangarei', 'Berri', 'Nairobi (Aga)', 'Quetta',
       'Aberdeen', 'Dublin (Malahide)', 'Sylhet', 'Srinagar', 'Deventer',
       'Bready', 'Albion', 'Castries', 'Mombasa')
    
    opp = st.selectbox("Opposition",Opponent)
    gro = st.selectbox("Ground",Ground)

    career_runs = st.number_input("Total Career Runs", step=1, value=0)
    career_sr = st.number_input("Career Strike Rate", min_value=0.0, max_value=100.0, step=0.1, value=0.0)
    career_avg = st.number_input("Career Average", min_value=0.0, step=0.1, value=0.0)
    career_hundreds = st.slider("Career Hundreds", min_value=0, max_value=50, value=0, step=1)
    career_fifties = st.slider("Career Fifties", min_value=0, max_value=100, value=0, step=1)
    career_ducks = st.slider("Career Ducks", min_value=0, max_value=100, value=0, step=1)
    career_not_outs = st.slider("Career Not Outs", min_value=0, max_value=100, value=0, step=1)
    highest_score = st.number_input("Highest Score", min_value=0, step=1, value=0)

    Last_match_runs = st.number_input("Last Match Runs", step=1, value=0)
    Second_Last_match_runs = st.number_input("2nd Last Match Runs", step=1, value=0)
    Third_Last_match_runs = st.number_input("3rd Last Match Runs", step=1, value=0)
    Fourth_Last_match_runs = st.number_input("4th Last Match Runs", step=1, value=0)
    Fifth_Last_match_runs = st.number_input("5th Last Match Runs", step=1, value=0)

    button = st.button("Predict")
    if button:
        records = career_hundreds*20 + career_fifties*10 - career_ducks*5 + career_not_outs*5
        colnames = ['Total Runs', 'Ave', 'Career SR', 'HS', 'Opposition', 'Ground', 'm1', 'm2', 'm3', 'm4', 'm5', 'Records']
        un_scaled = [[career_runs, career_avg, career_sr, highest_score, opp, gro, Last_match_runs, Second_Last_match_runs, Third_Last_match_runs, Fourth_Last_match_runs, Fifth_Last_match_runs, records]]
        df = pd.DataFrame(data=un_scaled, columns=colnames)
        model = data['model']
        pred = model.predict(df)[0]
        if(pred == 6):
            st.header(f"The Predicted score is 100+")
        elif(pred == 5):
            st.header(f"The Predicted score is 80-100")
        elif(pred == 4):
            st.header(f"The Predicted score is 60-80")
        elif(pred == 3):
            st.header(f"The Predicted score is 40-60")
        elif(pred == 2):
            st.header(f"The Predicted score is 20-40")
        elif(pred == 1):
            st.header(f"The Predicted score is 0-20")