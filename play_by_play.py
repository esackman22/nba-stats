import pandas as pd
import numpy as np
from constants import play_by_play_columns, player1_id, player1_name, player1_team_id, \
    player2_id, player2_name, player2_team_id, player3_id, player3_name, player3_team_id, game_id, TEAMS, scoremargin


class PlayByPlay:

    columns = play_by_play_columns

    def __init__(self, raw_plays_dfs):
        self.raw_plays_dfs = raw_plays_dfs

    def _build_raw_dataframe(self):
        """Concatenates the raw plays dataframes passed into the object into a single dataframe for processing."""

        return pd.concat(self.raw_plays_dfs)

    def clean_and_return_plays(self):

        play_by_play = self._build_raw_dataframe()

        """
        DATA CLEANING: There is a lot of messy data in the playbyplay dataframe that needs to be cleaned to ensure 
        inserted data meets foreign key constraints
        1. Where player ID is 0, set to null (player1_id, player2_id, player3_id)
        2. Where player ID is actually a team ID (cross reference teams table), set player ID to null and move ID to 
        team_id column (player1_id... player1_team_id...)
        3. Where player ID is a value but name is null set player id to null.
        4. Fix data types so when inserted into Postgres it's done correctly
        """
        # 1. Where player ID is 0, set to null (player1_id, player2_id, player3_id)
        play_by_play = self._nullify_zero_player_id(play_by_play)

        # 2. Where player ID is actually a team ID (cross-reference teams table), set player ID to
        # null and move ID to team_id column (player1_id... player1_team_id...)
        play_by_play = self._move_team_id_to_correct_column(play_by_play)

        # 3. Where player ID is a value but name is null set player id to null.
        play_by_play = self._nullify_empty_player_names(play_by_play)

        # 4. Fix data types
        play_by_play = self._fix_data_types(play_by_play)

        return play_by_play

    def _nullify_zero_player_id(self, plays_dataframe):
        """Looks for instances of a player ID value set to zero and changes it to null to avoid foreign key constraint
        issues."""

        plays_dataframe = plays_dataframe.replace(to_replace={player1_id.upper(): 0,
                                                              player2_id.upper(): 0,
                                                              player3_id.upper(): 0},
                                                  value=np.nan)
        return plays_dataframe

    def _move_team_id_to_correct_column(self, plays_dataframe):
        """In certain instances, like a turnover credited to a team, a team ID might show up in a player ID column.
        This can cause foreign key constraint issues, and the team ID must be moved to the correct column."""

        def move_team_id_if_in_player_column(row):

            team_ids = TEAMS

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
        """In rare cases, coaches or referees who may be retired players still tracked in the database have their
        player ID appear in the play by play data. However, when this happens, the player name is not
        usually reported, which can cause confusion. In this instance, the player ID in question is set to null."""

        plays_dataframe.loc[plays_dataframe[player1_name.upper()].isnull(), player1_id.upper()] = np.nan
        plays_dataframe.loc[plays_dataframe[player2_name.upper()].isnull(), player2_id.upper()] = np.nan
        plays_dataframe.loc[plays_dataframe[player3_name.upper()].isnull(), player3_id.upper()] = np.nan
        return plays_dataframe

    def _fix_data_types(self, plays_dataframe):
        """Fixes all data types before inserting into the database."""

        plays_dataframe[game_id] = plays_dataframe[game_id].astype('Int64')

        plays_dataframe = plays_dataframe.replace(to_replace={scoremargin: 'TIE'}, value='0')
        plays_dataframe[scoremargin] = plays_dataframe[scoremargin].astype('Int64')

        plays_dataframe[player1_id.upper()] = plays_dataframe[player1_id.upper()].astype('Int64')
        plays_dataframe[player2_id.upper()] = plays_dataframe[player2_id.upper()].astype('Int64')
        plays_dataframe[player3_id.upper()] = plays_dataframe[player3_id.upper()].astype('Int64')

        plays_dataframe[player1_team_id.upper()] = plays_dataframe[player1_team_id.upper()].astype('Int64')
        plays_dataframe[player2_team_id.upper()] = plays_dataframe[player2_team_id.upper()].astype('Int64')
        plays_dataframe[player3_team_id.upper()] = plays_dataframe[player3_team_id.upper()].astype('Int64')

        plays_dataframe.columns = plays_dataframe.columns.str.lower()
        return plays_dataframe
