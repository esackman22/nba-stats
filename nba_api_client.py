from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import SeasonTypeAllStarNullable
from nba_api.stats.endpoints import playbyplayv2
import time


class NbaApiClient:

    def __init__(self, from_date, to_date, season_type=SeasonTypeAllStarNullable.regular, league_id='00'):
        self.league_id = league_id
        self.season_type = season_type
        self.to_date = to_date
        self.from_date = from_date

    def retrieve_and_return_games_df(self):
        return self._retrieve_games()

    def _create_game_finder(self):

        game_finder = leaguegamefinder.LeagueGameFinder(date_from_nullable=self.from_date,
                                                        date_to_nullable=self.to_date,
                                                        season_type_nullable=self.season_type,
                                                        league_id_nullable=self.league_id)
        return game_finder

    def _retrieve_games(self):

        game_finder = self._create_game_finder()
        return game_finder.get_data_frames()[0]

    def retrieve_and_return_plays_dfs(self, game_ids):

        raw_plays_dfs = []
        if game_ids:

            for game_id in game_ids:
                pbp = playbyplayv2.PlayByPlayV2(game_id)
                raw_plays_dfs.append(pbp.get_data_frames()[0])
                time.sleep(0.5)

        return raw_plays_dfs

