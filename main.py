from models import engine
from extract_raw_games_and_pbp_data import retrieve_and_return_raw_games_and_pbp_dfs
from clean_and_return_games_and_pbp_data import clean_and_return_games_and_pbp_dfs
from retrieve_players_to_add_to_db_from_pbp import retrieve_and_return_players_to_add
from write_data_to_db import write_data_to_sql
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
    write_data_to_sql(players_to_add, final_games_df, final_plays_df)
else:
    print(f'There were no games on {from_date}.\n')


