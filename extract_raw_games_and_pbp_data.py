from nba_api_client import NbaApiClient


def retrieve_and_return_raw_games_and_pbp_dfs(from_date, to_date):

    api_client = NbaApiClient(from_date=from_date, to_date=to_date)
    raw_games_df = api_client.retrieve_and_return_games_df()
    game_ids = list(raw_games_df['GAME_ID'].unique())
    raw_plays_dfs = NbaApiClient.retrieve_and_return_games_df(game_ids)

    return raw_games_df, raw_plays_dfs