import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

st.set_page_config(page_title="IPL data analytics", page_icon="🏏", layout="wide")
def IPL_Analysis():

        df = pd.read_csv('IPL_data_with_all_features_till_2022.csv')
        df = df[(df['innings'] == 1 )| (df['innings'] ==2)]
        df = df.rename(columns = {'striker':'batsman', 'runs_off_bat':'runs_scored'})
        from helper import playerStatistics_vs_bowler , balls_per_dismissal , balls_per_boundary,playerStatistics_by_season,playerStatistics_by_Phase_of_play, playerStatistics_by_venue,playerStatistics_by_bowling_team


        import plotly.express as px


        player_stats = pd.read_csv('player_full_stats.csv')

        purple_cap = df.groupby(['bowler' , 'season'])['isBowlerWk'].sum().sort_values(ascending = False).reset_index().drop_duplicates(subset = 'season').reset_index(drop = True).rename(columns = {'isBowlerWk':'wickets'}).sort_values(by = 'season').reset_index(drop = True)
        purple_cap = purple_cap[['season' , 'bowler' , 'wickets']]

        orange_cap = df.groupby(['batsman' , 'season'])['runs_scored'].sum().sort_values(ascending = False).reset_index().drop_duplicates(subset = 'season').reset_index(drop = True).rename(columns = {'batsman': 'batsman' , 'runs_scored':'runs'}).sort_values(by = 'season').reset_index(drop = True)
        orange_cap = orange_cap[['season' , 'batsman' , 'runs']]

        top10_run_scorers = player_stats.sort_values(by = 'runs' , ascending=False)[:10]
        top_10_strike_rate = player_stats[player_stats['runs']>=1000].sort_values(by = 'sixes' , ascending=False)[:10]
        top_10_four_scores = player_stats.sort_values(by = 'fours' , ascending=False)[:10]
        top_10_six_scores = player_stats.sort_values(by = 'sixes' , ascending=False)[:10]
        top_10_wicket_takers = player_stats.sort_values(by = 'wickets_taken' , ascending=False)[:10]
        top_10_dot_bowlers = player_stats[player_stats['balls_bowled']>=1000].sort_values(by = 'bowling_dot%' , ascending=False)[:10]


        top10_run_scorers = top10_run_scorers.sort_values(by = 'runs' , ascending=True)
        top_10_strike_rate = top_10_strike_rate.sort_values(by = 'strike rate' , ascending=True)
        top_10_four_scores = top_10_four_scores.sort_values(by = 'fours' , ascending=True)
        top_10_six_scores = top_10_six_scores.sort_values(by = 'sixes' , ascending=True)
        top_10_wicket_takers = top_10_wicket_takers.sort_values(by = 'wickets_taken' , ascending=True)
        top_10_dot_bowlers = top_10_dot_bowlers.sort_values(by = 'bowling_dot%' , ascending=True)


        ##st.markdown("""
            ##<iframe title="ipl_analysis" width="800" height="500" src="https://app.powerbi.com/view?r=eyJrIjoiMTY2NGY1MWMtMTgxMC00MzVhLWE0ZDctMDVlMmRkYTI2M2VjIiwidCI6IjY2N2I0OTE1LThhMzMtNGMyYy1hNGVmLWE1YzFkNTkxMGJjZiJ9&pageName=ReportSectionc162d51dcf830db1921f" frameborder="0" allowFullScreen="true"></iframe>""", unsafe_allow_html=True)

        st.title('IPL Statistics')


        selected_player = st.selectbox(
             'Select a player',
             (player_stats['player'].unique()))

        playerStatistics_vs_bowler = playerStatistics_vs_bowler(df, selected_player)

        runs_by_season = df[df['batsman'] == selected_player].groupby(['season' , 'batsman'])['runs_scored'].sum().reset_index().drop('batsman' , axis=1)
        runs_against_opposition = df[df['batsman'] == selected_player].groupby(['batsman' , 'bowling_team'])['runs_scored'].sum().reset_index().drop('batsman' , axis=1).sort_values(by ='runs_scored')
        runs_by_phase = df[df['batsman'] == selected_player].groupby(['batsman' , 'Phase_of_play'])['runs_scored'].sum().reset_index().drop('batsman' , axis=1).sort_values(by ='runs_scored')
        runs_against_bowlers = df[df['batsman'] == selected_player].groupby(['batsman' , 'bowler'])['runs_scored'].sum().reset_index().drop('batsman' , axis=1).sort_values(by ='runs_scored' , ascending = False)[:10]
        runs_against_bowlers = runs_against_bowlers.sort_values(by = 'runs_scored')
        batsman_wickets_bowlers = df[df['batsman'] == selected_player].groupby(['batsman' , 'bowler'])['isBowlerWk'].sum().reset_index().drop('batsman' , axis=1).rename(columns = {'isBowlerWk': 'wickets'}).sort_values(by ='wickets' , ascending = False)[:10]
        top_10_dot_bowlers = top_10_dot_bowlers.sort_values(by = 'bowling_dot%')
        runs_against_venues = df[df['batsman'] == selected_player].groupby(['batsman', 'venue'])['runs_scored'].sum().reset_index().drop('batsman', axis=1).sort_values(by='runs_scored', ascending=False)[:10]
        runs_against_venues = runs_against_venues.sort_values(by='runs_scored')
        runs_by_innings = df[(df['batsman'] == selected_player) & (df['innings'] < 3)].groupby(['batsman', 'innings'])['runs_scored'].sum().reset_index().drop('batsman', axis=1).sort_values(by='runs_scored')

        st.title('Batting Statistics: {}'.format(selected_player))

        col1,col2,col3,col4,col5 = st.columns(5)

        with col1:
            st.header('Innings🏏')
            st.title(player_stats[player_stats['player'] == selected_player]['innings'].to_list()[0])

        with col2:
            st.header('Runs🏃‍♂️')
            st.title(player_stats[player_stats['player'] == selected_player]['runs'].to_list()[0])

        with col3:
            st.header('Balls⚾')
            st.title(player_stats[player_stats['player'] == selected_player]['balls'].to_list()[0])

        with col4:
            st.header('Fours:four:')
            st.title(player_stats[player_stats['player'] == selected_player]['fours'].to_list()[0])

        with col5:
            st.header('Sixes:six:')
            st.title(player_stats[player_stats['player'] == selected_player]['sixes'].to_list()[0])


        st.markdown('----------------------------------------------------------')
        col1,col2,col3,col4 , col5 = st.columns(5)

        with col1:
            st.header('Highest')
            st.title(player_stats[player_stats['player'] == selected_player]['highest'].to_list()[0])

        with col2:
            st.header('SR')
            st.title(player_stats[player_stats['player'] == selected_player]['strike rate'].to_list()[0])

        with col3:
            st.header('BpD')
            st.title(player_stats[player_stats['player'] == selected_player]['balls Per dismissal'].to_list()[0])

        with col4:
            st.header('BpB')
            st.title(player_stats[player_stats['player'] == selected_player]['balls per boundary'].to_list()[0])

        with col5:
            st.header('dot% :zero:')
            st.title(player_stats[player_stats['player'] == selected_player]['dot%'].to_list()[0])


        st.write('Note: BpD- Balls per Dismissals , BpB- Balls per Boundary')
        st.markdown('----------------------------------------------------------')

        st.title('Bowling Statistics: {}'.format(selected_player))

        col1,col2,col3,col4,col5 = st.columns(5)

        with col1:
            st.header('Innings🏏')
            st.title(player_stats[player_stats['player'] == selected_player]['bowling_innings'].to_list()[0])

        with col2:
            st.header('Runs🏃‍♂️')
            st.title(player_stats[player_stats['player'] == selected_player]['runs_conceded'].to_list()[0])

        with col3:
            st.header('Balls⚾')
            st.title(player_stats[player_stats['player'] == selected_player]['balls_bowled'].to_list()[0])

        with col4:
            st.header('Wickets')
            st.title(player_stats[player_stats['player'] == selected_player]['wickets_taken'].to_list()[0])

        with col5:
            st.header('Dot% :zero:')
            st.title(player_stats[player_stats['player'] == selected_player]['bowling_dot%'].to_list()[0])

        st.markdown('----------------------------------------------------------')

        st.title('Head to Head Stats')
        selected_bowler = st.selectbox(
             'Select a bowler',
             (playerStatistics_vs_bowler['bowler'].unique()))

        st.title('{} vs {}'.format(selected_player , selected_bowler) )

        col1,col2,col3,col4,col5 = st.columns(5)

        with col1:
            st.header('Innings🏏')
            st.title(playerStatistics_vs_bowler[playerStatistics_vs_bowler['bowler'] == selected_bowler]['innings'].to_list()[0])

        with col2:
            st.header('Runs🏃‍♂️')
            st.title(playerStatistics_vs_bowler[playerStatistics_vs_bowler['bowler'] == selected_bowler]['runs'].to_list()[0])

        with col3:
            st.header('Balls⚾')
            st.title(playerStatistics_vs_bowler[playerStatistics_vs_bowler['bowler'] == selected_bowler]['balls'].to_list()[0])

        with col4:
            st.header('Fours:four:')
            st.title(playerStatistics_vs_bowler[playerStatistics_vs_bowler['bowler'] == selected_bowler]['fours'].to_list()[0])

        with col5:
            st.header('Sixes:six:')
            st.title(playerStatistics_vs_bowler[playerStatistics_vs_bowler['bowler'] == selected_bowler]['sixes'].to_list()[0])


        st.markdown('----------------------------------------------------------')
        col1,col2,col3,col4 , col5 = st.columns(5)

        with col1:
            st.header('Dismissals')
            st.title(playerStatistics_vs_bowler[playerStatistics_vs_bowler['bowler'] == selected_bowler]['dismissals'].to_list()[0])

        with col2:
            st.header('SR')
            st.title(playerStatistics_vs_bowler[playerStatistics_vs_bowler['bowler'] == selected_bowler]['strike rate'].to_list()[0])

        with col3:
            st.header('BpD')
            st.title(playerStatistics_vs_bowler[playerStatistics_vs_bowler['bowler'] == selected_bowler]['balls per dismissal'].to_list()[0])

        with col4:
            st.header('BpB')
            st.title(playerStatistics_vs_bowler[playerStatistics_vs_bowler['bowler'] == selected_bowler]['balls per boundary'].to_list()[0])

        with col5:
            st.header('dot% :zero:')
            st.title(playerStatistics_vs_bowler[playerStatistics_vs_bowler['bowler'] == selected_bowler]['dot%'].to_list()[0])

        st.write('Note: BpD- Balls per Dismissals , BpB- Balls per Boundary')
        st.markdown('----------------------------------------------------------')

        playerStatistics_by_season = playerStatistics_by_season(df, selected_player)
        st.title('Stats by Season')
        selected_season = st.selectbox(
            'Select season',
            (playerStatistics_by_season['season'].unique()))

        st.title('{} vs {}'.format(selected_player, selected_season))

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.header('Innings🏏')
            st.title(playerStatistics_by_season[playerStatistics_by_season['season'] == selected_season][
                         'innings'].to_list()[0])

        with col2:
            st.header('Runs🏃‍♂️')
            st.title(
                playerStatistics_by_season[playerStatistics_by_season['season'] == selected_season]['runs'].to_list()[
                    0])

        with col3:
            st.header('Balls⚾')
            st.title(
                playerStatistics_by_season[playerStatistics_by_season['season'] == selected_season]['balls'].to_list()[
                    0])

        with col4:
            st.header('Fours:four:')
            st.title(
                playerStatistics_by_season[playerStatistics_by_season['season'] == selected_season]['fours'].to_list()[
                    0])

        with col5:
            st.header('Sixes:six:')
            st.title(
                playerStatistics_by_season[playerStatistics_by_season['season'] == selected_season]['sixes'].to_list()[
                    0])

        st.markdown('----------------------------------------------------------')
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.header('Dismissals')
            st.title(playerStatistics_by_season[playerStatistics_by_season['season'] == selected_season][
                         'dismissals'].to_list()[0])

        with col2:
            st.header('SR')
            st.title(playerStatistics_by_season[playerStatistics_by_season['season'] == selected_season][
                         'strike rate'].to_list()[0])

        with col3:
            st.header('BpD')
            st.title(playerStatistics_by_season[playerStatistics_by_season['season'] == selected_season][
                         'balls per dismissal'].to_list()[0])

        with col4:
            st.header('BpB')
            st.title(playerStatistics_by_season[playerStatistics_by_season['season'] == selected_season][
                         'balls per boundary'].to_list()[0])

        with col5:
            st.header('dot% :zero:')
            st.title(
                playerStatistics_by_season[playerStatistics_by_season['season'] == selected_season]['dot%'].to_list()[
                    0])

        st.write('Note: BpD- Balls per Dismissals , BpB- Balls per Boundary')
        st.markdown('----------------------------------------------------------')

        playerStatistics_by_Phase_of_play = playerStatistics_by_Phase_of_play(df, selected_player)
        st.title('Stats by Phase of play')
        selected_Phase_of_play = st.selectbox(
            'Select Phase of play',
            (playerStatistics_by_Phase_of_play['Phase_of_play'].unique()))

        st.title('{} in {} overs'.format(selected_player, selected_Phase_of_play))

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.header('Innings🏏')
            st.title(playerStatistics_by_Phase_of_play[
                         playerStatistics_by_Phase_of_play['Phase_of_play'] == selected_Phase_of_play][
                         'innings'].to_list()[0])

        with col2:
            st.header('Runs🏃‍♂️')
            st.title(
                playerStatistics_by_Phase_of_play[
                    playerStatistics_by_Phase_of_play['Phase_of_play'] == selected_Phase_of_play]['runs'].to_list()[
                    0])

        with col3:
            st.header('Balls⚾')
            st.title(
                playerStatistics_by_Phase_of_play[
                    playerStatistics_by_Phase_of_play['Phase_of_play'] == selected_Phase_of_play]['balls'].to_list()[
                    0])

        with col4:
            st.header('Fours:four:')
            st.title(
                playerStatistics_by_Phase_of_play[
                    playerStatistics_by_Phase_of_play['Phase_of_play'] == selected_Phase_of_play]['fours'].to_list()[
                    0])

        with col5:
            st.header('Sixes:six:')
            st.title(
                playerStatistics_by_Phase_of_play[
                    playerStatistics_by_Phase_of_play['Phase_of_play'] == selected_Phase_of_play]['sixes'].to_list()[
                    0])

        st.markdown('----------------------------------------------------------')
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.header('Dismissals')
            st.title(playerStatistics_by_Phase_of_play[
                         playerStatistics_by_Phase_of_play['Phase_of_play'] == selected_Phase_of_play][
                         'dismissals'].to_list()[0])

        with col2:
            st.header('SR')
            st.title(playerStatistics_by_Phase_of_play[
                         playerStatistics_by_Phase_of_play['Phase_of_play'] == selected_Phase_of_play][
                         'strike rate'].to_list()[0])

        with col3:
            st.header('BpD')
            st.title(playerStatistics_by_Phase_of_play[
                         playerStatistics_by_Phase_of_play['Phase_of_play'] == selected_Phase_of_play][
                         'balls per dismissal'].to_list()[0])

        with col4:
            st.header('BpB')
            st.title(playerStatistics_by_Phase_of_play[
                         playerStatistics_by_Phase_of_play['Phase_of_play'] == selected_Phase_of_play][
                         'balls per boundary'].to_list()[0])

        with col5:
            st.header('dot% :zero:')
            st.title(
                playerStatistics_by_Phase_of_play[
                    playerStatistics_by_Phase_of_play['Phase_of_play'] == selected_Phase_of_play]['dot%'].to_list()[
                    0])

        st.write('Note: BpD- Balls per Dismissals , BpB- Balls per Boundary')
        st.markdown('----------------------------------------------------------')

        playerStatistics_by_venue = playerStatistics_by_venue(df, selected_player)
        st.title('Stats by venue')
        selected_venue = st.selectbox(
            'Select venue',
            (playerStatistics_by_venue['venue'].unique()))

        st.title('{} in {}'.format(selected_player, selected_venue))

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.header('Innings🏏')
            st.title(playerStatistics_by_venue[playerStatistics_by_venue['venue'] == selected_venue][
                         'innings'].to_list()[0])

        with col2:
            st.header('Runs🏃‍♂️')
            st.title(
                playerStatistics_by_venue[playerStatistics_by_venue['venue'] == selected_venue]['runs'].to_list()[
                    0])

        with col3:
            st.header('Balls⚾')
            st.title(
                playerStatistics_by_venue[playerStatistics_by_venue['venue'] == selected_venue]['balls'].to_list()[
                    0])

        with col4:
            st.header('Fours:four:')
            st.title(
                playerStatistics_by_venue[playerStatistics_by_venue['venue'] == selected_venue]['fours'].to_list()[
                    0])

        with col5:
            st.header('Sixes:six:')
            st.title(
                playerStatistics_by_venue[playerStatistics_by_venue['venue'] == selected_venue]['sixes'].to_list()[
                    0])

        st.markdown('----------------------------------------------------------')
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.header('Dismissals')
            st.title(playerStatistics_by_venue[playerStatistics_by_venue['venue'] == selected_venue][
                         'dismissals'].to_list()[0])

        with col2:
            st.header('SR')
            st.title(playerStatistics_by_venue[playerStatistics_by_venue['venue'] == selected_venue][
                         'strike rate'].to_list()[0])

        with col3:
            st.header('BpD')
            st.title(playerStatistics_by_venue[playerStatistics_by_venue['venue'] == selected_venue][
                         'balls per dismissal'].to_list()[0])

        with col4:
            st.header('BpB')
            st.title(playerStatistics_by_venue[playerStatistics_by_venue['venue'] == selected_venue][
                         'balls per boundary'].to_list()[0])

        with col5:
            st.header('dot% :zero:')
            st.title(
                playerStatistics_by_venue[playerStatistics_by_venue['venue'] == selected_venue]['dot%'].to_list()[
                    0])

        st.write('Note: BpD- Balls per Dismissals , BpB- Balls per Boundary')
        st.markdown('----------------------------------------------------------')

        playerStatistics_by_bowling_team = playerStatistics_by_bowling_team(df, selected_player)
        st.title('Stats vs Opposition')
        selected_bowling_team = st.selectbox(
            'Select opposition team',
            (playerStatistics_by_bowling_team['bowling_team'].unique()))

        st.title('{} vs {}'.format(selected_player, selected_bowling_team))

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.header('Innings🏏')
            st.title(playerStatistics_by_bowling_team[
                         playerStatistics_by_bowling_team['bowling_team'] == selected_bowling_team][
                         'innings'].to_list()[0])

        with col2:
            st.header('Runs🏃‍♂️')
            st.title(
                playerStatistics_by_bowling_team[
                    playerStatistics_by_bowling_team['bowling_team'] == selected_bowling_team]['runs'].to_list()[
                    0])

        with col3:
            st.header('Balls⚾')
            st.title(
                playerStatistics_by_bowling_team[
                    playerStatistics_by_bowling_team['bowling_team'] == selected_bowling_team]['balls'].to_list()[
                    0])

        with col4:
            st.header('Fours:four:')
            st.title(
                playerStatistics_by_bowling_team[
                    playerStatistics_by_bowling_team['bowling_team'] == selected_bowling_team]['fours'].to_list()[
                    0])

        with col5:
            st.header('Sixes:six:')
            st.title(
                playerStatistics_by_bowling_team[
                    playerStatistics_by_bowling_team['bowling_team'] == selected_bowling_team]['sixes'].to_list()[
                    0])

        st.markdown('----------------------------------------------------------')
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.header('Dismissals')
            st.title(playerStatistics_by_bowling_team[
                         playerStatistics_by_bowling_team['bowling_team'] == selected_bowling_team][
                         'dismissals'].to_list()[0])

        with col2:
            st.header('SR')
            st.title(playerStatistics_by_bowling_team[
                         playerStatistics_by_bowling_team['bowling_team'] == selected_bowling_team][
                         'strike rate'].to_list()[0])

        with col3:
            st.header('BpD')
            st.title(playerStatistics_by_bowling_team[
                         playerStatistics_by_bowling_team['bowling_team'] == selected_bowling_team][
                         'balls per dismissal'].to_list()[0])

        with col4:
            st.header('BpB')
            st.title(playerStatistics_by_bowling_team[
                         playerStatistics_by_bowling_team['bowling_team'] == selected_bowling_team][
                         'balls per boundary'].to_list()[0])

        with col5:
            st.header('dot% :zero:')
            st.title(
                playerStatistics_by_bowling_team[
                    playerStatistics_by_bowling_team['bowling_team'] == selected_bowling_team]['dot%'].to_list()[
                    0])

        st.write('Note: BpD- Balls per Dismissals , BpB- Balls per Boundary')
        st.markdown('----------------------------------------------------------')

        st.title("{}'s other statistics".format(selected_player))

        fig_runs_by_season = px.line(
            runs_by_season,
            x="season",
            y='runs_scored',
            title="<b>Runs in each season</b>",
            color_discrete_sequence=["#0083B8"] * len(runs_by_season),
            template="plotly_white",
            text = 'runs_scored',
            width=1500, height=500
        )
        fig_runs_by_season.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        fig_runs_by_phase = px.pie(
            runs_by_phase,
            values="runs_scored",
            names='Phase_of_play',
            title="<b>Runs By Phase</b>",
            template="plotly_white",
            width=1500, height=500)


        fig_batsman_wickets_bowlers = px.bar(
            batsman_wickets_bowlers,
            x="wickets",
            y='bowler',
            title="<b>Most Dismissals</b>",
            color_discrete_sequence=["#0083B8"] * len(batsman_wickets_bowlers),
            template="plotly_white",
            text = 'wickets',
            width=1500, height=500
        )
        fig_batsman_wickets_bowlers.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        fig_runs_against_venues = px.bar(
            runs_against_venues,
            x="runs_scored",
            y='venue',
            title="<b>Runs in each venues</b>",
            color_discrete_sequence=["#0083B8"] * len(runs_against_venues),
            template="plotly_white",
            text='runs_scored',
            width=1500, height=500
        )
        fig_runs_against_venues.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )



        fig_top_10_strike_rate = px.bar(
            top_10_strike_rate,
            x="strike rate",
            y='player',
            title="<b>Highest Strike Rate (Min 1000 runs)</b>",
            color_discrete_sequence=["#0083B8"] * len(top_10_strike_rate),
            template="plotly_white",
            text = 'strike rate',
            width=1500, height=500
        )
        fig_top_10_strike_rate.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )


        fig_top10_runs = px.bar(
            top10_run_scorers,
            x="runs",
            y='player',
            title="<b>Top 10 run scorers</b>",
            color_discrete_sequence=["#0083B8"] * len(top10_run_scorers),
            template="plotly_white",
            text = 'runs',
            width=1500, height=500
        )
        fig_top10_runs.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )


        fig_top_10_sixes = px.bar(
            top_10_six_scores,
            x="sixes",
            y='player',
            title="<b>Most Sixes</b>",
            color_discrete_sequence=["#0083B8"] * len(top_10_six_scores),
            template="plotly_white",
            text = 'sixes',
            width=1500, height=500
        )
        fig_top_10_sixes.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )


        fig_top_10_fours = px.bar(
            top_10_four_scores,
            x="fours",
            y='player',
            title="<b>Most Fours</b>",
            color_discrete_sequence=["#0083B8"] * len(top_10_four_scores),
            template="plotly_white",
            text = 'fours',
            width=1500, height=500
        )
        fig_top_10_fours.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )


        fig_runs_against_opposition = px.bar(
            runs_against_opposition,
            x="runs_scored",
            y='bowling_team',
            title="<b>Runs against each opposition</b>",
            color_discrete_sequence=["#0083B8"] * len(runs_against_opposition),
            template="plotly_white",
            text = 'runs_scored',
            width=1500, height=500
        )
        fig_runs_against_opposition.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        fig_runs_against_bowlers = px.bar(
            runs_against_bowlers,
            x="runs_scored",
            y='bowler',
            title="<b>Most runs against bowlers</b>",
            color_discrete_sequence=["#0083B8"] * len(runs_against_bowlers),
            template="plotly_white",
            text = 'runs_scored',
            width=1500, height=500
        )
        fig_runs_against_bowlers.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )


        fig_top_10_wicket_takers = px.bar(
            top_10_wicket_takers,
            x="wickets_taken",
            y='player',
            title="<b>Highest Wickets Takers</b>",
            color_discrete_sequence=["#0083B8"] * len(top_10_wicket_takers),
            template="plotly_white",
            text = 'wickets_taken',
            width=1500, height=500
        )
        fig_top_10_wicket_takers.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )


        fig_top_10_dot_bowlers = px.bar(
            top_10_dot_bowlers,
            x="bowling_dot%",
            y='player',
            title="<b>Highest Dot% by bowlers(Min 1000 balls)</b>",
            color_discrete_sequence=["#0083B8"] * len(top_10_dot_bowlers),
            template="plotly_white",
            text = 'bowling_dot%',
            width=1500, height=500
        )
        fig_top_10_dot_bowlers.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        fig_runs_by_innings = px.pie(
            runs_by_innings,
            values="runs_scored",
            names='innings',
            title="<b>Runs By Innings</b>",
            template="plotly_white",
            width=1500, height=500)


        left_column, right_column = st.columns(2)

        left_column.plotly_chart(fig_runs_by_season, use_container_width=True)
        right_column.plotly_chart(fig_runs_against_opposition , use_container_width=True)

        left_column, right_column = st.columns(2)
        right_column.plotly_chart(fig_runs_by_phase , use_container_width=True)
        left_column.plotly_chart(fig_runs_against_bowlers , use_container_width=True)

        left_column , right_column = st.columns(2)
        left_column.plotly_chart(fig_batsman_wickets_bowlers, use_container_width=True)
        right_column.plotly_chart(fig_runs_against_venues, use_container_width=True)

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_runs_by_innings, use_container_width=True)
        #right_column.plotly_chart(fig_runs_against_venues, use_container_width=True)

        st.title('Top Statistics')

        col1 , col2 = st.columns(2)
        with col1:
            st.title('Orange Cap Winners')
            st.dataframe(orange_cap)

        with col2:
            st.title('Purple Cap Winners')
            st.dataframe(purple_cap)



        left_column, right_column = st.columns(2)
        right_column.plotly_chart(fig_top_10_strike_rate, use_container_width=True)
        left_column.plotly_chart(fig_top10_runs, use_container_width=True)



        left_column, right_column = st.columns(2)
        right_column.plotly_chart(fig_top_10_fours, use_container_width=True)
        left_column.plotly_chart(fig_top_10_sixes, use_container_width=True)

        left_column, right_column = st.columns(2)
        right_column.plotly_chart(fig_top_10_wicket_takers, use_container_width=True)
        left_column.plotly_chart(fig_top_10_dot_bowlers, use_container_width=True)



IPL_Analysis()
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;}
                    </style>
                    """
st.markdown(hide_st_style, unsafe_allow_html=True)
