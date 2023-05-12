from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Float, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base
from config import PGUSER, PGHOST, PGPASSWORD, PGDATABASE

# Create Engine Object
port = 5432
connection_string = f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{port}/{PGDATABASE}'
engine = create_engine(connection_string)

# Create declarative base object
Base = declarative_base()


class Players(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, autoincrement=False)
    full_name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean)


class Teams(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, autoincrement=False)
    full_name = Column(String)
    abbreviation = Column(String)
    nickname = Column(String)
    city = Column(String)
    state = Column(String)
    year_founded = Column(Integer)


class Games(Base):
    __tablename__ = 'games'

    season_id = Column(Integer)
    team_id_h = Column(Integer, ForeignKey('teams.id'))
    team_abbreviation_h = Column(String)
    team_name_h = Column(String)
    game_id = Column(Integer, primary_key=True, autoincrement=False)
    game_date = Column(DateTime)
    matchup_h = Column(String)
    wl_h = Column(String)
    min_h = Column(Integer)
    pts_h = Column(Integer)
    fgm_h = Column(Integer)
    fga_h = Column(Integer)
    fg_pct_h = Column(Float)
    fg3m_h = Column(Integer)
    fg3a_h = Column(Integer)
    fg3_pct_h = Column(Float)
    ftm_h = Column(Integer)
    fta_h = Column(Integer)
    ft_pct_h = Column(Float)
    oreb_h = Column(Integer)
    dreb_h = Column(Integer)
    reb_h = Column(Integer)
    ast_h = Column(Integer)
    stl_h = Column(Integer)
    blk_h = Column(Integer)
    tov_h = Column(Integer)
    pf_h = Column(Integer)
    plus_minus_h = Column(Integer)
    team_id_a = Column(Integer, ForeignKey('teams.id'))
    team_abbreviation_a = Column(String)
    team_name_a = Column(String)
    matchup_a = Column(String)
    wl_a = Column(String)
    min_a = Column(Integer)
    pts_a = Column(Integer)
    fgm_a = Column(Integer)
    fga_a = Column(Integer)
    fg_pct_a = Column(Float)
    fg3m_a = Column(Integer)
    fg3a_a = Column(Integer)
    fg3_pct_a = Column(Float)
    ftm_a = Column(Integer)
    fta_a = Column(Integer)
    ft_pct_a = Column(Float)
    oreb_a = Column(Integer)
    dreb_a = Column(Integer)
    reb_a = Column(Integer)
    ast_a = Column(Integer)
    stl_a = Column(Integer)
    blk_a = Column(Integer)
    tov_a = Column(Integer)
    pf_a = Column(Integer)
    plus_minus_a = Column(Integer)


class Plays(Base):
    __tablename__ = 'plays'

    play_id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('games.game_id'))
    eventnum = Column(Integer)
    eventmsgtype = Column(Integer)
    eventmsgactiontype = Column(Integer)
    period = Column(Integer)
    wctimestring = Column(String)
    pctimestring = Column(String)
    homedescription = Column(String)
    neutraldescription = Column(String)
    visitordescription = Column(String)
    score = Column(String)
    scoremargin = Column(Integer)
    person1type = Column(Integer)
    player1_id = Column(Integer, ForeignKey('players.id'))
    player1_name = Column(String)
    player1_team_id = Column(Integer, ForeignKey('teams.id'))
    player1_team_city = Column(String)
    player1_team_nickname = Column(String)
    player1_team_abbreviation = Column(String)
    person2type = Column(Integer)
    player2_id = Column(Integer, ForeignKey('players.id'))
    player2_name = Column(String)
    player2_team_id = Column(Integer, ForeignKey('teams.id'))
    player2_team_city = Column(String)
    player2_team_nickname = Column(String)
    player2_team_abbreviation = Column(String)
    person3type = Column(Integer)
    player3_id = Column(Integer, ForeignKey('players.id'))
    player3_name = Column(String)
    player3_team_id = Column(Integer, ForeignKey('teams.id'))
    player3_team_city = Column(String)
    player3_team_nickname = Column(String)
    player3_team_abbreviation = Column(String)
    video_available_flag = Column(Integer)


class PlayTypes(Base):
    __tablename__ = 'play_types'

    eventmsgtype = Column(Integer, primary_key=True, nullable=False)
    eventmsgactiontype = Column(Integer, nullable=False)
    eventmsgtype_description = Column(String)
    eventmsgactiontype_description = Column(String)


if __name__ == "__main__":
    Base.metadata.create_all(engine)