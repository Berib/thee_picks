from flask import Flask, render_template, jsonify, request
from create_schedule import three_picks, watched_status, create_missing_tables
from schedules import *
import os
import signal



app = Flask(__name__)


def handle_db(title):
    """Business logic: Handles the actual label processing"""
    # Add any validation/transformation here
    if not title:
        raise ValueError("Empty title provided")

    # Database operation
    return watched_status(title, "Schedule", schedule_main)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run_function')
def run_function():
    labels = three_picks("Schedule", schedule_main)  # Run the imported function
    return jsonify(labels)

@app.route('/about')
def about():
    return 'About'

@app.route('/shutdown', methods=['POST'])
def shutdown():
    # Safely shutdown the server
    os.kill(os.getpid(), signal.SIGINT)
    return 'Server shutting down...'


@app.route('/process_label', methods=['POST'])
def process_label_route():
    """Handles HTTP request and response only"""
    try:
        data = request.get_json()
        full_label = data['label']

        # Extract and clean label (HTTP layer responsibility)
        title = full_label.rsplit(':', 1)[0].strip()

        # Delegate to business logic
        result = handle_db(title)

        return jsonify({
            "status": "success",
            "title": title,
            "result": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


schedule_main = schedule_test

if __name__ == '__main__':
    print("⚙️ Initializing database...")
    create_missing_tables("Schedule.db", schedules)
    print("✅ Database ready")
    app.run(debug=True)
