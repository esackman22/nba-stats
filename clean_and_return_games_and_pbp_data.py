from games import Games
from play_by_play import PlayByPlay


def clean_and_return_games_and_pbp_dfs(raw_games_df, raw_plays_dfs):

    games = Games(raw_games_df)
    pbp = PlayByPlay(raw_plays_dfs)

    return games.clean_and_return_games_df(), pbp.clean_and_return_plays()