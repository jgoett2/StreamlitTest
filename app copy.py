import streamlit as st
import pandas as pd
import numpy as np

st.title("CFP")

df = pd.read_csv("data.csv")

key = pd.Series({"CFP_First_Round1": "2. Notre Dame"})

st.session_state.key = pd.Series({"Game1":"Notre Dame", "Game2":"Penn State"})

if "key" not in st.session_state:
  st.session_state.key = pd.Series({"Game1":"Notre Dame", "Game2":"Penn State"})

if "df" not in st.session_state:
  st.session_state.df = pd.DataFrame([{"Name":"Jeff", "Game1":"Notre Dame", "Game2":"Penn State"},
             {"Name":"Dave", "Game1":"Indiana", "Game2":"Penn State"} 
              ])

results = st.session_state.df.iloc[:,1:] == st.session_state.key
st.session_state.df["Wins"] = np.sum(results, axis=1)
st.session_state.df = st.session_state.df.sort_values(by="Wins", ascending=False)

data_window = st.dataframe(st.session_state.df[["Name", "Wins"]])

def callback_function1():
    #print(st.session_state.Game1)
    #st.session_state.key["Game1"] = st.session_state.Game1
    pass


st.radio("Game 1", ["Notre Dame", "Indiana", "open"], index=1, horizontal=True, on_change=callback_function1)

