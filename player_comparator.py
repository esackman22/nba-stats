import pandas as pd
import numpy as np
from play_by_play import PlayByPlay
from games import Games
from constants import player2_name, player1_id, player2_id, player1_name, player3_id, player3_name


class PlayerComparator:
    """This object is initialized with two dataframes. One contains all of the active players in the database,
    and the other is a processed play by play dataframe. The object then extracts the player data from the play by play,
    and compares it to existing players. If there are new players in the play by play data, the object will return
    a dataframe containing their info to write to the database."""

    columns = ['id', 'full_name', 'first_name', 'last_name', 'is_active']

    def compare_to_existing(self, existing_players_dataframe, play_by_play_dataframe):
        """Compares existing players dataframe to to players extracted from play by play data.
        If there are new players, it returns a dataframe with their data."""

        updated = self.extract_players_from_pbp(play_by_play_dataframe)
        existing_ids = set(existing_players_dataframe['id'])
        updated_ids = set(updated['id'])
        ids_to_add = updated_ids.difference(existing_ids)

        if len(ids_to_add) > 0:
            players_to_add = updated[updated['id'].isin(ids_to_add)]
            return players_to_add
        else:
            return pd.DataFrame()

    def extract_players_from_pbp(self, play_by_play_dataframe):
        """Extracts player data from play by play data."""

        pbp = play_by_play_dataframe

        unique_player_ids = self._extract_unique_player_ids(pbp)
        players_from_pbp = self._build_players_list_from_unique_ids(pbp, unique_player_ids)
        columns = self.columns
        players_from_pbp_dataframe = pd.DataFrame(players_from_pbp, columns=columns)

        return players_from_pbp_dataframe

    def _extract_unique_player_ids(self, play_by_play_dataframe):
        """Retrieves a list of unique player IDs from a play by play dataframe. This is then used by
        subsequent processing methods to build player dataframes from the play by play data."""

        pbp = play_by_play_dataframe
        unique_player_ids = set()
        player_ids = np.append(pbp['player1_id'].unique(), np.append(pbp['player2_id'].unique(), pbp['player3_id'].unique()))

        for player_id in player_ids:

            unique_player_ids.add(player_id)

        return unique_player_ids

    def _build_players_list_from_unique_ids(self, play_by_play_dataframe, unique_ids):
        """Given a list of unique player IDs and play by play data, this builds a list of tuples
        containing player data extracted from the play by play data."""

        pbp = play_by_play_dataframe
        players_from_pbp = list()

        for player_id in unique_ids:

            if len(pbp[pbp[player1_id] == player_id][player1_name].unique()) == 1:
                full_name, first_name, last_name = self._extract_player_name(player_id, 1, pbp)
            elif len(pbp[pbp[player2_id] == player_id][player2_name].unique()) == 1:
                full_name, first_name, last_name = self._extract_player_name(player_id, 2, pbp)
            elif len(pbp[pbp[player3_id] == player_id][player3_name].unique()) == 1:
                full_name, first_name, last_name = self._extract_player_name(player_id, 3, pbp)
            else:
                continue

            players_from_pbp.append((player_id, full_name, first_name, last_name, True))

        return players_from_pbp

    def _extract_player_name(self, player_id, player_column_number, pbp):
        """This function extracts player name information from a row in play by play dataframe."""

        id = f'player{player_column_number}_id'
        name = f'player{player_column_number}_name'

        full_name = pbp[pbp[id] == player_id][name].unique()[0]
        first_name = full_name.split(' ', 1)[0]
        if len(full_name.split(' ', 1)) < 2:
            last_name = ''
        else:
            last_name = full_name.split(' ', 1)[1]

        return full_name, first_name, last_name
