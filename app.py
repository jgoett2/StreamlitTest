import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("CFP")

df = pd.read_csv("data.csv")
games = pd.read_csv("key.csv")


family = st.selectbox(
    "Family:",
    np.insert(df["Family"].unique(), 0, "Everyone")
)

if family != "Everyone":
  df = df[df["Family"]==family]



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
  return df, scenarios


df, scenarios = calculate_pathways(df, st.session_state.key)


#Experimental
df = df.sort_values(["Wins","Pathways_to_First"], ascending=False)

name_detail = df["Name"].unique()[0]

scenarios = pd.DataFrame(scenarios)


scenarios["Win1"] = scenarios["number"] & 4


def get_status(name_detail, x):
  if name_detail in x and len(x) == 1:
    return "win_outright"
  elif name_detail in x and len(x) > 1:
    return "tie"
  else:
    return "lost"

scenarios["status"] = scenarios["winners"].map(lambda x: get_status(name_detail, x))

i = len(open_games)-1
scenarios["teams"] = ""
for y in open_games.values:
  number = 2**i
  scenarios["teams"] += scenarios["number"].map(lambda x: (y[1] + ", ") if ((x & number) > 0) else (y[3] + ", "))
  i -= 1
  

def count_distance(x, player_binary, losses):
  result = (player_binary ^ np.uint32(x))
  distance = 0
  for i in range(0,len(open_games)):
    distance += result % 2
    result = result >> 1
  return distance + losses

scenarios["distance"] = scenarios["number"].map(lambda x:count_distance(x, int(df.loc[df.Name==name_detail,"num"]), int(df.loc[df.Name==name_detail,"Losses"])))

for losses in scenarios["distance"].unique():
  temp_index = 0
  for i in scenarios[scenarios.distance==losses].index:
    scenarios.loc[i,"x"] = (temp_index % 3)*0.15 + scenarios.loc[i,"distance"]
    scenarios.loc[i,"y"] = (temp_index // 3)*0.1 + 0.1
    temp_index += 1



  # Create distplot with custom bin_size

fig = px.scatter(scenarios, x="x", y="y", color="status", 
                 color_discrete_map={"win_outright": 'blue', "tie": "lightblue", "lost":"white"}, 
                 hover_name="winners",
                 hover_data={'x':False, # remove species from hover data
                             'y':False, # customize hover for column of y attribute
                             'teams':True # add other column, default formatting
                            },
                 title="Remaining Scenarios and Respective Winners")

fig.update_traces(marker=dict(size=10, line=dict(width=2, color='black')))

fig.update_layout(
    xaxis=dict(fixedrange=True),
    yaxis=dict(fixedrange=True)
)


fig.update_xaxes(title_text=name_detail + " Possible Losses")
fig.update_xaxes(tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

fig.update_yaxes(range=[0,1])
fig.update_yaxes(tickvals=[0,1])
fig.update_yaxes(title_text='')

  
st.plotly_chart(fig, use_container_width=True)
# end experiment




col1, col2 = st.columns(2)

with col1:
  df = df.sort_values(["Wins","Pathways_to_First"], ascending=False)
  st.dataframe(df[["Name", "Wins", "Losses", "Pathways_to_First", "Chance_of_Winning"]], hide_index=True, height=50*len(df))


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


