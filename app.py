import streamlit as st
import pandas as pd
import numpy as np

st.title("My Test App")

if "key" not in st.session_state:
  st.session_state.key = {"Game1":"Notre Dame", "Game2":"Penn State"}

df = pd.DataFrame([{"Name":"Jeff", "Game1":"Notre Dame", "Game2":"Penn State"},
             {"Name":"Dave", "Game1":"Indiana", "Game2":"Penn State"} 
              ])

results = df.iloc[:,1:] == st.session_state.key
df["Wins"] = np.sum(results, axis=1)

data_window = st.dataframe(df[["Name", "Wins"]])

def callback_function1():
    st.session_state.key["Game1"] = "Notre Dame"

def callback_function2():
    st.session_state.key["Game1"] = "Indiana"


st.button("Notre Dame Wins", on_click=callback_function1)
st.button("Indiana Wins", on_click=callback_function2)
