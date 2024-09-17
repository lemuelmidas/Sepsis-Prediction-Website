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


    
    
with open('model_DC.pkl', 'rb') as f:
    model= pickle.load(f)

with open('columns.pkl', 'rb') as f:
    model_columns= pickle.load(f)
    
def prediction(prediction_df):
    model = pickle.load(open('model_DC.pkl', 'rb'))
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
        select("Visit", name='visit', options= [('One', 1), ('Two', 2), ('Three', 3), ('Four', 4), ('Five', 5)]),
        radio("What's your gender?", name='gender', options= [('Male', 1), ('Female', 0)]),
        input("Your Age", name= 'age', type= FLOAT),
        select("Hospital Outcome", name='outcome', options= [('Dead', 0), ('Alive', 1) ]),
    ])
    
    prediction_df= pd.DataFrame(data= [[model_inputs[i] for i in ['visit', 'gender', 'age', 'outcome']]],
                               columns= ['Visit', 'Your Gender', 'Age'])    
   
  
        
      
  
    
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
    
