from flask import Flask, render_template, request, redirect, url_for, jsonify, g
import sqlite3

app = Flask(__name__)

# Login credentials (replace with actual authentication mechanism)
users = {'user': 'user123'}
admins = {'admin': 'admin123'}

# Define a global variable to track user roles
user_roles = {}

# Function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('dashboard_data.db')
    return db

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            user_roles[username] = 'user'
            return redirect(url_for('dashboard', username=username))
        elif username in admins and admins[username] == password:
            user_roles[username] = 'admin'
            return redirect(url_for('dashboard', username=username))
    return render_template('login.html')

# Route for user dashboard
@app.route('/dashboard')
def dashboard():
    username = request.args.get('username')
    if username and username in user_roles:
        role = user_roles[username]
        if role == 'admin':
            return render_template('dashboard.html', role='admin')
        else:
            return render_template('dashboard.html', role='user')
    else:
        return redirect(url_for('login'))

# API endpoint to retrieve sector-wise data
# API endpoint to retrieve sector-wise data
@app.route('/api/sectors')
def get_sector_data():
    # Retrieve intensity range from query parameters
    min_intensity_str = request.args.get('min_intensity')
    max_intensity_str = request.args.get('max_intensity')

    # Convert intensity values to integers, handling the case when they are not provided
    min_intensity = int(min_intensity_str) if min_intensity_str and min_intensity_str != 'null' else None
    max_intensity = int(max_intensity_str) if max_intensity_str and max_intensity_str != 'null' else None

    # Modify the query to filter by intensity range if both min and max intensity are provided
    if min_intensity is not None and max_intensity is not None:
        query = '''
        SELECT sector, COUNT(*) AS count
        FROM insights
        WHERE intensity >= ? AND intensity <= ?
        GROUP BY sector
        '''
        params = (min_intensity, max_intensity)
    else:
        # Query to retrieve sector-wise counts without intensity filtering
        query = '''
        SELECT sector, COUNT(*) AS count
        FROM insights
        GROUP BY sector
        '''
        params = None

    db = get_db()
    cursor = db.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    sectors_data = cursor.fetchall()

    # Format data as list of dictionaries
    sectors = [{'sector': row[0], 'count': row[1]} for row in sectors_data]

    # Return data as JSON response
    return jsonify({'sectors': sectors})
# API endpoint to retrieve topics data for a specific sector
@app.route('/api/topics/<sector>')
def get_topics_by_sector(sector):
    # Retrieve intensity range from query parameters
    min_intensity_str = request.args.get('min_intensity')
    max_intensity_str = request.args.get('max_intensity')

    # Convert intensity values to integers, handling the case when they are not provided
    min_intensity = int(min_intensity_str) if min_intensity_str and min_intensity_str != 'null' else None
    max_intensity = int(max_intensity_str) if max_intensity_str and max_intensity_str != 'null' else None

    # Modify the query to filter by intensity range if both min and max intensity are provided
    if min_intensity is not None and max_intensity is not None:
        query = '''
        SELECT topic, COUNT(*) AS count
        FROM insights
        WHERE (sector = ? OR sector IS NULL)
          AND (intensity >= ? AND intensity <= ?)
        GROUP BY topic
        '''
        params = (sector, min_intensity, max_intensity)
    else:
        # Query to retrieve topics data for the specified sector without intensity filtering
        query = '''
        SELECT topic, COUNT(*) AS count
        FROM insights
        WHERE sector = ? OR sector IS NULL
        GROUP BY topic
        '''
        params = (sector,)

    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, params)
    topics_data = cursor.fetchall()

    # Format data as list of dictionaries
    topics = [{'topic': row[0], 'count': row[1]} for row in topics_data]

    # Return data as JSON response
    return jsonify({'topics': topics})

