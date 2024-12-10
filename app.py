import streamlit as st
import pandas as pd
import numpy as np

st.title("CFP")


df = pd.read_csv("data.csv")

if "key" not in st.session_state:
  st.session_state.key = pd.Series({})

df["Wins"] = np.sum(df.eq(st.session_state.key), axis=1)
df["Losses"] = len(st.session_state.key) - df["Wins"] 
df = df.sort_values("Wins", ascending=False)

st.dataframe(df[["Name", "Wins", "Losses"]], hide_index=True)

def callback_function():
    #print(st.session_state.Game1)
    st.session_state.key["CFP_FirstRound1"] = st.session_state.CFP1
    pass

st.radio("CFP First Round 2 3", ["Blabama", "Indiana", "open"], key="CFP1", index=2, horizontal=True, on_change=callback_function)


