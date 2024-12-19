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

open_games

def possible_outcome(completed_key, open_games, number):
  num = len(open_games.index)
  key = ('{0:0' + str(num) + 'b}').format(number)
  for i in list(zip(open_games.index, key)):
    if i[1] == "0":
      completed_key[open_games.loc[i[0],"Game"]] = open_games.loc[i[0],"Team2"]
    else:
      completed_key[open_games.loc[i[0],"Game"]] = open_games.loc[i[0],"Team1"] 
  return completed_key



def possible_outcome3(completed_key, open_games, number):
    for i in open_games.index:
      if (number & 2**i) > 0:
        completed_key[open_games.loc[i,'Game']] = open_games.loc[i,"Team1"]
      else:
        completed_key[open_games.loc[i,'Game']] = open_games.loc[i,"Team2"]
    return completed_key 

def run_simulation(df, completed_key, open_games):
  df["Simulations_Won"] = 0
  key = completed_key.copy(deep=True)
  open_games_temp = open_games.reset_index()
  for i in range(0,2**len(open_games)):
    if i%1000 == 0:
      print(i)
    possible_outcome2 = possible_outcome(key, open_games_temp, i)
    record = np.sum(df.eq(possible_outcome2, axis=1), axis=1)
    #print(i,record)
    df["Simulations_Won"] += (record == np.max(record))
  return df

## Jeff Test Code Speed
for i in range(0,2**19):
  total = 0
  grade = ~(np.uint32(2**18-1) ^ np.uint32(i))

  for j in range(0,18):
    total += grade % 2
    grade = grade >> 1


df["Simulations_Won"] = 0

open_games

st.session_state.key






col1, col2 = st.columns(2)

with col1:
  df = df.sort_values(["Wins","Simulations_Won"], ascending=False)
  st.dataframe(df[["Name", "Wins", "Losses", "Simulations_Won"]], hide_index=True)


def callback_function(game):
    #print(st.session_state.Game1)
    st.session_state.key[game] = name_conversion[st.session_state[game]]

with col2:
  for open_game in games[(games.Team1_Victory == False) & (games.Team2_Victory == False)].values:
    team1 = open_game[1].strip(" 0123456789.")
    team2 = open_game[3].strip(" 0123456789.")
    name_conversion[team1] = open_game[1]
    name_conversion[team2] = open_game[3]
    st.segmented_control(open_game[0], [team1, team2], key=open_game[0],  
           on_change=callback_function, kwargs={"game":open_game[0]})


