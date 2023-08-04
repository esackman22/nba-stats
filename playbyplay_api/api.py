from validate_and_build_query import validate_query_params, build_query_with_filters, convert_to_json


def lambda_handler(event, context):

    # Retrieve query parameters from lambda function call
    query_params = event.get('queryStringParameters', {})

    # Check if all query parameters are valid
    invalid_param_info = validate_query_params(query_params)

    # Return an error message if the any query parameters are invalid
    if invalid_param_info:
        invalid_param, invalid_param_value = invalid_param_info
        return {
            'statusCode': 400,
            'body': f"Query parameter '{invalid_param}' with value '{invalid_param_value}' returns zero results. "
        }

    # Build a query with the parameters and extract the results
    query_results = build_query_with_filters(query_params, 20)

    # Return the results converted to JSON format
    return {
        'statusCode': 200,
        'body': convert_to_json(query_results)
    }