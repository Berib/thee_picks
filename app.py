from flask import Flask, render_template, jsonify, request
from create_schedule import three_picks, watched_status, create_missing_tables, get_watch_count
from schedules import *
import signal
import shutil
import webbrowser
import os


app = Flask(__name__)

# Store selected schedule globally
selected_schedule = None

def handle_db(title):
    """Handles the actual label processing"""
    # Add any validation/transformation here
    if not title:
        raise ValueError("Empty title provided")

    # Database operation
    return watched_status(title, "Schedule", selected_schedule)

def backup_database():
    """Creates backup of Schedule.db"""
    backup_file = f"Schedule_backup.db"
    if os.path.exists("Schedule.db"):
        shutil.copy2("Schedule.db", backup_file)
        print(f"✅ Created database backup: {backup_file}")

@app.route('/')
def home():
    global selected_schedule
    # Initialize with first schedule if not set
    if selected_schedule is None:
        selected_schedule = schedules[0]
    schedule_options = [schedule.name for schedule in schedules]
    return render_template('index.html', schedule_options=schedule_options)

@app.route('/run_function')
def run_function():
    labels = three_picks("Schedule", selected_schedule)  # Run the imported function
    return jsonify(labels)

@app.route('/about')
def about():
    return 'About'

@app.route('/shutdown', methods=['POST'])
def shutdown():
    # Shutdown the server
    os.kill(os.getpid(), signal.SIGINT)
    return 'Server shutting down...'

@app.route('/process_label', methods=['POST'])
def process_label_route():
    """Handles HTTP request and response only"""
    try:
        data = request.get_json()
        full_label = data['label']

        title = full_label.rsplit(':', 1)[0].strip()

        result = handle_db(title)

        return jsonify({
            "status": "success",
            "title": title,
            "result": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/select_schedule', methods=['POST'])
def select_schedule():
    global selected_schedule
    schedule_name = request.json.get('schedule_name')
    for schedule in schedules:
        if schedule.name == schedule_name:
            selected_schedule = schedule
            return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Schedule not found'}), 404

@app.route('/watch_count')
def watch_count():
    if selected_schedule:
        counts = get_watch_count("Schedule", selected_schedule.name)
        return jsonify(counts)
    return jsonify({"error": "No schedule selected"}), 400

schedule_main = selected_schedule


print("⚙️ Initializing database...")
create_missing_tables("Schedule.db", schedules)
print("✅ Database ready")
backup_database()

if __name__ == '__main__':
    # Start Flask first
    import threading
    def run_server():
        app.run(debug=False)

    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Then open browser after delay
    import time
    time.sleep(1)  # Wait 1 second for server to start
    webbrowser.open('http://127.0.0.1:5000')

    # Keep main thread alive
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        pass



