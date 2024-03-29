from models import Plays, Players, Teams, Games, engine
from sqlalchemy.orm import sessionmaker
import json

# Initialize the database connection
Session = sessionmaker(bind=engine)

# Map columns to query parameters to allow for dynamic query building
column_mappings = {
    'game_id': Plays.game_id,
    'eventmsgtype': Plays.eventmsgtype,
    'period': Plays.period,
    'homedescription': Plays.homedescription,
    'visitordescription': Plays.visitordescription,
    'scoremargin': Plays.scoremargin,
    'player1_id': Plays.player1_id,
    'player1_name': Plays.player1_name,
    'player1_team_nickname': Plays.player1_team_nickname,
    'player2_id': Plays.player2_id,
    'player2_name': Plays.player2_name,
    'player2_team_nickname': Plays.player2_team_nickname,
    'player3_id': Plays.player3_id,
    'player3_name': Plays.player3_name,
    'player3_team_nickname': Plays.player3_team_nickname
}


def validate_query_params(query_params):
    """Input a dictionary of query parameters, output is None if all are valid or
    a tuple of the parameter and its corresponding value if it returns no results."""

    session = Session()
    query = session.query(Plays)

    for param, value in query_params.items():
        if param in column_mappings:
            column = column_mappings[param]
            if isinstance(value, str):
                filtered_query = query.filter(column == value)
                count = filtered_query.count()
            elif isinstance(value, int):
                filtered_query = query.filter(column == value)
                count = filtered_query.count()

            if count == 0:
                return (param, value)
        else:
            return (param, value)

    return None


def build_query_with_filters(query_params, limit=None):
    """Input a dictionary with query parameters and a limit on results if necessary,
    output a list of SQLalchemy objects that are the results of the query."""

    session = Session()
    query = session.query(Plays)

    for param, value in query_params.items():
        if param in column_mappings:
            column = column_mappings[param]
        if isinstance(value, str):
            query = query.filter(column == value)
        elif isinstance(value, int):
            query = query.filter(column == value)

    if limit:
        query = query.limit(limit)

    return query.all()


def convert_to_json(query_results):
    """Input query results in the form of a list of SQLalchemy objects,
    output the results in JSON format."""

    result_list = []
    for item in query_results:
        # Create a dictionary representation without the _sa_instance_state attribute
        item_dict = {key: value for key, value in item.__dict__.items() if key != '_sa_instance_state'}
        result_list.append(item_dict)

    return json.dumps(result_list)

