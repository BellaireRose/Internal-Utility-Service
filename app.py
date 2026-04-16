from flask import Flask, jsonify
from database import get_users
import config
import boto3
import json
import logging

# Configure global logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)

logger = logging.getLogger(__name__)

app = Flask(__name__)


def get_secret():
    """Fetch secrets from AWS Secrets Manager."""
    logger.info("Fetching secrets from AWS Secrets Manager...")
    try:
        client = boto3.client("secretsmanager", region_name="us-east-1")
        response = client.get_secret_value(SecretId="capstone/app-secrets")
        logger.info("Secrets retrieved successfully")
        return json.loads(response.get("SecretString", "{}"))
    except Exception as e:
        logger.warning(f"Could not retrieve secrets: {e}")
        return {}


# Load secrets at startup
secrets = get_secret()


@app.route("/")
def home():
    logger.info("Home endpoint accessed")
    return jsonify({
        "message": "Internal Utility Service Running",
        "environment": config.ENVIRONMENT,
        "db_host": config.DB_HOST
    }), 200


@app.route("/health")
def health():
    logger.info("Health check endpoint accessed")
    return jsonify({"status": "UP"}), 200


@app.route("/users")
def users():
    logger.info("Users endpoint accessed")
    try:
        users_data = get_users()
        logger.info(f"Fetched {len(users_data)} users")
        return jsonify(users_data), 200
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return jsonify({"error": "Unable to fetch users"}), 500


if __name__ == "__main__":
    logger.info("Starting Flask application...")
    app.run(host="0.0.0.0", port=5000, debug=True)