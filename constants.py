play_by_play_columns = ['GAME_ID', 'EVENTNUM', 'EVENTMSGTYPE', 'EVENTMSGACTIONTYPE', 'PERIOD',
                        'WCTIMESTRING', 'PCTIMESTRING', 'HOMEDESCRIPTION', 'NEUTRALDESCRIPTION',
                        'VISITORDESCRIPTION', 'SCORE', 'SCOREMARGIN', 'PERSON1TYPE',
                        'PLAYER1_ID', 'PLAYER1_NAME', 'PLAYER1_TEAM_ID', 'PLAYER1_TEAM_CITY',
                        'PLAYER1_TEAM_NICKNAME', 'PLAYER1_TEAM_ABBREVIATION', 'PERSON2TYPE',
                        'PLAYER2_ID', 'PLAYER2_NAME', 'PLAYER2_TEAM_ID', 'PLAYER2_TEAM_CITY',
                        'PLAYER2_TEAM_NICKNAME', 'PLAYER2_TEAM_ABBREVIATION', 'PERSON3TYPE',
                        'PLAYER3_ID', 'PLAYER3_NAME', 'PLAYER3_TEAM_ID', 'PLAYER3_TEAM_CITY',
                        'PLAYER3_TEAM_NICKNAME', 'PLAYER3_TEAM_ABBREVIATION',
                        'VIDEO_AVAILABLE_FLAG']

players_columns = ['id', 'full_name', 'first_name', 'last_name', 'is_active']
TEAMS = [1610612737, 1610612738, 1610612739, 1610612740, 1610612741, 1610612742, 1610612743, 1610612744, 1610612745,
         1610612746, 1610612747, 1610612748, 1610612749, 1610612750, 1610612751, 1610612752, 1610612753, 1610612754,
         1610612755, 1610612756, 1610612757, 1610612758, 1610612759, 1610612760, 1610612761, 1610612762, 1610612763,
         1610612764, 1610612765, 1610612766]

dtypes = {'GAME_ID': str,
          'EVENTNUM': int,
          'SCOREMARGIN': str}

player1_id = 'player1_id'
player2_id = 'player2_id'
player3_id = 'player3_id'
player1_name = 'player1_name'
player2_name = 'player2_name'
player3_name = 'player3_name'
player1_team_id = 'player1_team_id'
player2_team_id = 'player2_team_id'
player3_team_id = 'player3_team_id'

game_id = 'GAME_ID'
season_id = 'SEASON_ID'
game_date = 'GAME_DATE'
scoremargin = 'SCOREMARGIN'