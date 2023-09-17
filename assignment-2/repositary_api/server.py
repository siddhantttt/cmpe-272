import json
import os

import requests
from flask import Flask, request, jsonify
from requests_oauthlib import OAuth1
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_secret = os.environ['TWITTER_ACCESS_SECRET']

auth = OAuth1(consumer_key, client_secret=consumer_secret, resource_owner_key=access_token,
              resource_owner_secret=access_secret)


@app.route("/tweets", methods=["POST"])
def create_tweet():
    tweet_text = request.json.get("text", "")

    if not tweet_text:
        return jsonify({"error": "No tweet text provided"}), 400

    payload = json.dumps({"text": tweet_text})
    headers = {"Content-Type": "application/json"}
    response = requests.post("https://api.twitter.com/2/tweets", headers=headers, data=payload,
                             auth=auth)
    print(response.content)
    

    if response.status_code != 201:
        return jsonify({"error": response.json()}), 500
    return response.json()
    if response.status_code != 200:
        print(response.content)
        return jsonify({"error": response.json()}), 500


@app.route("/tweets/<tweet_id>", methods=["DELETE"])
def delete_tweet(tweet_id):
    if not tweet_id:
        return jsonify({"error": "No tweet ID provided"}), 400

    response = requests.delete(f"https://api.twitter.com/2/tweets/{tweet_id}", auth=auth)

    if response.status_code != 200:
        return jsonify({"error": response.json()}), 500

    return jsonify({"message": "Tweet deleted successfully"}), 200


@app.route("/users/me", methods=["GET"])
def get_authenticated_user():
    response = requests.get("https://api.twitter.com/2/users/me", auth=auth)
    if response.status_code != 200:
        return jsonify({"error": response.json()}), 500
    return response.json()


@app.route("/user/<user_id>/tweets", methods=["GET"])
def get_user_tweets(user_id):
    if not user_id:
        return jsonify({"error": "No user ID provided"}), 400
    response = requests.get(f"https://api.twitter.com/2/users/{user_id}/tweets", auth=auth)

    if response.status_code != 200:
        return jsonify({"error": response.json()}), 500

    return response.json()


if __name__ == "__main__":
    app.run(debug=True)
