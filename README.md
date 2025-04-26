# Flask Scheduling Application

A web-based scheduling application built with Python and Flask.

## Features
- Schedule management system
- Database integration (SQLite)
- Web interface with HTML/CSS

## Requirements
- Python 3.x
- Flask
- See `requirements.txt` for full dependencies

## Installation
1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv .venv
   ```
3. Activate the environment:
   ```
   .venv\Scripts\activate
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
Run the application:
```
python app.py
```

Access the web interface at `http://localhost:5000`

## Web Interface Usage

1. **Initial Screen**:
   - Click the "Roll" button to generate three random options

2. **Selection Screen**:
   - Three buttons will appear with different options
   - Click any button to select your preferred option
   - Your selection will be displayed below the buttons

3. **Exit**:
   - Use the "Exit" button to close the application

Note: The application randomly selects from available options when you click "Roll"

## Schedule Management System

This Flask application includes a schedule management system with predefined film schedules.

## Features

- `Schedule` class for managing film schedules
- Delete the predefined schedules, maybe keep the test one.
- Each schedule contains:
  - A name (e.g. "Schedule_1")
  - A list of films with appearances status tracking


Each film entry tracks:
- Film title
- Appearances count
- Completion status

To modify schedules, edit the `schedules.py` file.

## Creating Custom Schedules

To add your own film schedules to the application:

1. **Define your film list** in `schedules.py`:
   ```python
   films_custom = [
       "Film Title 1",  # Simple string format (auto-converts to tuple)
       ("Film Title 2", 0, False),  # Explicit tuple format
       # Add more films...
   ]
   ```
   - Tuple format: `(title, appearance_count, watched_status)`
   - `appearance_count`: Tracks how many times the film has been displayed
   - `watched_status`: Boolean indicating if film was watched
   - Strings auto-convert to `(title, 0, False)`

2. **Create a Schedule object**:
   ```python
   custom_schedule = Schedule("Schedule_Name", films_custom)  # No whitespace allowed in name
   ```
   - Names must be valid SQLite table identifiers (no whitespace, special chars)
   - Use underscores instead of spaces

3. **Add to schedules list**:
   ```python
   schedules.append(custom_schedule)
   ```

**Notes**:
- Appearance counts and watch status are automatically tracked
- Existing schedule (films_test) serve as templates
- For testing, use the existing `schedule_test` as an example
- To change the default schedule, modify `schedule_main = schedule_test` in app.py

## Film Management

### Adding/Removing Films
1. Edit the film lists in `schedules.py`:
   ```python
   # Example: Adding to Schedule_test
   films_test = [
       ...
       "New Film",  # Add new films here
   ]
   ```
2. Changes are automatically detected:
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
