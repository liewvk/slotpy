from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Game state and configuration
user_state = {"credits": 100}
symbols = ["🍒", "🍋", "🍉", "⭐", "🔔"]
payouts = {
    "🍒🍒🍒": 50,
    "🍋🍋🍋": 30,
    "🍉🍉🍉": 20,
    "⭐⭐⭐": 100,
    "🔔🔔🔔": 200,
}

@app.route("/spin", methods=["POST"])
def spin():
    try:
        logging.info("Received spin request.")
        
        # Check if user has enough credits
        if user_state["credits"] <= 0:
            logging.warning("User attempted to spin with no credits.")
            return jsonify({"error": "No credits left"}), 400

        # Deduct credits for the spin
        user_state["credits"] -= 10
        logging.debug(f"Credits deducted. Remaining credits: {user_state['credits']}.")

        # Generate random spin results
        reels = [random.choice(symbols) for _ in range(3)]
        result = "".join(reels)
        payout = payouts.get(result, 0)
        logging.debug(f"Spin result: {result}. Payout: {payout}.")

        # Update user credits with payout
        user_state["credits"] += payout
        logging.debug(f"Credits after payout: {user_state['credits']}.")

        # Response data
        response = {
            "reels": reels,
            "result": result,
            "payout": payout,
            "credits": user_state["credits"],
        }
        logging.info(f"Response sent: {response}")
        return jsonify(response)

    except Exception as e:
        logging.error(f"Error processing spin: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # Start Flask app on port 8000
    logging.info("Starting Flask server on http://127.0.0.1:8080...")
    app.run(host="0.0.0.0", port=8080)
