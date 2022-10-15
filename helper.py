import pandas as pd
import numpy as np

def playerStatistics_vs_bowler(df, selected_batsman):
    df = df[df['batsman'] == selected_batsman]

    df['isDot'] = df['runs_scored'].apply(lambda x: 1 if x == 0 else 0)
    df['isOne'] = df['runs_scored'].apply(lambda x: 1 if x == 1 else 0)
    df['isTwo'] = df['runs_scored'].apply(lambda x: 1 if x == 2 else 0)
    df['isThree'] = df['runs_scored'].apply(lambda x: 1 if x == 3 else 0)
    df['isFour'] = df['runs_scored'].apply(lambda x: 1 if x == 4 else 0)
    df['isSix'] = df['runs_scored'].apply(lambda x: 1 if x == 6 else 0)

    runs = pd.DataFrame(df.groupby(['bowler'])['runs_scored'].sum().reset_index()).groupby(['bowler'])[
        'runs_scored'].sum().reset_index().rename(columns={'runs_scored': 'runs'})
    innings = pd.DataFrame(
        df.groupby(['bowler'])['match_id'].apply(lambda x: len(list(np.unique(x)))).reset_index()).rename(
        columns={'match_id': 'innings'})
    balls = pd.DataFrame(df.groupby(['bowler'])['match_id'].count()).reset_index().rename(columns={'match_id': 'balls'})
    dismissals = pd.DataFrame(df[df['player_dismissed'] == df['batsman']].groupby(['bowler'])[
                                  'player_dismissed'].count()).reset_index().rename(
        columns={'player_dismissed': 'dismissals'})

    dots = pd.DataFrame(df.groupby(['bowler'])['isDot'].sum()).reset_index().rename(columns={'isDot': 'dots'})
    ones = pd.DataFrame(df.groupby(['bowler'])['isOne'].sum()).reset_index().rename(columns={'isOne': 'ones'})
    twos = pd.DataFrame(df.groupby(['bowler'])['isTwo'].sum()).reset_index().rename(columns={'isTwo': 'twos'})
    threes = pd.DataFrame(df.groupby(['bowler'])['isThree'].sum()).reset_index().rename(columns={'isThree': 'threes'})
    fours = pd.DataFrame(df.groupby(['bowler'])['isFour'].sum()).reset_index().rename(columns={'isFour': 'fours'})
    sixes = pd.DataFrame(df.groupby(['bowler'])['isSix'].sum()).reset_index().rename(columns={'isSix': 'sixes'})

    df = pd.merge(innings, runs, on='bowler').merge(balls, on='bowler').merge(dismissals, on='bowler').merge(dots,
                                                                                                             on='bowler').merge(
        ones, on='bowler').merge(twos, on='bowler').merge(threes, on='bowler').merge(fours, on='bowler').merge(sixes,
                                                                                                               on='bowler')

    # bowlerate
    df['strike rate'] = df.apply(lambda x: round(100 * (x['runs'] / x['balls']), 2), axis=1)

    # runs per innings
    df['runs per innings'] = df.apply(lambda x: round(x['runs'] / x['innings'], 2), axis=1)

    # balls per dismissals
    df['balls per dismissal'] = df.apply(lambda x: round(balls_per_dismissal(x['balls'], x['dismissals']), 2), axis=1)

    # balls per boundary
    df['balls per boundary'] = df.apply(lambda x: round(balls_per_boundary(x['balls'], (x['fours'] + x['sixes'])), 2),
                                        axis=1)

    # dot ball percentage
    df['dot%'] = round(df['dots'] / df['balls'] * 100, 2)

    return df


def balls_per_dismissal(balls, dismissals):
    if dismissals > 0:
        return balls / dismissals
    else:
        return balls / 1


def balls_per_boundary(balls, boundaries):
    if boundaries > 0:
        return balls / boundaries
    else:
        return balls / 1



