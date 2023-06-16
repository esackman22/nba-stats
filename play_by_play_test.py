import unittest
from pandas.testing import assert_frame_equal
import pandas as pd
from play_by_play import PlayByPlay
from constants import dtypes


class TestPlays(unittest.TestCase):

    def setUp(self) -> None:
        directory = 'test_directory'
        self.row_1 = pd.read_csv(directory + '/row_1.csv',
                                 index_col=0,
                                 dtype=dtypes)
        self.row_2 = pd.read_csv(directory + '/row_2.csv',
                                 index_col=0,
                                 dtype=dtypes)
        self.row_3 = pd.read_csv(directory + '/row_3.csv',
                                 index_col=0,
                                 dtype=dtypes)
        self.row_4 = pd.read_csv(directory + '/row_4.csv',
                                 index_col=0,
                                 dtype=dtypes)
        self.row_5 = pd.read_csv(directory + '/row_5.csv',
                                 index_col=0,
                                 dtype=dtypes)
        self.row_6 = pd.read_csv(directory + '/row_6.csv',
                                 index_col=0,
                                 dtype=dtypes)
        dataframes = [self.row_1, self.row_2, self.row_3, self.row_4, self.row_5, self.row_6]
        self.playbyplay = PlayByPlay(dataframes)
        self.test_data_0 = pd.read_csv(directory + '/test_play_by_play_data.csv',
                                       index_col=0,
                                       dtype=dtypes)
        self.test_data_2 = pd.read_csv(directory + '/test_data_zero_player_id_null.csv',
                                       index_col=0,
                                       dtype=dtypes)
        self.test_data_3 = pd.read_csv(directory + '/test_data_move_team_id.csv',
                                       index_col=0,
                                       dtype=dtypes)
        self.test_data_4 = pd.read_csv(directory + '/test_data_null_empty_player_name.csv',
                                       index_col=0,
                                       dtype=dtypes)
        self.test_data_5 = pd.read_csv(directory + '/test_play_by_play_data_final.csv',
                                       index_col=0)
        self.test_data_5['GAME_ID'] = self.test_data_5['GAME_ID'].astype('Int64')
        self.test_data_5['SCOREMARGIN'] = self.test_data_5['SCOREMARGIN'].astype('Int64')
        self.test_data_5['PLAYER1_ID'] = self.test_data_5['PLAYER1_ID'].astype('Int64')
        self.test_data_5['PLAYER2_ID'] = self.test_data_5['PLAYER2_ID'].astype('Int64')
        self.test_data_5['PLAYER3_ID'] = self.test_data_5['PLAYER3_ID'].astype('Int64')
        self.test_data_5['PLAYER1_TEAM_ID'] = self.test_data_5['PLAYER1_TEAM_ID'].astype('Int64')
        self.test_data_5['PLAYER2_TEAM_ID'] = self.test_data_5['PLAYER2_TEAM_ID'].astype('Int64')
        self.test_data_5['PLAYER3_TEAM_ID'] = self.test_data_5['PLAYER3_TEAM_ID'].astype('Int64')
        self.test_data_5.columns = self.test_data_5.columns.str.lower()

    def test_build_raw_dataframe(self):
        result = self.playbyplay._build_raw_dataframe()
        assert_frame_equal(result, self.test_data_0)

    def test_nullify_zero_player_id(self):
        result = self.playbyplay._nullify_zero_player_id(self.test_data_0)
        assert_frame_equal(result, self.test_data_2)

    def test_move_team_id_to_correct_column(self):
        result = self.playbyplay._move_team_id_to_correct_column(self.test_data_2)
        assert_frame_equal(result, self.test_data_3)

    def test_nullify_empty_player_names(self):
        result = self.playbyplay._nullify_empty_player_names(self.test_data_3)
        assert_frame_equal(result, self.test_data_4)

    def test_fix_data_types(self):
        result = self.playbyplay._fix_data_types(self.test_data_4)
        assert_frame_equal(result, self.test_data_5)

    def test_clean_data(self):
        result = self.playbyplay.clean_and_return_plays()
        assert_frame_equal(result, self.test_data_5)


if __name__ == "__main__":
    unittest.main()
