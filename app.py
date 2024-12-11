import streamlit as st
import pandas as pd
import numpy as np

st.title("CFP")

df = pd.read_csv("data.csv")

name_conversion = {None:"open", "Indiana":"1. Indiana", "Notre Dame":"2. Notre Dame"}

if "key" not in st.session_state:
  st.session_state.key = pd.Series({})

df["Wins"] = np.sum(df.eq(st.session_state.key), axis=1)
df["Losses"] = np.sum(st.session_state.key != "open") - df["Wins"] 
df = df.sort_values("Wins", ascending=False)

st.dataframe(df[["Name", "Wins", "Losses"]], hide_index=True)


def callback_function():
    #print(st.session_state.Game1)
    st.session_state.key["CFP_First_Round1"] = name_conversion[st.session_state.CFP1]
    
for i in range(0,10):
  st.segmented_control("CFP", ["Indiana", "Notre Dame"], key="CFP"+str(i),  
           on_change=callback_function)


