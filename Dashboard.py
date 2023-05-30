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
    target_player_list = np.array(target_player_list)
    
    euclidean_list = []
    for player in df['player']:
        player_row = df[df['player'] == player].drop(['player'], axis=1)
        player_vals = player_row.values.tolist()
        
        if len(player_vals) == 1:
            player_list = player_vals[0]
            player_list = np.array(player_list)
            euclidean = euclidean_distance(target_player_list, player_list)
            euclidean_list.append(euclidean)
            
        else:
            euclidean_list.append(0)

    output_df = pd.DataFrame()
    output_df['player'] = df['player']
    output_df['value'] = euclidean_list

    identifiers = ['Nationality', 'Team', 'sub_position', 'Age', 'Comp_Level', 'Games', 'Games Starts', 'Minutes', 'Minutes 90S']

    for column in identifiers:
        output_df[column] = player_info[column]

    output_df.columns = ['Player', 'Similarity Score', 'Nationality', 'Club', 'Position', 'Age', 'League', 'Played', 'Starts', 'Total Mins', 'Total 90s']

    output_df = output_df.sort_values('Similarity Score', ascending=True).reset_index(drop=True).head(output_count + 1)

    return output_df

comparison_df = pd.read_csv('improved_vector_space.csv')
player_info  = pd.read_csv('analysis_players.csv')
player_info.rename(columns={'Comp Level':'Comp_Level'}, inplace=True)

st.title('Similar Player Identification Dashboard')

st.subheader("Data from FBREF and Transfermarkt")
st.subheader('Created by Thomas Cannon')

with st.expander('In Depth Details'):
    st.write('''
    This dashboard was created to accompany an analysis completed for my BSc Data Science Final Year Project.  
    The analyis consisted of testing a number of machine learning classification models to try to make accurate predictions on football players in game positions.  
    The analysis took into context a player's in-game data such as passing, shooting and defensive tendancies to build a profile of each player which could be atributed to a position.  
    Transfer Learning methods through a combination of Support Vector Machines and K-Nearest Neighbour Clustering to build the most accurate models.  
    The data comprises of performance data from all players in the worlds top 11 leagues during the 2021-2022 season. (See bellow for details)  
    Usage:  
    Player: You will be asked to choose the player you would like to analyse. You may choose any player from the leagues provided and the filters applied.  
    League: You will be asked to choose which leagues you would like to explore similar players from.  
    Nationality: You will be asked to choose which Nationalites you would like to explore similar players from.  
    Age: You will be asked to choose which Age Range you would like to explore similar players from.  
    Number Of Inputs: You will be asked to choose the number of outputs you would like to recieve from your filters.  
    ''')

players = comparison_df['player'].to_list()

st.subheader('Player Selection:')
st.text('Please select which player you would like to analyse')

user_input = st.selectbox('Select Player:', players)

selected_player = comparison_df[comparison_df['player'] == user_input]
selected_player_info = player_info[player_info['Player'] == user_input]

st.subheader('League Selection:')
st.text('Please select which league you would like to explore')

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

st.subheader('Nationality Selection:')
st.text('Please select which Nation you would like your output to be limited to')

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

st.subheader('Age Selection:')
st.text('Please select which Age Range you would like your output to be limited to')

min_age = min(player_info['Age'].to_list())
max_age = max(player_info['Age'].to_list())

age_filter = st.slider('Age', min_age, max_age, (min_age, max_age))

chosen_df = chosen_df[(age_filter[0] < chosen_df['Age'])  & (chosen_df['Age'] < age_filter[1])]

filtered_players = chosen_df['Player']

filtered_players = comparison_df['player'].isin(filtered_players)
comparison_df = comparison_df[filtered_players]

player_info = player_info[filtered_players]

players = comparison_df['player'].to_list()


if user_input not in players:
    comparison_df = pd.concat([comparison_df, selected_player], ignore_index=True)
    player_info = pd.concat([player_info, selected_player_info], ignore_index=True)
#     comparison_df = comparison_df.append(selected_player)

st.subheader('Number of Outputs Selection:')
st.text('Please select how many similar players you would like your output to be limited to')
output_count = st.slider('Number Of Outputted Players', 5, 30, 10)

if league_filter == None:
    st.text('Player yet to be chosen')

else:
    output_df = similar_players(user_input, comparison_df, output_count)
    st.write(output_df)

with st.expander('Leagues & Filters'):
    st.write('''
    Leagues:  
    Premier league (England)  
    Championship (England)  
    La Liga (Spain)  
    Serie A (Italy)  
    Bundesliga (Germany)  
    Ligue 1 (France)  
    MLS (United States)  
    Eredivisie (Netherlands)  
    Liga MX (Mexico)  
    Brasiliero Liga (Brazil)  
    Primiera Liga (Portugal)  
      
    Filters:  
    This analysis is only limited to outfiled players. (No Goalkeepers)  
    Limited to players with 900+ minutes played in 21-22 season (10 Full Matches)  
    ''')