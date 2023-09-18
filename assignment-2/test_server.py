#Author - Sai Mouna Bogireddy, test cases for server.py 
import unittest
from unittest.mock import MagicMock, patch
from server import app, create_tweet, delete_tweet, get_user_tweets
import json

class TestServer(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @classmethod
    def mock_response(cls, status_code, json_data):
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.json.return_value = json_data
        return mock_response

    def test_create_tweet_failure_400(self):
        mock_response = self.mock_response({"error": "No tweet ID provided"}, 400)
        tweet_text=""
        with app.test_request_context('/tweets', json={"text": tweet_text}):
            response = create_tweet()

        #expected_response = {"error": "No tweet ID provided"}
        print("response create tweet failure:", mock_response)
        self.assertEqual(response[1], 400)

    @patch('server.requests.post')
    def test_create_tweet_failure_500(self, mock_post):
        # Mock a failure response from the Twitter API (status code 500)
        tweet_text = "This is a test tweet."
        error_response = {
            "error": "Internal Server Error"
        }

        mock_post.return_value = MagicMock(status_code=500, json=lambda: error_response)

        # Call the create_tweet function
        response = self.app.post('/tweets', json={"text": tweet_text})

        # Verify that the response matches the expected structure for a 500 error
        expected_response = {
            "error": error_response
        }
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), expected_response)


    @patch('server.requests.post')
    def test_create_tweet(self, mock_post):
        mock_response = {
            "data": {
                "edit_history_tweet_ids": ["1703287656078254358"],
                "id": "1703287656078254358",
                "text": "This is a test tweet."
            }
        }

        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.status_code = 201

        mock_request = {
            "text": "This is a test tweet."
        }

        with app.test_request_context('/', method='POST', json=mock_request):
            response = create_tweet()

        expected_response = json.dumps(mock_response)
        self.assertEqual(json.dumps(response), expected_response)

    @patch('server.requests.delete')
    def test_delete_tweet_success(self, mock_delete):
        tweet_id = "1703448506437079393"  # Replace with a valid tweet ID
        expected_response = {"message": "Tweet deleted successfully"}

        mock_delete.return_value = self.mock_response(200, expected_response)

        with app.test_request_context(f"/tweets/{tweet_id}", method='DELETE'):
            response, status_code = delete_tweet(tweet_id)

        print("response in test file:", response)
        print("statuscode in test file:", status_code)

        self.assertEqual(status_code, 200)



    def test_delete_tweet_failure(self):
        tweet_id = ""
        mock_response = self.mock_response({"error": "No tweet ID provided"}, 400)

        with app.test_request_context(f'/tweets/{tweet_id}', method='DELETE'):
            response = delete_tweet(tweet_id)

        expected_response = {"error": "No tweet ID provided"}
     
        self.assertEqual(response[1], 400)

    @patch('server.requests.delete')
    def test_delete_tweet_failure_500(self, mock_delete):
        error_response = {
            "error": "Internal Server Error"
        }

        mock_delete.return_value = MagicMock(status_code=500, json=lambda: error_response)

        tweet_id = "123456789"  

        with app.test_request_context(f'/tweets/{tweet_id}', method='DELETE'):
            response = delete_tweet(tweet_id)

        expected_response = {
            "error": error_response
        }
        self.assertEqual(response[1], 500)

    @patch('server.requests.get')
    def test_get_authenticated_user_success(self, mock_get):
        mock_response = {
            "id": "123456789",
            "name": "John Doe"
        }

        mock_get.return_value = MagicMock(status_code=200, json=lambda: mock_response)
        user_id="12345"

        response = self.app.get('/users/me')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), mock_response)

    @patch('server.requests.get')
    def test_get_authenticated_user_failure_500(self, mock_get):
        error_response = {
            "error": "Internal Server Error"
        }

        mock_get.return_value = MagicMock(status_code=500, json=lambda: error_response)

        response = self.app.get('/users/me')

        expected_response = {
            "error": error_response
        }
        print("response in test file:", response)

        self.assertEqual(response.get_json(), expected_response)

    @patch('server.requests.get')
    def test_get_user_tweets_failure_500(self, mock_get):
        # Mock a failure response from the Twitter API (status code 500)
        user_id = "123456789"  # Example user ID
        error_response = {
            "error": "Internal Server Error"
        }

        mock_get.return_value = MagicMock(status_code=500, json=lambda: error_response)

        # Call the get_user_tweets function
        response = self.app.get(f'/user/{user_id}/tweets')

        # Verify that the response matches the expected structure for a 500 error
        expected_response = {
            "error": error_response
        }
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), expected_response)

    @patch('server.requests.get')
    def test_get_user_tweets_success(self, mock_get):
        # Mock a successful response from the Twitter API (status code 200)
        user_id = "123456789"  # Example user ID
        mock_response = {
            "tweets": [
                {"id": "tweet1", "text": "This is tweet 1"},
                {"id": "tweet2", "text": "This is tweet 2"}
            ]
        }

        mock_get.return_value = MagicMock(status_code=200, json=lambda: mock_response)

        # Call the get_user_tweets function
        response = self.app.get(f'/user/{user_id}/tweets')

        # Verify that the response matches the expected structure
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), mock_response)


    def test_get_tweets_400(self):
        user_id = ""
        mock_response = self.mock_response({"error": "No tweet ID provided"}, 400)

        with app.test_request_context(f'/user/<user_id>/tweets', method='DELETE'):
            response = get_user_tweets(user_id)

        expected_response = {"error": "No tweet ID provided"}
     
        self.assertEqual(response[1], 400)

   
if __name__ == "__main__":
    unittest.main()
