import unittest
from pandas.testing import assert_frame_equal
import pandas as pd
from play_by_play import PlayByPlay
from config import dtypes


class TestPlays(unittest.TestCase):

    def setUp(self) -> None:
        directory = 'test_data'
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
        self.playbyplay = PlayByPlay(dataframes, 0)
        self.test_data_0 = pd.read_csv(directory + '/test_play_by_play_data.csv',
                                       index_col=0,
                                       dtype=dtypes)
        self.test_data_1 = pd.read_csv(directory + '/test_play_by_play_data_with_play_id.csv',
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
                                       index_col=0,
                                       dtype=dtypes)

    def test_build_raw_dataframe(self):
        result = self.playbyplay._build_raw_dataframe()
        assert_frame_equal(result, self.test_data_0)
        print('Build raw dataframe test passed!')

    def test_add_play_id(self):
        result = self.playbyplay._add_play_id()
        assert_frame_equal(result, self.test_data_1)
        print('Add play ID test passed!')

    def test_nullify_zero_player_id(self):
        result = self.playbyplay._nullify_zero_player_id(self.test_data_1)
        assert_frame_equal(result, self.test_data_2)
        print('Nullify zero player ID test passed!')

    def test_move_team_id_to_correct_column(self):
        result = self.playbyplay._move_team_id_to_correct_column(self.test_data_2)
        assert_frame_equal(result, self.test_data_3)
        print('Move team ID test passed!')

    def test_nullify_empty_player_names(self):
        result = self.playbyplay._nullify_empty_player_names(self.test_data_3)
        assert_frame_equal(result, self.test_data_4)
        print('Nullify empty player names test passed!')

    def test_fix_data_types(self):
        result = self.playbyplay._fix_data_types(self.test_data_4)
        assert_frame_equal(result, self.test_data_5)
        print('Fix data types test passed!')

    def test_clean_data(self):
        result = self.playbyplay.get_plays()
        assert_frame_equal(result, self.test_data_5)
        print('Get plays dataframe test passed!')


if __name__ == "__main__":
    unittest.main()
