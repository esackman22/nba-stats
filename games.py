import pandas as pd


class Games:
    """Clean games data extracted from API and transform it to be ready for insertion into DB
    """

    def __init__(self, data):

        self.data = data

    def _combine_team_games(self):
        """Combine a TEAM_ID-GAME_ID unique table into rows by game.

                Parameters
                ----------
                self._retrieve_games() : Retrieves input DataFrame.

                Returns
                -------
                result : DataFrame
        """
        # Join every row to all others with the same game ID.
        raw_games = self.data

        joined = pd.merge(raw_games,
                          raw_games,
                          suffixes=('_H', '_A'),
                          on=['SEASON_ID', 'GAME_ID', 'GAME_DATE'])

        # Filter out any row that is joined to itself.
        result = joined[joined.TEAM_ID_H != joined.TEAM_ID_A]

        # Take action based on the keep_method flag.
        result = result[result.MATCHUP_H.str.contains(' vs. ')]

        return result

    def _clean_games_data(self):
        """Combines home and away rows for a game into a single row and converts season and game
        ID columns to integer. Also makes column names all lowercase."""

        data = self._combine_team_games()
        data['SEASON_ID'] = data['SEASON_ID'].apply(lambda x: int(x))
        data['GAME_ID'] = data['GAME_ID'].apply(lambda x: int(x))
        data.columns = data.columns.str.lower()

        return data

    def clean_and_return_games_df(self):

        dataframe = self._clean_games_data()
        return dataframe

    def to_csv(self):
        to_date = self.to_date.replace('/', '-')
        from_date = self.from_date.replace('/', '-')
        filepath = 'games/' + from_date + '_to_' + to_date + '.csv'
        print(filepath)
        dataframe = self.get_games()
        dataframe.to_csv(filepath)
