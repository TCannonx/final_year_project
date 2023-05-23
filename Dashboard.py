import pandas as pd
import os
import streamlit as st
import numpy as np
from numpy import dot
from numpy.linalg import norm

def player_values(player_df):
    output = player_df.drop(['player'], axis=1)
    output = output.values.tolist()[0]
    return output
    
def euclidean_distance(list_1, list_2):
    distance = np.linalg.norm(list_1 - list_2)
    return distance

def similar_players(target_player, df, output_count):
    target_player_row = df[df['player'] == target_player].drop(['player'], axis=1)
    target_player_list = target_player_row.values.tolist()[0]
    
    euclidean_list = []
    for player in df['player']:
        player_row = df[df['player'] == player].drop(['player'], axis=1)
        player_vals = player_row.values.tolist()
        
        if len(player_vals) == 1:
            player_list = player_vals[0]
            euclidean = euclidean_distance(target_player_list, player_list)
            euclidean_list.append(euclidean)
            
        else:
            euclidean_list.append(0)

    output_df = pd.DataFrame()
    output_df['player'] = df['player']
    output_df['value'] = euclidean_list

    output_df = output_df.sort_values('value', ascending=False).reset_index(drop=True).head(output_count + 1)

    return output_df

comparison_df = pd.read_csv('improved_vector_space.csv')
player_info  = pd.read_csv('player_info.csv')
player_info.rename(columns={'Comp Level':'Comp_Level'}, inplace=True)

st.title('Similar Player App')

players = comparison_df['player'].to_list()
user_input = st.selectbox('Select Player:', players)

selected_player = comparison_df[comparison_df['player'] == user_input]


# league
league_list = player_info["Comp_Level"].unique().tolist()

container = st.container()
all = st.checkbox('Select All Leagues')
 
if all:
    league_filter = container.multiselect("Select one or more options:",
         league_list,league_list)

else:
    league_filter =  container.multiselect("Select one or more options:",
        league_list)

chosen_df = player_info.query(('Comp_Level == @league_filter'))

# nationality

nation_list = player_info['Nationality'].unique().tolist()

nation_container = st.container()
all = st.checkbox('Select All Nations', key = 1)
 
if all:
    nation_filter = nation_container.multiselect("Select one or more options:",
         nation_list,nation_list)

else:
    nation_filter =  nation_container.multiselect("Select one or more options:",
        nation_list)

chosen_df = chosen_df.query(('Nationality == @nation_filter'))

# age
min_age = min(player_info['Age'].to_list())
max_age = max(player_info['Age'].to_list())

age_filter = st.slider('Age', min_age, max_age, (min_age, max_age))

chosen_df = chosen_df[(age_filter[0] < chosen_df['Age'])  & (chosen_df['Age'] < age_filter[1])]

filtered_players = chosen_df['Player']

filtered_players = comparison_df['player'].isin(filtered_players)

comparison_df = comparison_df[filtered_players]

players = comparison_df['player'].to_list()

if user_input not in players:
    comparison_df = pd.concat([comparison_df, selected_player], ignore_index=True)
#     comparison_df = comparison_df.append(selected_player)

output_count = st.slider('Number Of Outputted Players', 5, 30, 10)

if league_filter == None:
    st.text('Player yet to be chosen')

else:
    output_df = similar_players(user_input, comparison_df, output_count)
    st.write(output_df)
