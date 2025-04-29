import sqlite3
from schedules import *

"""
Manages film schedules in SQLite database
- Creates/renames/deletes tables
- Tracks watched status and appearances
"""

class FilmDatabase:
    def __init__(self, db_name, schedule):
        self.db_name = db_name
        self.schedule = schedule
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def create_table(self):
        """Creates Database Framework"""
        with self.conn:
            self.conn.execute(f'''CREATE TABLE IF NOT EXISTS {self.schedule.name}
                              (id INTEGER PRIMARY KEY, 
                               name TEXT, 
                               appearances INTEGER, 
                               watched BOOLEAN)''')

    def create_items(self,):
        """Creates a Database from a class object in schedules.py"""
        with self.conn:
            self.conn.executemany(f"INSERT INTO {self.schedule.name} (name, appearances, watched) VALUES (?, ?, ?)",
                                  self.schedule.films)


    def get_random_unwatched(self, limit: int = 3) -> list[tuple]:
        """Returns [(rowid, name, appearances)] with incremented counts"""
        # 1. Select random films
        self.cursor.execute(f"""
            SELECT rowid, name, appearances FROM {self.schedule.name}
            WHERE watched = False
            ORDER BY RANDOM()
            LIMIT ?
        """, (limit,))
        films = self.cursor.fetchall()

        # 2. Increment appearances
        for rowid, _, _ in films:
            self.cursor.execute(f"""
                UPDATE {self.schedule.name} 
                SET appearances = appearances + 1 
                WHERE rowid = ?
            """, (rowid,))
        self.conn.commit()
        return films

    def watched_change(self, choice):
        """Updates the watched status to True"""
        self.cursor.execute(f"""
                UPDATE {self.schedule.name}
                SET watched = 1
                WHERE name = ?
                """, (choice,))
        self.conn.commit()

    def delete_table(self, schedule):
        """Deletes the current schedule's table"""
        with self.conn:
            self.conn.execute(f'DROP TABLE IF EXISTS {schedule}')

    def watched_per(self):
        """Schedule watched percentage"""
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.schedule.name}")
        total_films = self.cursor.fetchone()[0]
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.schedule.name} WHERE watched = ?", (1,))
        not_watched = self.cursor.fetchone()[0]
        print(f"{not_watched}/{total_films}")

    def verify_all_tables(self):
        """Checks all tables for duplicates and prints results"""
        print("\nVerifying all tables:")
        found_issues = False
        original_schedule = self.schedule
        
        tables = self.get_table_names()
        for table in tables:
            self.schedule = Schedule(table, [])  # Temp schedule
            if dup_count := self.get_duplicate_count():
                print(f"⚠️ Found {dup_count} duplicates in '{table}'")
                found_issues = True
        
        self.schedule = original_schedule
        if not found_issues:
            print("✅ All tables are clean - no duplicates found")
        return found_issues

    def get_table_names(self):
        """Returns list of all table names"""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [row[0] for row in self.cursor.fetchall()]

    def get_duplicate_count(self) -> int:
        """Returns count of duplicate films in current table"""
        self.cursor.execute(f"""
            SELECT COUNT(*) FROM (
                SELECT name FROM {self.schedule.name}
                GROUP BY name HAVING COUNT(*) > 1
            )
        """)
        return self.cursor.fetchone()[0]

    def check_new_additions(self):
        """Check for new films added to current schedule"""
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT name FROM {self.schedule.name}")
        existing_films = {row[0] for row in cursor.fetchall()}
        return [film for film in self.schedule.films if film[0] not in existing_films]

    def sync_films(self):
        """Syncs current schedule's films with database"""
        current_films = {f[0] for f in self.schedule.films}
        
        # Get existing films
        self.cursor.execute(f"SELECT rowid, name FROM {self.schedule.name}")
        existing = {row[1]: row[0] for row in self.cursor.fetchall()}
        
        # Add new films
        new_films = [f for f in self.schedule.films if f[0] not in existing]
        if new_films:
            with self.conn:
                self.conn.executemany(
                    f"INSERT INTO {self.schedule.name} (name, appearances, watched) VALUES (?, ?, ?)",
                    new_films
                )
        
        # Remove deleted films
        deleted = [rowid for name, rowid in existing.items() if name not in current_films]
        if deleted:
            with self.conn:
                self.conn.executemany(
                    f"DELETE FROM {self.schedule.name} WHERE rowid = ?",
                    [(rowid,) for rowid in deleted]
                )
        
        return {
            'added': [f[0] for f in new_films],
            'removed': [name for name, rowid in existing.items() if name not in current_films]
        }

def three_picks(db_name, schedule):
    """Main Loop"""
    with FilmDatabase(f"{db_name}.db", schedule=schedule) as db:
        return db.get_random_unwatched(3)

def watched_status(choice, db_name, schedule):
    with FilmDatabase(f"{db_name}.db", schedule=schedule) as db:
        db.watched_change(choice)

def delete_table_func(db_name, schedule):
    with FilmDatabase(f"{db_name}.db", schedule=schedule) as db:
        db.delete_table(schedule)


def rename_db_table(db_path: str, old_name: str, new_name: str):
    """Renames a table in a SQLite database file

    Args:
        db_path: Path to the .db file (e.g. 'my_db.db')
        old_name: Current table name
        new_name: New table name
    """
    with sqlite3.connect(db_path) as conn:
        conn.execute(f'ALTER TABLE "{old_name}" RENAME TO "{new_name}"')
    print(f"Renamed table '{old_name}' to '{new_name}' in {db_path}")


def create_missing_tables(db_path: str, schedules: list):
    """Creates missing tables with automatic verification"""
    with FilmDatabase(db_path, schedule=schedules[0]) as db:
        # Create missing tables
        existing_tables = db.get_table_names()

        for schedule in schedules:
            if schedule.name not in existing_tables:
                print(f"Creating table '{schedule.name}'...")
                db.schedule = schedule
                db.create_table()
                db.create_items()
            else:
                db.schedule = schedule
                if (result := db.sync_films()) and (result['added'] or result['removed']):
                    if result['added']:
                        print(f"Added {len(result['added'])} films to {schedule.name}: {', '.join(result['added'])}")
                    if result['removed']:
                        print(f"Removed {len(result['removed'])} films from {schedule.name}: {', '.join(result['removed'])}")
        # Deletes tables that don't exist in schedules.py
        for table in existing_tables:
            if table not in [schedule.name for schedule in schedules]:
                db.delete_table(table)

        # verification
        db.verify_all_tables()

def get_watch_count(db_name, table_name):
    """Returns just unwatched and total counts"""
    with FilmDatabase(f"{db_name}.db", schedule=None) as db:
        db.cursor.execute(f"""
            SELECT 
                COUNT(*) as total,
                SUM(watched) as watched
            FROM {table_name}
        """)
        total, watched = db.cursor.fetchone()
        return {
            'total': total or 0,
            'unwatched': (total - watched) if watched else total
        }
#rename_db_table("Schedule.db", "films", "Schedule_1") # run this to rename a table

#delete_table_func("Schedule", schedule_test) #run this to delete a table

if __name__ == "__main__":
    print("⚙️ Running direct database initialization")
    create_missing_tables("Schedule.db", schedules)
    print("✅ Database tables ready")
