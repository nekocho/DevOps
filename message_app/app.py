from flask import Flask, render_template
import time
import redis
import psycopg2


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

@app.route('/') # For home route
def home():
    count = get_hit_count()
    messages = get_messages()
    return render_template('index.html', count=count, messages=messages)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def get_messages():
    conn = psycopg2.connect(
        dbname="your_database",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages")
    messages = cur.fetchall()
    cur.close()
    conn.close()
    return messages

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)

# host: allows connection from any IP
# port: needs to match whats exposed in dockerfile
