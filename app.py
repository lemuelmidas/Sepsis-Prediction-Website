from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
#from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from pywebio.exceptions import SessionClosedException
import pandas as pd
import pickle
import warnings
import argparse



#app= Flask(__name__)

warnings.filterwarnings("ignore")


with open('rf_model.pkl', 'rb') as f:
    model= pickle.load(f)

with open('sepsis_columns.pkl', 'rb') as f:
    model_columns= pickle.load(f)

def prediction(prediction_df):
    model = pickle.load(open('rf_model.pkl', 'rb'))
    query= pd.DataFrame(prediction_df, index= [0])
    result=list(model.predict(query))
    final_result= round(result[0],3)

    return final_result

def values():
    #input_group("Sepsis Prediction")
    put_markdown(
    '''
    Sepsis Prediction Web App
    '''
    , lstrip=True
    )

    model_inputs= input_group(
            "Sepsis Prediction",
            [
                        input("Your PRG", name= 'PRG', type= FLOAT),
                        input("Your PL", name= 'PL', type= FLOAT),
                        input("Your PR", name= 'PR', type= FLOAT),
                        input("Your SK", name= 'SK', type= FLOAT),
                        input("Your TS", name= 'TS', type= FLOAT),
                        input("Your M11", name= 'M11', type= FLOAT),
                        input("Your BD2", name= 'BD2', type= FLOAT),
                        input("Your Age", name= 'age', type= FLOAT),
                        select("Insurance type", name='Insurance', options= [('0', 0), ('1', 1)]),

            ])

            prediction_df= pd.DataFrame(data= [[model_inputs[i] for i in ['PRG', 'PL', 'PR', 'SK', 'TS', 'M11', 'BD2', 'age', 'Insurance']]],
            columns= ['Your PRG', 'Your PL', 'Your PR', 'Your SK', 'Your TS', 'Your M11', 'Your BD2', 'Your age', 'Insurance type'])



            SepsisCategory= prediction(prediction_df)
            #prediction_text=''
            if SepsisCategory<=0:
                put_markdown("You have sepsis")

            else:
                put_markdown("No sepsis")


if __name__== "__main__":
    try:
        values()
    except SessionClosedException:
        print("The session was closed unexpectedly")
