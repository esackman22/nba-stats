import pandas as pd


def write_data_to_sql(players_df: pd.DataFrame, games_df: pd.DataFrame, plays_df: pd.DataFrame, engine):
    
    if len(players_df) > 0:
        players_df.to_sql('players', engine, if_exists='append', index=False)

    games_df.to_sql('games', engine, if_exists='append', index=False)
    plays_df.to_sql('plays', engine, if_exists='append', index=False)