"""
What do we need the players class to do
    1. Pull in updated players df from the api
    2. Compare the updated players df to what's in the db. Anything not in the db gets
        output as a new dataframe that we can then plug into the executor to write to db
    3. Take in a playbyplay dataframe and build a players dataframe from it.
"""
from nba_api.stats.static import players as api_players
import pandas as pd
import numpy as np
from connect import Connector


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

    def compare_to_existing(self, updated):

        existing = self.existing_players_dataframe
        if len(existing) > 0:
            existing_ids = set(existing['id'])
        else:
            existing_ids = set()

        updated_ids = set(updated['id'])

        ids_to_add = updated_ids.difference(existing_ids)

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
        all_player_ids = np.append(pbp['PLAYER1_ID'].unique(), np.append(pbp['PLAYER2_ID'].unique(), pbp['PLAYER3_ID'].unique()))

        for player_id in all_player_ids:
            unique_player_ids.add(player_id)

        return unique_player_ids

    def _build_players_list_from_unique_ids(self, play_by_play_dataframe, unique_ids):

        pbp = play_by_play_dataframe
        players_from_pbp = list()

        for player_id in unique_ids:
            if len(pbp[pbp['PLAYER1_ID'] == player_id]['PLAYER1_NAME'].unique()) == 1:
                full_name = pbp[pbp['PLAYER1_ID'] == player_id]['PLAYER1_NAME'].unique()[0]
                first_name = full_name.split(' ', 1)[0]
                last_name = full_name.split(' ', 1)[1]
                players_from_pbp.append((player_id, full_name, first_name, last_name, True))
            elif len(pbp[pbp['PLAYER2_ID'] == player_id]['PLAYER2_NAME'].unique()) == 1:
                full_name = pbp[pbp['PLAYER2_ID'] == player_id]['PLAYER2_NAME'].unique()[0]
                first_name = full_name.split(' ', 1)[0]
                last_name = full_name.split(' ', 1)[1]
                players_from_pbp.append((player_id, full_name, first_name, last_name, True))
            else:
                full_name = pbp[pbp['PLAYER3_ID'] == player_id]['PLAYER3_NAME'].unique()[0]
                first_name = full_name.split(' ', 1)[0]
                last_name = full_name.split(' ', 1)[1]
                players_from_pbp.append((player_id, full_name, first_name, last_name, True))

        return players_from_pbp


if __name__ == "__main__":

    players = Players()
    updated_players = players.retrieve_players_from_api()
    players_to_add = players.compare_to_existing(updated_players)
    print(players_to_add)
