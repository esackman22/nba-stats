from nba_api.stats.static import players as api_players
import pandas as pd
import numpy as np
from connect import Connector
from play_by_play import PlayByPlay
from games import Games


class Players:

    columns = ['id', 'full_name', 'first_name', 'last_name', 'is_active']

    def __init__(self):

        connector = Connector()
        conn, cursor = connector.connect()
        cursor.execute("SELECT * FROM players")
        existing_players = cursor.fetchall()
        conn.commit()
        conn.close()

        self.existing_players_dataframe = pd.DataFrame(data=existing_players, columns=self.columns)

    def retrieve_players_from_api(self):
        players_from_api = api_players.get_players()
        return pd.DataFrame(players_from_api)

    def compare_to_existing(self, play_by_play_dataframe):

        updated = self.extract_players_from_pbp(play_by_play_dataframe)
        existing_ids = set(self.existing_players_dataframe['id'])
        updated_ids = set(updated['id'])
        print(updated_ids)
        ids_to_add = updated_ids.difference(existing_ids)
        print(ids_to_add)

        if len(ids_to_add) > 0:
            players_to_add = updated[updated['id'].isin(ids_to_add)]
            print(f'There are {len(ids_to_add)} new players to add to the database.')
            return players_to_add
        else:
            print('There are no players to add to the database.')
            return None

    def extract_players_from_pbp(self, play_by_play_dataframe):

        pbp = play_by_play_dataframe

        unique_player_ids = self._extract_unique_player_ids(pbp)
        players_from_pbp = self._build_players_list_from_unique_ids(pbp, unique_player_ids)
        columns = self.columns
        players_from_pbp_dataframe = pd.DataFrame(players_from_pbp, columns=columns)

        return players_from_pbp_dataframe

    def _extract_unique_player_ids(self, play_by_play_dataframe):

        pbp = play_by_play_dataframe
        unique_player_ids = set()
        player_ids = np.append(pbp['PLAYER1_ID'].unique(), np.append(pbp['PLAYER2_ID'].unique(), pbp['PLAYER3_ID'].unique()))

        for player_id in player_ids:

            unique_player_ids.add(player_id)

        return unique_player_ids

    def _build_players_list_from_unique_ids(self, play_by_play_dataframe, unique_ids):

        pbp = play_by_play_dataframe
        players_from_pbp = list()

        for player_id in unique_ids:

            if len(pbp[pbp['PLAYER1_ID'] == player_id]['PLAYER1_NAME'].unique()) == 1:
                full_name, first_name, last_name = self._extract_player_name(player_id, 1, pbp)
            elif len(pbp[pbp['PLAYER2_ID'] == player_id]['PLAYER2_NAME'].unique()) == 1:
                full_name, first_name, last_name = self._extract_player_name(player_id, 2, pbp)
            elif len(pbp[pbp['PLAYER3_ID'] == player_id]['PLAYER3_NAME'].unique()) == 1:
                full_name, first_name, last_name = self._extract_player_name(player_id, 3, pbp)
            else:
                continue

            players_from_pbp.append((player_id, full_name, first_name, last_name, True))

        return players_from_pbp

    def _extract_player_name(self, player_id, player_column_number, pbp):

        id = f'PLAYER{player_column_number}_ID'
        name = f'PLAYER{player_column_number}_NAME'

        full_name = pbp[pbp[id] == player_id][name].unique()[0]
        first_name = full_name.split(' ', 1)[0]
        last_name = full_name.split(' ', 1)[1]
        return full_name, first_name, last_name



if __name__ == "__main__":

    players = Players()
    games = Games()
    game_ids = list(games.get_games()["GAME_ID"])
    playbyplay = PlayByPlay(game_ids)
    plays = playbyplay.get_plays()
    print(players.compare_to_existing(plays))
