
import sqlite3

# Connect to the database
conn = sqlite3.connect('Project1.db')
c = conn.cursor()

# Execute the DELETE statement
c.execute('DELETE FROM User')

# Commit the transaction
conn.commit()

# Close the connection
conn.close()