import boto3
import json
from playbyplay_api.api import lambda_handler


def test_lambda_handler():
    # Create a sample test event (use the same format as expected by your Lambda function)
    test_event = {
            "httpMethod": "GET",
            "headers": {
                "Content-Type": "application/json"
            },
            "queryStringParameters": {
                "player1_name": "Jayson Tatum",
                "player2_name": "Marcus Smart",
                "eventmsgtype": 1
            },
            "body": "{\"message\": \"Test body data\"}"
    }

    # Invoke the Lambda function locally
    response = lambda_handler(test_event, None)

    # Print the response or perform assertions
    print(response)


if __name__ == "__main__":
    test_lambda_handler()