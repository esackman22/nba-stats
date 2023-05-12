import pandas as pd
import numpy as np
from play_by_play import PlayByPlay
from games import Games


class PlayerComparator:

    columns = ['id', 'full_name', 'first_name', 'last_name', 'is_active']

    def compare_to_existing(self, existing_players_dataframe, play_by_play_dataframe):

        updated = self.extract_players_from_pbp(play_by_play_dataframe)
        existing_ids = set(existing_players_dataframe['id'])
        updated_ids = set(updated['id'])
        ids_to_add = updated_ids.difference(existing_ids)

        if len(ids_to_add) > 0:
            players_to_add = updated[updated['id'].isin(ids_to_add)]
            print(f'There are {len(ids_to_add)} new players to add to the database.')
            print(players_to_add)
            return players_to_add
        else:
            print('There are no players to add to the database.')
            return pd.DataFrame()

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
        player_ids = np.append(pbp['player1_id'].unique(), np.append(pbp['player2_id'].unique(), pbp['player3_id'].unique()))

        for player_id in player_ids:

            unique_player_ids.add(player_id)

        return unique_player_ids

    def _build_players_list_from_unique_ids(self, play_by_play_dataframe, unique_ids):

        pbp = play_by_play_dataframe
        players_from_pbp = list()

        for player_id in unique_ids:

            if len(pbp[pbp['player1_id'] == player_id]['player1_name'].unique()) == 1:
                full_name, first_name, last_name = self._extract_player_name(player_id, 1, pbp)
            elif len(pbp[pbp['player2_id'] == player_id]['player2_name'].unique()) == 1:
                full_name, first_name, last_name = self._extract_player_name(player_id, 2, pbp)
            elif len(pbp[pbp['player3_id'] == player_id]['player3_name'].unique()) == 1:
                full_name, first_name, last_name = self._extract_player_name(player_id, 3, pbp)
            else:
                continue

            players_from_pbp.append((player_id, full_name, first_name, last_name, True))

        return players_from_pbp

    def _extract_player_name(self, player_id, player_column_number, pbp):

        id = f'player{player_column_number}_id'
        name = f'player{player_column_number}_name'

        full_name = pbp[pbp[id] == player_id][name].unique()[0]
        first_name = full_name.split(' ', 1)[0]
        if len(full_name.split(' ', 1)) < 2:
            last_name = ''
        else:
            last_name = full_name.split(' ', 1)[1]

        return full_name, first_name, last_name



if __name__ == "__main__":

    players = Players()
    games = Games()
    game_ids = list(games.get_games()["GAME_ID"])
    playbyplay = PlayByPlay(game_ids)
    plays = playbyplay.get_plays()
    print(players.compare_to_existing(plays))
