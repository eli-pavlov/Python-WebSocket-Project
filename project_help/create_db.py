import sqlite3

conn = sqlite3.connect("data.db")
cur = conn.cursor()

cmd = """
CREATE TABLE IF NOT EXISTS station_status (
	station_id INT,
	last_date TEXT,
	alarm1 INT,
	alarm2 INT,
	PRIMARY KEY(station_id)
);
"""
cur.execute(cmd)
conn.commit()


# ....

conn.close()


