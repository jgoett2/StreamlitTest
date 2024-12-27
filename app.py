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



def calculate_pathways(df, key):
  open_games = [x for x in df.columns if x not in key.index]
  open_games = [x for x in open_games if x not in ["Name", "Wins", "Losses", "num", "Pathways_to_First"]]

  picks_binary = df[open_games].map(lambda x: int(x.split(".")[0])%2)
  powers_two = np.array([2**x for x in np.arange(len(open_games)-1, -1, -1)])
  df["num"] = (np.array(picks_binary.values)).dot(powers_two)

  family_picks = df["num"].to_numpy()
  pathways = np.zeros(len(df))

  for scenario in range(0,2**len(open_games)):
    total = df.Wins.to_numpy(copy=True)

    if (len(open_games)>0):
      results = ~(family_picks ^ np.uint32(scenario))
    
      for i in range(0,len(open_games)):
        total += results % 2
        results = results >> 1
    winners = (total == max(total))
    pathways += winners
  
  df["Pathways_to_First"] = pathways
  df["Pathways_to_First"] = df["Pathways_to_First"].astype(int)
  df["Chance_of_Winning"] = df["Pathways_to_First"] / 2**len(open_games) * 100
  df["Chance_of_Winning"] = (df["Chance_of_Winning"]*10).astype(int)
  df["Chance_of_Winning"] = (df["Chance_of_Winning"]/10).astype(str) + "%"
  return df


df = calculate_pathways(df, st.session_state.key)





col1, col2 = st.columns(2)

with col1:
  df = df.sort_values(["Wins","Pathways_to_First"], ascending=False)
  st.dataframe(df[["Name", "Wins", "Losses", "Pathways_to_First", "Chance_of_Winning"]], hide_index=True, height=40*len(df))


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


