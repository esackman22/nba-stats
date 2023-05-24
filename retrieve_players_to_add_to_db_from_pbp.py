import pandas as pd
from player_comparator import PlayerComparator
from sqlalchemy.orm import sessionmaker
from models import Players


def retrieve_and_return_players_to_add(engine, play_by_play_data):
    cur_session = sessionmaker(bind=engine)
    session = cur_session()
    query = session.query(Players)
    stmt = query.statement
    existing_players_dataframe = pd.read_sql(stmt, session.connection())
    comparator = PlayerComparator()
    players_to_add = comparator.compare_to_existing(existing_players_dataframe, plays)
    return players_to_add