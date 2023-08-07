Context and Scope:</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span>The NBA exposes numerous undocumented API endpoints from which one can access a wide variety of statistical data. This could be useful for many applications, including analysis and the building of machine learning models by interested parties. An </span><span class="c14"><a class="c22" href="https://www.google.com/url?q=https://github.com/swar/nba_api&amp;sa=D&amp;source=editors&amp;ust=1691423213696517&amp;usg=AOvVaw3jG13zXfs1kcwlCPGuBGm7">open source package</a></span><span class="c1">&nbsp;was built in an attempt to document these endpoints and provide better access to this data.</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c1">One of the endpoints documented by this package allows a user to pass in a game ID and retrieve play by play data, one line per play, in the form of a pandas dataframe. While valuable data, the need to possess a specific game ID, combined with rate limiting on the part of the NBA, can make any analysis a time consuming and labor intensive process.</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c1">For example, say that one wanted to retrieve all of the instances of a jump ball involving a certain player (jump balls are not usually tracked in any form other than in play by play data). This would require first obtaining all the game ID&rsquo;s for whatever date range is being looked at, followed by iterating over each game, isolating jump ball occurrences, and then concatenating data. </span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c1">If a project involved analyses of many different play types, players, teams, or date ranges, these limitations could require more time and resources than would otherwise be expected or desired. As such, a standardized database on which queries can be run using the parameters mentioned above could dramatically reduce the time spent retrieving and cleaning data, allowing users to focus on their own tasks and goals.</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c3">Goals:</span></p><ul class="c17 lst-kix_ej719cz6l4jx-0 start"><li class="c0 c16 li-bullet-0"><span class="c1">Implement a data pipeline that can automatically extract, clean, process, and write play by play data to a standardized database.</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Build an API that allows for queries to be run against the database that can be filtered based on various parameters.</span></li></ul><p class="c0 c13 c26"><span class="c1"></span></p><p class="c0 c13 c26"><span class="c1"></span></p><p class="c0"><span class="c3">Data Flow Diagram:</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 132.00px;"><img alt="" src="images/image2.png" style="width: 624.00px; height: 132.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" title=""></span></p><p class="c0"><span class="c1">Data is extracted from the NBA API, processed in the pipeline, written to the project database, and then accessed by end users with the project API.</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c3">Data Pipeline Diagram:</span></p><p class="c0"><span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 293.33px;"><img alt="" src="images/image1.png" style="width: 624.00px; height: 293.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" title=""></span></p><p class="c0"><span class="c1">Every morning, raw games data from the previous night of basketball games is extracted from the NBA API. Games are represented in two rows, one for statistics from the home team, and one for statistics from the away team. By joining these two rows on the game ID, they are combined into one row and written to the database.</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c1">From the games data, a list of game ID&rsquo;s is pulled. These game IDs are used to retrieve raw play by play data from each game, which gets concatenated into a single dataframe. Then, the data is cleaned and reformatted into processed play by play data, ready to be written to the database. </span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c1">Sometimes, at the beginning of a season or towards the end, new players that are not present in the database appear for the first time in the play by play data. Before the play by play data can be written to the database, these new players (if they exist in the data for that day) must be extracted from the play by play data and written to the players table of the database.</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c3">Database Schema:</span></p><p class="c0 c13"><span class="c3"></span></p><p class="c0"><span class="c1">The database consists of 4 tables: Games, Players, Plays, and Teams</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c21">Games:</span></p><ul class="c17 lst-kix_jhmswzs4ukmb-0 start"><li class="c0 c16 li-bullet-0"><span class="c1">Primary Key: Game ID</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Foreign Keys: Team IDs</span></li></ul><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c19">Players:</span></p><ul class="c17 lst-kix_r00l4b6th6se-0 start"><li class="c0 c16 li-bullet-0"><span class="c1">Primary Key: Player ID</span></li></ul><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c19">Teams:</span></p><ul class="c17 lst-kix_ttyroh6gxgk6-0 start"><li class="c0 c16 li-bullet-0"><span class="c1">Primary Key: Team ID</span></li></ul><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c19">Plays:</span></p><ul class="c17 lst-kix_5zkjfb5fxsh4-0 start"><li class="c0 c16 li-bullet-0"><span class="c1">Primary Key: Play ID</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Foreign Keys: Game ID, Team IDs, Player IDs</span></li></ul><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c1">When data is written to the table, it must be written in the following order to ensure data integrity:</span></p><ol class="c17 lst-kix_a1lddp9itr0n-0 start" start="1"><li class="c0 c16 li-bullet-0"><span class="c1">Teams (in case of league expansion, extremely rare)</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Games </span></li><li class="c0 c16 li-bullet-0"><span class="c1">Players (if necessary)</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Plays</span></li></ol><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c12">API Design:</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c1">The API consists of a single endpoint that allows for GET HTTP requests by authorized users. These users may filter their query based on various parameters. </span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span>API Base URL: </span><span class="c14"><a class="c22" href="https://www.google.com/url?q=https://frh5etghs5kzsmppofo7zjehby0zratt.lambda-url.us-east-1.on.aws/&amp;sa=D&amp;source=editors&amp;ust=1691423213702013&amp;usg=AOvVaw3wt3RWn1vde79sYn2KEaEa">https://frh5etghs5kzsmppofo7zjehby0zratt.lambda-url.us-east-1.on.aws/</a></span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c1">Query Parameters:</span></p><ul class="c17 lst-kix_ld930ajv1hm9-0 start"><li class="c0 c16 li-bullet-0"><span class="c1">Game ID: a foreign key referencing a game stored in the Games table</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Period: which period (1, 2, 3, 4, 5+ for Overtimes)</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Score Margin: the difference in the score for home and away teams</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player 1, 2, or 3 ID: a foreign key referencing a player stored in the Players table</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player 1, 2, or 3 name: the full name in title case of the player involved in the play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player 1, 2, or 3 team nickname: the nickname (e.g. Celtics) of the team of the player involved in the play</span></li></ul><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c1">API Output:</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c1">The API will take in the query parameters and then return a list of plays in JSON format that match those query parameters (if they exist). The Play model, shown below, describes the data that will be returned by the API request.</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c1">Play Model:</span></p><ul class="c17 lst-kix_h7uclas9n4mg-0 start"><li class="c0 c16 li-bullet-0"><span class="c1">Play ID (Primary Key): Serialized unique identifier for each play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Game ID: Foreign key reference to Games table</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Eventnum: a unique identifier for each play within a given game</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Eventmsgtype: the type of play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Eventmsgactiontype: play subtype</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Period: which quarter/overtime the play occurred in</span></li><li class="c0 c16 li-bullet-0"><span class="c1">WCtimestring: the time at which the play occurred (Pacific time zone)</span></li><li class="c0 c16 li-bullet-0"><span class="c1">PCtimestring: the time remaining on the game clock when the play occurred</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Homedescription: a qualitative description of the play involving a home team player</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Neutraldescription: a qualitative description of the play involving neutral parties (referees)</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Visitordescription: a qualitative description of the play involving a visiting team player</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Score: the current score of the game, stored as a string, the home team score first</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Scoremargin: the difference between the score of the home and visiting team</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Person1Type: the type of player, usually 4 for a home player and a 5 for the away player</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player1_id: Foreign key reference to a player in the Players table</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player1_name: Full name of the primary player involved in the play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player1_team_id: Foreign key reference to the team corresponding to the primary player involved in the play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player1_team_city: City in which the team corresponding to the primary player involved in the play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player1_team_nickname: Nickname of the team corresponding to the primary player involved in the play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player1_team_abbreviation: Abbreviation, as shown on scoreboards, of the team corresponding to the primary player involved in the play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Person2Type: the type of player, usually 4 for a home player and a 5 for the away player</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player2_id: Foreign key reference to a player in the Players table</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player2_name: Full name of the secondary player involved in the play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player2_team_id: Foreign key reference to the team corresponding to the secondary player involved in the play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player2_team_city: City in which the team corresponding to the secondary player involved in the play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player2_team_nickname: Nickname of the team corresponding to the secondary player involved in the play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player2_team_abbreviation: Abbreviation, as shown on scoreboards, of the team corresponding to the secondary player involved in the play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Person3Type: the type of player, usually 4 for a home player and a 5 for the away player</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player3_id: Foreign key reference to a player in the Players table</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player3_name: Full name of the tertiary player involved in the play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player3_team_id: Foreign key reference to the team corresponding to the tertiary player involved in the play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player3_team_city: City in which the team corresponding to the tertiary player involved in the play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player3_team_nickname: Nickname of the team corresponding to the tertiary player involved in the play</span></li><li class="c0 c16 li-bullet-0"><span class="c1">Player3_team_abbreviation: Abbreviation, as shown on scoreboards, of the team corresponding to the tertiary player involved in the play</span></li><li class="c0 c16 li-bullet-0"><span>VideoAvailableFlag: A boolean that references whether the NBA has a video highlight available for the play.</span></li></ul><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c19">Example get request 1: </span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c1">https://frh5etghs5kzsmppofo7zjehby0zratt.lambda-url.us-east-1.on.aws/?eventmsgtype=1&amp;period=3&amp;player1_name=Brook Lopez&amp;player2_name=Jrue Holiday</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c1">The above query represents a search for made field goals by Brook Lopez, assisted by Jrue Holiday, occurring in the 3rd period. Below is one of the rows (with each row representing one play) from the response, returned in JSON format:</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c7"><span class="c5">{</span></p><p class="c4"><span class="c10 c9">&quot;play_id&quot;</span><span class="c9">: </span><span class="c2">1673437</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;game_id&quot;</span><span class="c9">: </span><span class="c2">22000051</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;eventnum&quot;</span><span class="c9">: </span><span class="c2">375</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;eventmsgtype&quot;</span><span class="c9">: </span><span class="c2">1</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;eventmsgactiontype&quot;</span><span class="c9">: </span><span class="c2">1</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;period&quot;</span><span class="c9">: </span><span class="c2">3</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;wctimestring&quot;</span><span class="c9">: </span><span class="c8">&quot;9:02 PM&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;pctimestring&quot;</span><span class="c9">: </span><span class="c8">&quot;9:22&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;homedescription&quot;</span><span class="c9">: </span><span class="c8 c12">null</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;neutraldescription&quot;</span><span class="c9">: </span><span class="c8 c12">null</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;visitordescription&quot;</span><span class="c9">: </span><span class="c8">&quot;Lopez 24&#39; 3PT Jump Shot (14 PTS) (Holiday 7 AST)&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;score&quot;</span><span class="c9">: </span><span class="c8">&quot;88 - 56&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;scoremargin&quot;</span><span class="c9">: </span><span class="c2">-32</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;person1type&quot;</span><span class="c9">: </span><span class="c2">5</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player1_id&quot;</span><span class="c9">: </span><span class="c2">201572</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player1_name&quot;</span><span class="c9">: </span><span class="c8">&quot;Brook Lopez&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player1_team_id&quot;</span><span class="c9">: </span><span class="c2">1610612749</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player1_team_city&quot;</span><span class="c9">: </span><span class="c8">&quot;Milwaukee&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player1_team_nickname&quot;</span><span class="c9">: </span><span class="c8">&quot;Bucks&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player1_team_abbreviation&quot;</span><span class="c9">: </span><span class="c8">&quot;MIL&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;person2type&quot;</span><span class="c9">: </span><span class="c2">5</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player2_id&quot;</span><span class="c9">: </span><span class="c2">201950</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player2_name&quot;</span><span class="c9">: </span><span class="c8">&quot;Jrue Holiday&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player2_team_id&quot;</span><span class="c9">: </span><span class="c2">1610612749</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player2_team_city&quot;</span><span class="c9">: </span><span class="c8">&quot;Milwaukee&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player2_team_nickname&quot;</span><span class="c9">: </span><span class="c8">&quot;Bucks&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player2_team_abbreviation&quot;</span><span class="c9">: </span><span class="c8">&quot;MIL&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;person3type&quot;</span><span class="c9">: </span><span class="c2">0</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player3_id&quot;</span><span class="c9">: </span><span class="c8 c12">null</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player3_name&quot;</span><span class="c9">: </span><span class="c8 c12">null</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player3_team_id&quot;</span><span class="c9">: </span><span class="c8 c12">null</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player3_team_city&quot;</span><span class="c9">: </span><span class="c8 c12">null</span></p><p class="c4"><span class="c10 c9">&quot;player3_team_nickname&quot;</span><span class="c9">: </span><span class="c8 c12">null</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player3_team_abbreviation&quot;</span><span class="c9">: </span><span class="c8 c12">null</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;video_available_flag&quot;</span><span class="c9">: </span><span class="c2">1</span><span class="c9">,</span></p><p class="c7"><span class="c9">}</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c19">Example get request 2:</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c1">https://frh5etghs5kzsmppofo7zjehby0zratt.lambda-url.us-east-1.on.aws/?eventmsgtype=10&amp;player1_name=Al Horford&amp;player2_name=Nikola Vucevic</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c1">The above query filters for jump balls between Al Horford and Nikola Vucevic, where Horford is on the home team and Vucevic the away team. Below is one of the rows (with each row representing one play) of the response in JSON format:</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c7"><span class="c5">{</span></p><p class="c4"><span class="c10 c9">&quot;play_id&quot;</span><span class="c9">: </span><span class="c2">584389</span><span class="c5">,</span></p><p class="c4"><span class="c9 c10">&quot;game_id&quot;</span><span class="c9">: </span><span class="c2">21800040</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;eventnum&quot;</span><span class="c9">: </span><span class="c2">4</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;eventmsgtype&quot;</span><span class="c9">: </span><span class="c2">10</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;eventmsgactiontype&quot;</span><span class="c9">: </span><span class="c2">0</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;period&quot;</span><span class="c9">: </span><span class="c2">1</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;wctimestring&quot;</span><span class="c9">: </span><span class="c8">&quot;7:41 PM&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;pctimestring&quot;</span><span class="c9">: </span><span class="c8">&quot;12:00&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;homedescription&quot;</span><span class="c9">: </span><span class="c8">&quot;Jump Ball Horford vs. Vucevic: Tip to Hayward&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;neutraldescription&quot;</span><span class="c9">: </span><span class="c8 c12">null</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;visitordescription&quot;</span><span class="c9">: </span><span class="c8 c12">null</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;score&quot;</span><span class="c9">: </span><span class="c8 c12">null</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;scoremargin&quot;</span><span class="c9">: </span><span class="c8 c12">null</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;person1type&quot;</span><span class="c9">: </span><span class="c2">4</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player1_id&quot;</span><span class="c9">: </span><span class="c2">201143</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player1_name&quot;</span><span class="c9">: </span><span class="c8">&quot;Al Horford&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player1_team_id&quot;</span><span class="c9">: </span><span class="c2">1610612738</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player1_team_city&quot;</span><span class="c9">: </span><span class="c8">&quot;Boston&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player1_team_nickname&quot;</span><span class="c9">: </span><span class="c8">&quot;Celtics&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player1_team_abbreviation&quot;</span><span class="c9">: </span><span class="c8">&quot;BOS&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;person2type&quot;</span><span class="c9">: </span><span class="c2">5</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player2_id&quot;</span><span class="c9">: </span><span class="c2">202696</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player2_name&quot;</span><span class="c9">: </span><span class="c8">&quot;Nikola Vucevic&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player2_team_id&quot;</span><span class="c9">: </span><span class="c2">1610612753</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player2_team_city&quot;</span><span class="c9">: </span><span class="c8">&quot;Orlando&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player2_team_nickname&quot;</span><span class="c9">: </span><span class="c8">&quot;Magic&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player2_team_abbreviation&quot;</span><span class="c9">: </span><span class="c8">&quot;ORL&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;person3type&quot;</span><span class="c9">: </span><span class="c2">4</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player3_id&quot;</span><span class="c9">: </span><span class="c2">202330</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player3_name&quot;</span><span class="c9">: </span><span class="c8">&quot;Gordon Hayward&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player3_team_id&quot;</span><span class="c9">: </span><span class="c2">1610612738</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player3_team_city&quot;</span><span class="c9">: </span><span class="c8">&quot;Boston&quot;</span></p><p class="c4"><span class="c10 c9">&quot;player3_team_nickname&quot;</span><span class="c9">: </span><span class="c8">&quot;Celtics&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;player3_team_abbreviation&quot;</span><span class="c9">: </span><span class="c8">&quot;BOS&quot;</span><span class="c5">,</span></p><p class="c4"><span class="c10 c9">&quot;video_available_flag&quot;</span><span class="c9">: </span><span class="c2">1</span><span class="c9">,</span></p><p class="c7"><span class="c5">}</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c1">Note on the &ldquo;eventmsgtype&rdquo; field: this refers to a play type and is very useful when querying the database for specific data. The table below summarizes each of the play types.</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0 c13"><span class="c1"></span></p><a id="t.aefc776c7c197a5b8f3e7e380a3e4f013b475552"></a><a id="t.0"></a><table class="c23"><tr class="c15"><td class="c18" colspan="1" rowspan="1"><p class="c6"><span class="c3">EventMsgType</span></p></td><td class="c11" colspan="1" rowspan="1"><p class="c6"><span class="c3">Meaning</span></p></td></tr><tr class="c15"><td class="c18" colspan="1" rowspan="1"><p class="c6"><span class="c1">1</span></p></td><td class="c11" colspan="1" rowspan="1"><p class="c6"><span class="c1">Field Goal Made</span></p></td></tr><tr class="c15"><td class="c18" colspan="1" rowspan="1"><p class="c6"><span class="c1">2</span></p></td><td class="c11" colspan="1" rowspan="1"><p class="c6"><span class="c1">Field Goal Missed</span></p></td></tr><tr class="c15"><td class="c18" colspan="1" rowspan="1"><p class="c6"><span class="c1">3</span></p></td><td class="c11" colspan="1" rowspan="1"><p class="c6"><span class="c1">Free Throw Attempt</span></p></td></tr><tr class="c15"><td class="c18" colspan="1" rowspan="1"><p class="c6"><span class="c1">4</span></p></td><td class="c11" colspan="1" rowspan="1"><p class="c6"><span class="c1">Rebound</span></p></td></tr><tr class="c15"><td class="c18" colspan="1" rowspan="1"><p class="c6"><span class="c1">5</span></p></td><td class="c11" colspan="1" rowspan="1"><p class="c6"><span class="c1">Turnover</span></p></td></tr><tr class="c15"><td class="c18" colspan="1" rowspan="1"><p class="c6"><span class="c1">6</span></p></td><td class="c11" colspan="1" rowspan="1"><p class="c6"><span class="c1">Foul</span></p></td></tr><tr class="c15"><td class="c18" colspan="1" rowspan="1"><p class="c6"><span class="c1">7</span></p></td><td class="c11" colspan="1" rowspan="1"><p class="c6"><span class="c1">Violation</span></p></td></tr><tr class="c15"><td class="c18" colspan="1" rowspan="1"><p class="c6"><span class="c1">8</span></p></td><td class="c11" colspan="1" rowspan="1"><p class="c6"><span class="c1">Substitution</span></p></td></tr><tr class="c15"><td class="c18" colspan="1" rowspan="1"><p class="c6"><span class="c1">9</span></p></td><td class="c11" colspan="1" rowspan="1"><p class="c6"><span class="c1">Timeout</span></p></td></tr><tr class="c15"><td class="c18" colspan="1" rowspan="1"><p class="c6"><span class="c1">10</span></p></td><td class="c11" colspan="1" rowspan="1"><p class="c6"><span class="c1">Jump Ball</span></p></td></tr><tr class="c15"><td class="c18" colspan="1" rowspan="1"><p class="c6"><span class="c1">11</span></p></td><td class="c11" colspan="1" rowspan="1"><p class="c6"><span class="c1">Ejection</span></p></td></tr><tr class="c15"><td class="c18" colspan="1" rowspan="1"><p class="c6"><span class="c1">12</span></p></td><td class="c11" colspan="1" rowspan="1"><p class="c6"><span class="c1">Period Begin</span></p></td></tr><tr class="c15"><td class="c18" colspan="1" rowspan="1"><p class="c6"><span class="c1">13</span></p></td><td class="c11" colspan="1" rowspan="1"><p class="c6"><span class="c1">Period End</span></p></td></tr><tr class="c15"><td class="c18" colspan="1" rowspan="1"><p class="c6"><span class="c1">18</span></p></td><td class="c11" colspan="1" rowspan="1"><p class="c6"><span class="c1">Instant Replay Review</span></p></td></tr></table><p class="c0 c13"><span class="c1"></span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0"><span class="c3">Infrastructure:</span></p><p class="c0 c13"><span class="c3"></span></p><p class="c0"><span class="c1">The data pipeline script is automated to run daily using an AWS Lambda function. As the NBA blacklists cloud IP addresses, a VPN must be used. The pipeline is written in Python and utilizes the Pandas library for transformations and data cleaning. It also uses SQLalchemy to interact with the database. The database is a PostgreSQL instance hosted in AWS. Finally, the API is a lambda function written in python that uses SQLalchemy to query the database.</span></p><p class="c0 c13"><span class="c1"></span></p><p class="c0 c13"><span class="c1"></span></p></body></html>
