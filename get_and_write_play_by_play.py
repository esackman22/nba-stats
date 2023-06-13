import pandas as pd
from sqlalchemy.orm import sessionmaker

from games import Games
from models import Players
from nba_api_client import NbaApiClient
from play_by_play import PlayByPlay
from player_comparator import PlayerComparator


def clean_and_return_games_and_pbp_dfs(raw_games_df, raw_plays_dfs):

    games = Games(raw_games_df)
    pbp = PlayByPlay(raw_plays_dfs)

    return games.clean_and_return_games_df(), pbp.clean_and_return_plays()


def retrieve_and_return_raw_games_and_pbp_dfs(from_date, to_date):

    api_client = NbaApiClient(from_date=from_date, to_date=to_date)
    raw_games_df = api_client.retrieve_and_return_games_df()
    game_ids = list(raw_games_df['GAME_ID'].unique())
    raw_plays_dfs = NbaApiClient.retrieve_and_return_games_df(game_ids)

    return raw_games_df, raw_plays_dfs


def retrieve_and_return_players_to_add(engine, play_by_play_data):
    cur_session = sessionmaker(bind=engine)
    session = cur_session()
    query = session.query(Players)
    stmt = query.statement
    existing_players_dataframe = pd.read_sql(stmt, session.connection())
    comparator = PlayerComparator()
    players_to_add = comparator.compare_to_existing(existing_players_dataframe, plays)
    return players_to_add


def write_data_to_sql(players_df: pd.DataFrame, games_df: pd.DataFrame, plays_df: pd.DataFrame, engine):

    if len(players_df) > 0:
        players_df.to_sql('players', engine, if_exists='append', index=False)

    games_df.to_sql('games', engine, if_exists='append', index=False)
    plays_df.to_sql('plays', engine, if_exists='append', index=False)
