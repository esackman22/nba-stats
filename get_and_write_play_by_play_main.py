from models import engine
from get_and_write_play_by_play import clean_and_return_games_and_pbp_dfs, retrieve_and_return_raw_games_and_pbp_dfs, \
    retrieve_and_return_players_to_add, write_data_to_sql
import datetime

from_date = to_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%m/%d/%Y')

# Extract raw data from NBA API Client Package
raw_games_df, raw_plays_dfs = retrieve_and_return_raw_games_and_pbp_dfs(from_date, to_date)

if raw_plays_dfs:
    print(f'There were {len(raw_plays_dfs)} games on {from_date}.')
    final_games_df, final_plays_df = clean_and_return_games_and_pbp_dfs(raw_games_df, raw_plays_dfs)

    # Extract players from plays data and compare to what's already in the database
    players_to_add = retrieve_and_return_players_to_add(engine, final_plays_df)

    # Write data to DB
    write_data_to_sql(players_to_add, final_games_df, final_plays_df, engine)
else:
    print(f'There were no games on {from_date}.\n')


