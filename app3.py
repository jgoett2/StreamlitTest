import streamlit as st
import numpy as np
import plotly.express as px

import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("data.csv")
games = pd.read_csv("key.csv")



name_conversion = {None:"open"}

temp = games.set_index(games["Game"])
key = pd.concat([temp.loc[temp["Team1_Victory"],"Team1"], temp.loc[temp["Team2_Victory"], "Team2"]]) 

key = key[key != "open"]

df["Wins"] = np.sum(df.eq(key), axis=1)
df["Losses"] = len(key) - df["Wins"]

# Simulate all possibe outcomes and total pathways to victory for each
open_games = games[~games.Game.isin(key.index)]



def calculate_pathways(df, key):
  open_games = [x for x in df.columns if x not in key.index]
  open_games = [x for x in open_games if x not in ["Name", "Wins", "Losses", "num", "Pathways_to_First", "Family"]]

  picks_binary = df[open_games].map(lambda x: int(x.split(".")[0])%2)
  powers_two = np.array([2**x for x in np.arange(len(open_games)-1, -1, -1)])
  df["num"] = (np.array(picks_binary.values)).dot(powers_two)

  family_picks = df["num"].to_numpy()
  pathways = np.zeros(len(df))
  scenarios = []

  for scenario in range(0,2**len(open_games)):
    total = df.Wins.to_numpy(copy=True)

    if (len(open_games)>0):
      results = ~(family_picks ^ np.uint32(scenario))
    
      for i in range(0,len(open_games)):
        total += results % 2
        results = results >> 1
    winners = (total == max(total))
    pathways += winners
    scenarios.append({"number":scenario, "winners":df.loc[winners, "Name"].values})
  
  df["Pathways_to_First"] = pathways
  df["Pathways_to_First"] = df["Pathways_to_First"].astype(int)
  df["Chance_of_Winning"] = df["Pathways_to_First"] / 2**len(open_games) * 100
  df["Chance_of_Winning"] = (df["Chance_of_Winning"]*10).astype(int)
  df["Chance_of_Winning"] = (df["Chance_of_Winning"]/10).astype(str) + "%"
  return (df, scenarios)


df, df1 = calculate_pathways(df, key)

df1 = pd.DataFrame(df1)
df1["David_Win"] = df1["winners"].map(lambda x: "David" in x)
df1["color"] = df1["winners"].map(lambda x: "blue" if "David" in x and len(x) == 1 else "lightsteelblue")

def count_distance(x):
  result = (356 ^ np.uint32(x))
  distance = 0
  for i in range(0,8):
    distance += result % 2
    result = result >> 1
  return distance

df1["distance"] = df1["number"].map(lambda x:count_distance(x))

for losses in df1["distance"].unique():
  temp_index = 0
  for i in df1[df1.distance==losses].index:
    df1.loc[i,"x"] = (temp_index % 3)*0.15 + df1.loc[i,"distance"]
    df1.loc[i,"y"] = (temp_index // 3)*0.1 + 0.1
    temp_index += 1



# Create distplot with custom bin_size
fig = px.scatter(df, x=df1["x"], y=df1["y"], color=df1["color"])

fig.update_xaxes(title_text='Losses')
fig.update_xaxes(range=[0,6])
fig.update_xaxes(tickvals=[0, 1, 2, 3, 4, 5, 6])

fig.update_yaxes(title_text='')

# Plot!
st.plotly_chart(fig, use_container_width=True)