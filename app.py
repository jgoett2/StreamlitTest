import streamlit as st
import pandas as pd
import numpy as np

st.title("CFP")

df = pd.read_csv("data.csv")

key = pd.Series({"CFP_First_Round1": "2. Notre Dame"})

df["Wins"] = np.sum(df.eq(key), axis=1)
df["Losses"] = len(key) - df["Wins"] 
df = df.sort_values("Wins", ascending=False)

st.dataframe(df[["Name", "Wins", "Losses"]], hide_index=True)

