# Flask Scheduling Application

A web-based scheduling application built with Python and Flask that helps users manage and select schedules.

## Project Structure

```
flasktut/
├── app.py                # Main Flask application
├── create_schedule.py    # Schedule creation script
├── schedules.py          # Schedule management module
├── static/
│   └── style.css         # CSS styles
├── templates/
│   └── index.html        # Main HTML template
├── Schedule.db           # SQLite database
└── requirements.txt      # Dependencies
```

## Features
- Schedule management system
- Database integration (SQLite)
- Web interface with HTML/CSS
- Random schedule selection functionality
- Database persistence for schedules

## Requirements
- Python 3.x
- Flask
- See `requirements.txt` for full dependencies

## Installation
1. Clone this repository
2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   ```
3. Activate the environment:
   ```
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
Run the application:
```
python app.py
```

Access the web interface at `http://localhost:5000`

## Web Interface Guide

1. **Main Screen**:
   - Select schedule from dropdown menu and confirm 
   - Click "Roll" to generate three random schedule options
   - Options are pulled from the database

2. **Selection**:
   - Three buttons appear with different schedule options
   - Click any button to select your preferred schedule
   - Your selection is displayed below the buttons

3. **Exit**:
   - Use the "Exit" button to close the application

## Development
To add new schedules:
1. Edit `schedules.py` to add your schedules
2. Run the script to update the database:
3. Changes are automatically detected:
   - Added films appear with default values (0 appearances, not watched)
   - Removed films are deleted from the database
   - Existing films remain unchanged

### Viewing Changes
The system logs all modifications:
```
Added 2 films to Schedule_test: New Film 1, New Film 2
Removed 1 film from Schedule_test: Old Film
```

## Project Structure
- `app.py` - Main Flask application
- `schedules.py` - Schedule management logic
- `templates/` - HTML templates
- `static/` - CSS and static files
- `Schedule.db` - SQLite database

## License
MIT