def playerStatistics_by_season(df, selected_batsman):

    df = df[df['batsman'] == selected_batsman]

    df['isDot'] = df['runs_scored'].apply(lambda x: 1 if x == 0 else 0)
    df['isOne'] = df['runs_scored'].apply(lambda x: 1 if x == 1 else 0)
    df['isTwo'] = df['runs_scored'].apply(lambda x: 1 if x == 2 else 0)
    df['isThree'] = df['runs_scored'].apply(lambda x: 1 if x == 3 else 0)
    df['isFour'] = df['runs_scored'].apply(lambda x: 1 if x == 4 else 0)
    df['isSix'] = df['runs_scored'].apply(lambda x: 1 if x == 6 else 0)

    runs = pd.DataFrame(df.groupby(['season'])['runs_scored'].sum().reset_index()).groupby(['season'])[
        'runs_scored'].sum().reset_index().rename(columns={'runs_scored': 'runs'})
    innings = pd.DataFrame(
        df.groupby(['season'])['match_id'].apply(lambda x: len(list(np.unique(x)))).reset_index()).rename(
        columns={'match_id': 'innings'})
    balls = pd.DataFrame(df.groupby(['season'])['match_id'].count()).reset_index().rename(columns={'match_id': 'balls'})
    dismissals = pd.DataFrame(df[df['player_dismissed'] == df['batsman']].groupby(['season'])[
                                  'player_dismissed'].count()).reset_index().rename(
        columns={'player_dismissed': 'dismissals'})

    dots = pd.DataFrame(df.groupby(['season'])['isDot'].sum()).reset_index().rename(columns={'isDot': 'dots'})
    ones = pd.DataFrame(df.groupby(['season'])['isOne'].sum()).reset_index().rename(columns={'isOne': 'ones'})
    twos = pd.DataFrame(df.groupby(['season'])['isTwo'].sum()).reset_index().rename(columns={'isTwo': 'twos'})
    threes = pd.DataFrame(df.groupby(['season'])['isThree'].sum()).reset_index().rename(columns={'isThree': 'threes'})
    fours = pd.DataFrame(df.groupby(['season'])['isFour'].sum()).reset_index().rename(columns={'isFour': 'fours'})
    sixes = pd.DataFrame(df.groupby(['season'])['isSix'].sum()).reset_index().rename(columns={'isSix': 'sixes'})

    df = pd.merge(innings, runs, on='season').merge(balls, on='season').merge(dismissals, on='season').merge(dots,
                                                                                                             on='season').merge(
        ones, on='season').merge(twos, on='season').merge(threes, on='season').merge(fours, on='season').merge(sixes,
                                                                                                               on='season')

    # seasonate
    df['strike rate'] = df.apply(lambda x: round(100 * (x['runs'] / x['balls']), 2), axis=1)

    # runs per innings
    df['runs per innings'] = df.apply(lambda x: round(x['runs'] / x['innings'], 2), axis=1)

    # balls per dismissals
    df['balls per dismissal'] = df.apply(lambda x: round(balls_per_dismissal(x['balls'], x['dismissals']), 2), axis=1)

    # balls per boundary
    df['balls per boundary'] = df.apply(lambda x: round(balls_per_boundary(x['balls'], (x['fours'] + x['sixes'])), 2),
                                        axis=1)

    # dot ball percentage
    df['dot%'] = round(df['dots'] / df['balls'] * 100, 2)

    return df


def balls_per_dismissal(balls, dismissals):
    if dismissals > 0:
        return balls / dismissals
    else:
        return balls / 1


def balls_per_boundary(balls, boundaries):
    if boundaries > 0:
        return balls / boundaries
    else:
        return balls / 1


