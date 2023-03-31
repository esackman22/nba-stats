from games import Games
from players import Players
from play_by_play import PlayByPlay
from connect import Connector
from executor import Executor
import datetime

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
from_date = to_date = yesterday.isoformat()

# Connect to DB and create a cursor for executing queries.
connector = Connector()
conn, cursor = connector.connect()

# Create an executor instance for writing to DB
exec = Executor(conn, cursor)

# Retrieve Games
yesterdays_games = Games(from_date, to_date)
yesterdays_games_data = yesterdays_games.get_games()
game_ids = list(yesterdays_games_data['GAME_ID'])

# Retrieve play by play data from those games, sorted by game chronologically
playbyplay = PlayByPlay(game_ids)
plays = playbyplay.get_plays()

# Extract players from plays data
nba_players = Players()
players_to_add = nba_players.compare_to_existing(plays)
if players_to_add:
    exec.execute_values(players_to_add, 'players')

# Write games data to DB
exec.execute_values(yesterdays_games_data, 'games')

# Write play by play data to DB
exec.execute_values(plays, 'playbyplay')

# Close connections
conn.close()

