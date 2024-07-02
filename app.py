from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

HACKER_NEWS_API = "https://hacker-news.firebaseio.com/v0"

def get_top_stories():
    top_stories_url = f"{HACKER_NEWS_API}/topstories.json"
    top_stories = requests.get(top_stories_url).json()
    return top_stories[:10]

def get_story_details(story_id):
    story_url = f"{HACKER_NEWS_API}/item/{story_id}.json"
    story_details = requests.get(story_url).json()
    return story_details

def summarize_text(text):
    return text[:200] + "..."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/news', methods=['GET'])
def get_news():
    top_stories = get_top_stories()
    news = []
    for story_id in top_stories:
        story_details = get_story_details(story_id)
        summary = summarize_text(story_details.get('text', ''))
        news.append({
            'title': story_details.get('title'),
            'summary': summary
        })
    return jsonify(news)

if __name__ == '__main__':
    app.run(debug=True)