def playerStatistics_by_Phase_of_play(df, selected_batsman):
    df = df[df['batsman'] == selected_batsman]

    df['isDot'] = df['runs_scored'].apply(lambda x: 1 if x == 0 else 0)
    df['isOne'] = df['runs_scored'].apply(lambda x: 1 if x == 1 else 0)
    df['isTwo'] = df['runs_scored'].apply(lambda x: 1 if x == 2 else 0)
    df['isThree'] = df['runs_scored'].apply(lambda x: 1 if x == 3 else 0)
    df['isFour'] = df['runs_scored'].apply(lambda x: 1 if x == 4 else 0)
    df['isSix'] = df['runs_scored'].apply(lambda x: 1 if x == 6 else 0)

    runs = pd.DataFrame(df.groupby(['Phase_of_play'])['runs_scored'].sum().reset_index()).groupby(['Phase_of_play'])[
        'runs_scored'].sum().reset_index().rename(columns={'runs_scored': 'runs'})
    innings = pd.DataFrame(
        df.groupby(['Phase_of_play'])['match_id'].apply(lambda x: len(list(np.unique(x)))).reset_index()).rename(
        columns={'match_id': 'innings'})
    balls = pd.DataFrame(df.groupby(['Phase_of_play'])['match_id'].count()).reset_index().rename(
        columns={'match_id': 'balls'})
    dismissals = pd.DataFrame(df[df['player_dismissed'] == df['batsman']].groupby(['Phase_of_play'])[
                                  'player_dismissed'].count()).reset_index().rename(
        columns={'player_dismissed': 'dismissals'})

    dots = pd.DataFrame(df.groupby(['Phase_of_play'])['isDot'].sum()).reset_index().rename(columns={'isDot': 'dots'})
    ones = pd.DataFrame(df.groupby(['Phase_of_play'])['isOne'].sum()).reset_index().rename(columns={'isOne': 'ones'})
    twos = pd.DataFrame(df.groupby(['Phase_of_play'])['isTwo'].sum()).reset_index().rename(columns={'isTwo': 'twos'})
    threes = pd.DataFrame(df.groupby(['Phase_of_play'])['isThree'].sum()).reset_index().rename(
        columns={'isThree': 'threes'})
    fours = pd.DataFrame(df.groupby(['Phase_of_play'])['isFour'].sum()).reset_index().rename(
        columns={'isFour': 'fours'})
    sixes = pd.DataFrame(df.groupby(['Phase_of_play'])['isSix'].sum()).reset_index().rename(columns={'isSix': 'sixes'})

    df = pd.merge(innings, runs, on='Phase_of_play').merge(balls, on='Phase_of_play').merge(dismissals,
                                                                                            on='Phase_of_play').merge(
        dots,
        on='Phase_of_play').merge(
        ones, on='Phase_of_play').merge(twos, on='Phase_of_play').merge(threes, on='Phase_of_play').merge(fours,
                                                                                                          on='Phase_of_play').merge(
        sixes,
        on='Phase_of_play')

    # Phase_of_playate
    df['strike rate'] = df.apply(lambda x: round(100 * (x['runs'] / x['balls']), 2), axis=1)

    # runs per innings
    df['runs per innings'] = df.apply(lambda x: round(x['runs'] / x['innings'], 2), axis=1)

    # balls per dismissals
    df['balls per dismissal'] = df.apply(lambda x: round(balls_per_dismissal(x['balls'], x['dismissals']), 2), axis=1)

    # balls per boundary
    df['balls per boundary'] = df.apply(lambda x: round(balls_per_boundary(x['balls'], (x['fours'] + x['sixes'])), 2),
                                        axis=1)

    # dot ball percentage
    df['dot%'] = round(df['dots'] / df['balls'] * 100, 2)

    return df


def playerStatistics_by_venue(df, selected_batsman):
    df = df[df['batsman'] == selected_batsman]

    df['isDot'] = df['runs_scored'].apply(lambda x: 1 if x == 0 else 0)
    df['isOne'] = df['runs_scored'].apply(lambda x: 1 if x == 1 else 0)
    df['isTwo'] = df['runs_scored'].apply(lambda x: 1 if x == 2 else 0)
    df['isThree'] = df['runs_scored'].apply(lambda x: 1 if x == 3 else 0)
    df['isFour'] = df['runs_scored'].apply(lambda x: 1 if x == 4 else 0)
    df['isSix'] = df['runs_scored'].apply(lambda x: 1 if x == 6 else 0)

    runs = pd.DataFrame(df.groupby(['venue'])['runs_scored'].sum().reset_index()).groupby(['venue'])[
        'runs_scored'].sum().reset_index().rename(columns={'runs_scored': 'runs'})
    innings = pd.DataFrame(
        df.groupby(['venue'])['match_id'].apply(lambda x: len(list(np.unique(x)))).reset_index()).rename(
        columns={'match_id': 'innings'})
    balls = pd.DataFrame(df.groupby(['venue'])['match_id'].count()).reset_index().rename(columns={'match_id': 'balls'})
    dismissals = pd.DataFrame(df[df['player_dismissed'] == df['batsman']].groupby(['venue'])[
                                  'player_dismissed'].count()).reset_index().rename(
        columns={'player_dismissed': 'dismissals'})

    dots = pd.DataFrame(df.groupby(['venue'])['isDot'].sum()).reset_index().rename(columns={'isDot': 'dots'})
    ones = pd.DataFrame(df.groupby(['venue'])['isOne'].sum()).reset_index().rename(columns={'isOne': 'ones'})
    twos = pd.DataFrame(df.groupby(['venue'])['isTwo'].sum()).reset_index().rename(columns={'isTwo': 'twos'})
    threes = pd.DataFrame(df.groupby(['venue'])['isThree'].sum()).reset_index().rename(columns={'isThree': 'threes'})
    fours = pd.DataFrame(df.groupby(['venue'])['isFour'].sum()).reset_index().rename(columns={'isFour': 'fours'})
    sixes = pd.DataFrame(df.groupby(['venue'])['isSix'].sum()).reset_index().rename(columns={'isSix': 'sixes'})

    df = pd.merge(innings, runs, on='venue').merge(balls, on='venue').merge(dismissals, on='venue').merge(dots,
                                                                                                          on='venue').merge(
        ones, on='venue').merge(twos, on='venue').merge(threes, on='venue').merge(fours, on='venue').merge(sixes,
                                                                                                           on='venue')

    # venueate
    df['strike rate'] = df.apply(lambda x: round(100 * (x['runs'] / x['balls']), 2), axis=1)

    # runs per innings
    df['runs per innings'] = df.apply(lambda x: round(x['runs'] / x['innings'], 2), axis=1)

    # balls per dismissals
    df['balls per dismissal'] = df.apply(lambda x: round(balls_per_dismissal(x['balls'], x['dismissals']), 2), axis=1)

    # balls per boundary
    df['balls per boundary'] = df.apply(lambda x: round(balls_per_boundary(x['balls'], (x['fours'] + x['sixes'])), 2),
                                        axis=1)

    # dot ball percentage
    df['dot%'] = round(df['dots'] / df['balls'] * 100, 2)

    return df


