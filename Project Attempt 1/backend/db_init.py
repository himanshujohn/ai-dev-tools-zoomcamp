
import sqlite3

def init_db():
	conn = sqlite3.connect('opportunity.db')
	c = conn.cursor()
	c.execute('''
		CREATE TABLE IF NOT EXISTS opportunities (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			title TEXT NOT NULL,
			client TEXT NOT NULL,
			contact_name TEXT NOT NULL,
			contact_email TEXT NOT NULL,
			description TEXT NOT NULL,
			type TEXT NOT NULL,
			complexity TEXT NOT NULL,
			duration TEXT NOT NULL,
			skills TEXT NOT NULL,
			deal_value REAL NOT NULL,
			insights TEXT
		)
	''')
	conn.commit()
	conn.close()

if __name__ == "__main__":
	init_db()
