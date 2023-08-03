from validate_and_build_query import validate_query_params, build_query_with_filters, convert_to_json


def lambda_handler(event, context):

    query_params = event.get('queryStringParameters', {})

    invalid_param_info = validate_query_params(query_params)

    if invalid_param_info:
        invalid_param, invalid_param_value = invalid_param_info
        return {
            'statusCode': 400,
            'body': f"Query parameter '{invalid_param}' with value '{invalid_param_value}' returns zero results. "
        }

    query_results = build_query_with_filters(query_params, 20)

    return {
        'statusCode': 200,
        'body': convert_to_json(query_results)
    }