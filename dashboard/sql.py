import json
import sqlite3

# Read JSON data from file
with open('jsondata.json', 'r', encoding='latin-1') as file:
    json_data = json.load(file)

# Connect to SQLite database (creates if not exists)
conn = sqlite3.connect('dashboard_data.db')
cursor = conn.cursor()

# Define table schema
create_table_query = '''
CREATE TABLE IF NOT EXISTS insights (
    id INTEGER PRIMARY KEY,
    end_year TEXT,
    intensity INTEGER,
    sector TEXT,
    topic TEXT,
    insight TEXT,
    url TEXT,
    region TEXT,
    start_year TEXT,
    impact TEXT,
    added TEXT,
    published TEXT,
    country TEXT,
    relevance INTEGER,
    pestle TEXT,
    source TEXT,
    title TEXT,
    likelihood INTEGER
)
'''

# Execute table creation query
cursor.execute(create_table_query)

# Insert data into the table
for item in json_data:
    # Replace empty values with NULL
    data_tuple = (
        item.get('end_year') or None,
        item.get('intensity'),
        item.get('sector') or None,
        item.get('topic') or None,
        item.get('insight') or None,
        item.get('url') or None,
        item.get('region') or None,
        item.get('start_year') or None,
        item.get('impact') or None,
        item.get('added') or None,
        item.get('published') or None,
        item.get('country') or None,
        item.get('relevance'),
        item.get('pestle') or None,
        item.get('source') or None,
        item.get('title') or None,
        item.get('likelihood')
    )

    # Define the insertion query
    insert_query = '''
    INSERT INTO insights (
        end_year, intensity, sector, topic, insight, url,
        region, start_year, impact, added, published,
        country, relevance, pestle, source, title, likelihood
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    # Execute the insertion query with the data tuple
    cursor.execute(insert_query, data_tuple)

# Commit changes and close connection
conn.commit()
conn.close()

print("Data inserted into SQLite database successfully.")
