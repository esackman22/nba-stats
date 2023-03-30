from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import SeasonTypeAllStarNullable
import pandas as pd
from connect import Connector


class Games:
    """Extract games data from API and transform it to be ready for insertion into DB
    """

    def __init__(self,
                 from_date='01/01/2023',
                 to_date='01/01/2023',
                 season_type=SeasonTypeAllStarNullable.regular,
                 league_id='00'):

        self.from_date = from_date
        self.to_date = to_date
        self.season_type = season_type
        self.league_id = league_id

    def _create_game_finder(self):
        """Instantiates the LeagueGameFinderClass with the instance variables filled in.
        """

        game_finder = leaguegamefinder.LeagueGameFinder(date_from_nullable=self.from_date,
                                                        date_to_nullable=self.to_date,
                                                        season_type_nullable=self.season_type,
                                                        league_id_nullable=self.league_id)
        return game_finder

    def _retrieve_games(self):
        """Retrieves games from the nba_api using the game finder instance created in the
        _create_game_finder method.
        """
        game_finder = self._create_game_finder()
        return game_finder.get_data_frames()[0]

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
        raw_games = self._retrieve_games()

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

        data = self._combine_team_games()
        data['SEASON_ID'] = data['SEASON_ID'].apply(lambda x: int(x))
        data['GAME_ID'] = data['GAME_ID'].apply(lambda x: int(x))

        return data

    def get_games(self):

        dataframe = self._clean_games_data()
        return dataframe

    def to_csv(self):
        to_date = self.to_date.replace('/', '-')
        from_date = self.from_date.replace('/', '-')
        filepath = 'games/' + from_date + '_to_' + to_date + '.csv'
        print(filepath)
        dataframe = self.get_games()
        dataframe.to_csv(filepath)


if __name__ == "__main__":
    games = Games()
    games.get_games()
    games.to_csv()
