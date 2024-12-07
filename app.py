import streamlit as st
import pandas as pd
import numpy as np

st.title("My Test App")

st.text_area(label="Your Question Here")

df = pd.DataFrame([{"name":"Jeff", "age":1},
                  {"name":"Dave", "age":2}])

st.table(data=df)

def call_back():
    df[df.Name=="Jeff", "age"] += 1

st.button("Hello!", on_click=call_back)