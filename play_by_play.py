import pandas as pd
import numpy as np
import time
import config
from connect import Connector
from nba_api.stats.endpoints import playbyplayv2
from games import Games


class PlayByPlay:

    columns = config.play_by_play_columns

    def __init__(self, game_ids):
        self.game_ids = game_ids

    def get_plays(self):
        return self._clean_data()

    def _build_raw_dataframe(self):

        raw_play_by_play_data = pd.DataFrame(columns=self.columns)

        for game_id in self.game_ids:
            pbp = playbyplayv2.PlayByPlayV2('00' + str(game_id))
            pbp = pbp.get_data_frames()[0]
            raw_play_by_play_data = pd.concat([raw_play_by_play_data, pbp], ignore_index=True)
            time.sleep(0.5)

        return raw_play_by_play_data

    def _retrieve_max_play_id(self):

        connector = Connector()
        conn, cursor = connector.connect()
        cursor.execute("SELECT MAX(play_id) FROM playbyplay")
        max_play_id = cursor.fetchall()[0][0]
        conn.commit()
        conn.close()

        return max_play_id

    def _add_play_id(self):

        start_id = self._retrieve_max_play_id()
        raw_plays = self._build_raw_dataframe()

        sorted_plays = raw_plays.sort_values(by=['GAME_ID', 'PERIOD'], axis=0).reset_index().drop('index', axis=1)
        length = len(sorted_plays)
        play_id = [x + start_id for x in range(1, length + 1)]
        sorted_plays.insert(0, 'PLAY_ID', play_id)

        return sorted_plays

    def _clean_data(self):

        play_by_play = self._add_play_id()

        """
        DATA CLEANING: There is a lot of messy data in the playbyplay dataframe that needs to be cleaned to ensure inserted data meets foreign key constraints
        1. Where player ID is 0, set to null (player1_id, player2_id, player3_id)
        2. Where player ID is actually a team ID (cross reference teams table), set player ID to null and move ID to team_id column (player1_id... player1_team_id...)
        3. Where player ID is a value but name is null set player id to null.
        4. Fix data types so when inserted into Postgres it's done correctly
        """
        # 1. Where player ID is 0, set to null (player1_id, player2_id, player3_id)
        play_by_play = self._nullify_zero_player_id(play_by_play)

        # 2. Where player ID is actually a team ID (cross reference teams table), set player ID to null and move ID to team_id column (player1_id... player1_team_id...)
        play_by_play = self._move_team_id_to_correct_column(play_by_play)

        # 3. Where player ID is a value but name is null set player id to null.
        play_by_play = self._nullify_empty_player_names(play_by_play)

        # 4. Fix data types
        play_by_play = self._fix_data_types(play_by_play)

        return play_by_play

    def _nullify_zero_player_id(self, plays_dataframe):
        plays_dataframe = plays_dataframe.replace(to_replace={'PLAYER1_ID': 0, 'PLAYER2_ID': 0, 'PLAYER3_ID': 0}, value=np.nan)
        return plays_dataframe

    def _move_team_id_to_correct_column(self, plays_dataframe):

        def move_team_id_if_in_player_column(row):

            team_ids = config.TEAMS

            if row.PLAYER1_ID in team_ids:
                row.PLAYER1_TEAM_ID = row.PLAYER1_ID
                row.PLAYER1_ID = np.nan

            if row.PLAYER2_ID in team_ids:
                row.PLAYER2_TEAM_ID = row.PLAYER2_ID
                row.PLAYER2_ID = np.nan

            if row.PLAYER3_ID in team_ids:
                row.PLAYER3_TEAM_ID = row.PLAYER3_ID
                row.PLAYER3_ID = np.nan

            return row

        plays_dataframe = plays_dataframe.apply(func=move_team_id_if_in_player_column, axis=1)
        return plays_dataframe

    def _nullify_empty_player_names(self, plays_dataframe):

        plays_dataframe.loc[plays_dataframe['PLAYER1_NAME'].isnull(), 'PLAYER1_ID'] = np.nan
        plays_dataframe.loc[plays_dataframe['PLAYER2_NAME'].isnull(), 'PLAYER2_ID'] = np.nan
        plays_dataframe.loc[plays_dataframe['PLAYER3_NAME'].isnull(), 'PLAYER3_ID'] = np.nan
        return plays_dataframe

    def _fix_data_types(self, plays_dataframe):

        plays_dataframe['GAME_ID'] = plays_dataframe['GAME_ID'].astype('Int64')

        plays_dataframe = plays_dataframe.replace(to_replace={'SCOREMARGIN': 'TIE'}, value='0')
        plays_dataframe['SCOREMARGIN'] = plays_dataframe['SCOREMARGIN'].astype('Int64')

        plays_dataframe['PLAYER1_ID'] = plays_dataframe['PLAYER1_ID'].astype('Int64')
        plays_dataframe['PLAYER2_ID'] = plays_dataframe['PLAYER2_ID'].astype('Int64')
        plays_dataframe['PLAYER3_ID'] = plays_dataframe['PLAYER3_ID'].astype('Int64')

        plays_dataframe['PLAYER1_TEAM_ID'] = plays_dataframe['PLAYER1_TEAM_ID'].astype('Int64')
        plays_dataframe['PLAYER2_TEAM_ID'] = plays_dataframe['PLAYER2_TEAM_ID'].astype('Int64')
        plays_dataframe['PLAYER3_TEAM_ID'] = plays_dataframe['PLAYER3_TEAM_ID'].astype('Int64')
        return plays_dataframe




if __name__ == "__main__":
    games = Games()
    game_ids = list(games.get_games()['GAME_ID'])
    print(game_ids)
    playbyplay = PlayByPlay(game_ids)
    plays = playbyplay.get_plays()
    print(plays.head())
    print(plays.info())
    print(plays.describe())