def playerStatistics_by_bowling_team(df, selected_batsman):
    df = df[df['batsman'] == selected_batsman]

    df['isDot'] = df['runs_scored'].apply(lambda x: 1 if x == 0 else 0)
    df['isOne'] = df['runs_scored'].apply(lambda x: 1 if x == 1 else 0)
    df['isTwo'] = df['runs_scored'].apply(lambda x: 1 if x == 2 else 0)
    df['isThree'] = df['runs_scored'].apply(lambda x: 1 if x == 3 else 0)
    df['isFour'] = df['runs_scored'].apply(lambda x: 1 if x == 4 else 0)
    df['isSix'] = df['runs_scored'].apply(lambda x: 1 if x == 6 else 0)

    runs = pd.DataFrame(df.groupby(['bowling_team'])['runs_scored'].sum().reset_index()).groupby(['bowling_team'])[
        'runs_scored'].sum().reset_index().rename(columns={'runs_scored': 'runs'})
    innings = pd.DataFrame(
        df.groupby(['bowling_team'])['match_id'].apply(lambda x: len(list(np.unique(x)))).reset_index()).rename(
        columns={'match_id': 'innings'})
    balls = pd.DataFrame(df.groupby(['bowling_team'])['match_id'].count()).reset_index().rename(
        columns={'match_id': 'balls'})
    dismissals = pd.DataFrame(df[df['player_dismissed'] == df['batsman']].groupby(['bowling_team'])[
                                  'player_dismissed'].count()).reset_index().rename(
        columns={'player_dismissed': 'dismissals'})

    dots = pd.DataFrame(df.groupby(['bowling_team'])['isDot'].sum()).reset_index().rename(columns={'isDot': 'dots'})
    ones = pd.DataFrame(df.groupby(['bowling_team'])['isOne'].sum()).reset_index().rename(columns={'isOne': 'ones'})
    twos = pd.DataFrame(df.groupby(['bowling_team'])['isTwo'].sum()).reset_index().rename(columns={'isTwo': 'twos'})
    threes = pd.DataFrame(df.groupby(['bowling_team'])['isThree'].sum()).reset_index().rename(
        columns={'isThree': 'threes'})
    fours = pd.DataFrame(df.groupby(['bowling_team'])['isFour'].sum()).reset_index().rename(columns={'isFour': 'fours'})
    sixes = pd.DataFrame(df.groupby(['bowling_team'])['isSix'].sum()).reset_index().rename(columns={'isSix': 'sixes'})

    df = pd.merge(innings, runs, on='bowling_team').merge(balls, on='bowling_team').merge(dismissals,
                                                                                          on='bowling_team').merge(dots,
                                                                                                                   on='bowling_team').merge(
        ones, on='bowling_team').merge(twos, on='bowling_team').merge(threes, on='bowling_team').merge(fours,
                                                                                                       on='bowling_team').merge(
        sixes,
        on='bowling_team')

    # bowling_teamate
    df['strike rate'] = df.apply(lambda x: round(100 * (x['runs'] / x['balls']), 2), axis=1)

    # runs per innings
    df['runs per innings'] = df.apply(lambda x: round(x['runs'] / x['innings'], 2), axis=1)

    # balls per dismissals
    df['balls per dismissal'] = df.apply(lambda x: round(balls_per_dismissal(x['balls'], x['dismissals']), 2), axis=1)

    # balls per boundary
    df['balls per boundary'] = df.apply(lambda x: round(balls_per_boundary(x['balls'], (x['fours'] + x['sixes'])), 2),
                                        axis=1)

    # dot ball percentage
    df['dot%'] = round(df['dots'] / df['balls'] * 100, 2)

    return df

