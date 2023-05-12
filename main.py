import pandas as pd
from games import Games
from player_comparator import PlayerComparator
from play_by_play import PlayByPlay
from nba_api.stats.endpoints import playbyplayv2
from models import engine, Players
from sqlalchemy.orm import sessionmaker
import time
import datetime

from_date = to_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%m/%d/%Y')

# Retrieve Games
print(f'Finding games for {from_date}.')
game_finder = Games(from_date, to_date)
games_df = game_finder.get_games()
game_ids = list(games_df['game_id'])

if game_ids:
    print(f'There were {len(game_ids)} games on {from_date}. Extracting play by play data...')
    # Retrieve play by play data from those games, sorted by game chronologically
    raw_plays_dfs = []
    for game_id in game_ids:
        pbp = playbyplayv2.PlayByPlayV2('00' + str(game_id))
        raw_plays_dfs.append(pbp.get_data_frames()[0])
        time.sleep(0.5)

    playbyplay = PlayByPlay(raw_plays_dfs)
    plays = playbyplay.get_plays()

    # Extract players from plays data and compare to what's already in the database
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Players)
    stmt = query.statement
    existing_players_dataframe = pd.read_sql(stmt, session.connection())
    comparator = PlayerComparator()
    players_to_add = comparator.compare_to_existing(existing_players_dataframe, plays)
    if len(players_to_add) > 0:
        players_to_add.to_sql('players', engine, if_exists='append', index=False)

    # Write games data to DB
    print(f'Writing games data for {from_date}.')
    games_df.to_sql('games', engine, if_exists='append', index=False)

    print(f'Writing plays data for {from_date}.\n')
    # Write play by play data to DB
    plays.to_sql('plays', engine, if_exists='append', index=False)
else:
    print(f'There were no games on {from_date}.\n')