# API endpoint to retrieve pests data for a specific sector and topic
@app.route('/api/pests/<sector>/<topic>')
def get_pests_by_sector_and_topic(sector, topic):
    # Retrieve intensity range from query parameters
    min_intensity_str = request.args.get('min_intensity')
    max_intensity_str = request.args.get('max_intensity')

    # Convert intensity values to integers, handling the case when they are not provided
    min_intensity = int(min_intensity_str) if min_intensity_str and min_intensity_str != 'null' else None
    max_intensity = int(max_intensity_str) if max_intensity_str and max_intensity_str != 'null' else None

    # Modify the query to filter by intensity range if both min and max intensity are provided
    if min_intensity is not None and max_intensity is not None:
        query = '''
        SELECT pestle, COUNT(*) AS count
        FROM insights
        WHERE sector = ? AND topic = ?
          AND intensity >= ? AND intensity <= ?
        GROUP BY pestle
        '''
        params = (sector, topic, min_intensity, max_intensity)
    else:
        # Query to retrieve pests data for the specified sector and topic without intensity filtering
        query = '''
        SELECT pestle, COUNT(*) AS count
        FROM insights
        WHERE sector = ? AND topic = ?
        GROUP BY pestle
        '''
        params = (sector, topic)

    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, params)
    pests_data = cursor.fetchall()

    # Format data as list of dictionaries
    pests = [{'pestle': row[0], 'count': row[1]} for row in pests_data]

    # Return data as JSON response
    return jsonify({'pests': pests})

@app.route('/api/important-insights')
def fetch_important_insights():
    query = '''
    SELECT insight
    FROM insights
    WHERE intensity > 70 AND relevance > 4 AND likelihood > 3
    '''
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    insights_data = cursor.fetchall()

    # Format data as list of dictionaries
    important_insights = [{'insight_text': row[0]} for row in insights_data]
    print(important_insights)

    # Return data as JSON response
    return jsonify({'important_insights': important_insights})

# Import necessary modules
from flask import jsonify

# Assuming you already have a Flask app instance named 'app'

# API endpoint to retrieve the count of insights for each start year
@app.route('/api/insights-by-year')
def get_insights_by_year():
    # Query the database to get the count of insights for each start year
    query = '''
    SELECT start_year, COUNT(*) AS insight_count
    FROM insights
    GROUP BY start_year
    ORDER BY start_year
    '''

    # Execute the query and fetch the results
    cursor = get_db().cursor()
    cursor.execute(query)
    insights_by_year = cursor.fetchall()

    # Format the data as a list of dictionaries
    insights_data = [{'year': row[0], 'count': row[1]} for row in insights_by_year]

    # Return the data as a JSON response
    return jsonify({'insights_by_year': insights_data})

# API endpoint to retrieve insights grouped by relevance
@app.route('/api/insights-by-relevance')
def get_insights_by_relevance():
    # Query the database to get the count of insights for each relevance
    query = '''
    SELECT relevance, COUNT(*) AS insight_count
    FROM insights
    GROUP BY relevance
    '''

    # Execute the query and fetch the results
    cursor = get_db().cursor()
    cursor.execute(query)
    insights_by_relevance = cursor.fetchall()

    # Format the data as a list of dictionaries
    insights_data = [{'relevance': row[0], 'count': row[1]} for row in insights_by_relevance]

    # Return the data as a JSON response
    return jsonify({'insights_by_relevance': insights_data})

@app.route('/api/insights-by-likelihood')
def get_insights_by_likelihood():
    # Query the database to get the count of insights for each likelihood
    query = '''
    SELECT likelihood, COUNT(*) AS insight_count
    FROM insights
    GROUP BY likelihood
    ORDER BY likelihood
    '''

    # Execute the query and fetch the results
    cursor = get_db().cursor()
    cursor.execute(query)
    insights_by_likelihood = cursor.fetchall()

    # Format the data as a list of dictionaries
    insights_data = [{'likelihood': row[0], 'count': row[1]} for row in insights_by_likelihood]

    # Return the data as a JSON response
    return jsonify({'insights_by_likelihood': insights_data})

@app.route('/api/leaderboard')
def get_leaderboard_data():
    query = '''
    SELECT country, COUNT(*) AS insight_count
    FROM insights
    GROUP BY country
    ORDER BY insight_count DESC
    '''

    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    leaderboard_data = cursor.fetchall()

    # Format the data as a list of dictionaries
    leaderboard = [{'country': row[0], 'insight_count': row[1]} for row in leaderboard_data]

    # Return the data as a JSON response
    return jsonify({'leaderboard': leaderboard})



if __name__ == '__main__':
    app.run(debug=True)


