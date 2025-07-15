from flask import Flask, render_template, request, redirect, url_for
from scraper import extract_username, scrape_reddit_user, generate_persona
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('reddit_url')
        username = extract_username(url)
        if username:
            posts, comments = scrape_reddit_user(username)
            if posts or comments:
                persona = generate_persona(username, posts, comments)
                return render_template('persona.html', persona=persona)
        return render_template('index.html', error="Invalid URL or no data found")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)