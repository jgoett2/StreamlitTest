import streamlit as st
import pandas as pd
import numpy as np

st.title("CFP")

df = pd.read_csv("data.csv")
games = pd.read_csv("key.csv")

name_conversion = {None:"open"}

if "key" not in st.session_state:
  temp = games.set_index(games["Game"])
  st.session_state.key = pd.concat([temp.loc[temp["Team1_Victory"],"Team1"], temp.loc[temp["Team2_Victory"], "Team2"]]) 

st.session_state.key = st.session_state.key[st.session_state.key != "open"]

df["Wins"] = np.sum(df.eq(st.session_state.key), axis=1)
df["Losses"] = len(st.session_state.key) - df["Wins"]

# Simulate all possibe outcomes and total pathways to victory for each
open_games = games[~games.Game.isin(st.session_state.key.index)]

#open_games






## Jeff Test Code Speed
family_picks = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], dtype=np.uint32)
for i in range(0,18):
  family_picks[i+1] = 2**i 


pathways = np.zeros(19)

for key in range(0,2**0):
  results = ~(family_picks ^ np.uint32(key))
  total = np.zeros(19)
  for i in range(0,18):
    total += results % 2
    results = results >> 1
  winners = (total == max(total))
  if (winners[0]):
    print(key) 
  pathways += winners



df["Simulations_Won"] = 0

#open_games

#st.session_state.key






col1, col2 = st.columns(2)

with col1:
  df = df.sort_values(["Wins","Simulations_Won"], ascending=False)
  st.dataframe(df[["Name", "Wins", "Losses", "Simulations_Won"]], hide_index=True, height=480)


def callback_function(game):
    st.session_state.key[game] = name_conversion[st.session_state[game]]

with col2:
  for open_game in games[(games.Team1_Victory == False) & (games.Team2_Victory == False)].values:
    team1 = open_game[1].strip(" 0123456789.")
    team2 = open_game[3].strip(" 0123456789.")
    name_conversion[team1] = open_game[1]
    name_conversion[team2] = open_game[3]
    st.segmented_control(open_game[0], [team1, team2], key=open_game[0],  
           on_change=callback_function, kwargs={"game":open_game[0]})


