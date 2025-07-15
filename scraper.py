import requests
from collections import Counter
import re

def extract_username(url):
    if "reddit.com/user/" not in url:
        return None
    return url.rstrip("/").split("/")[-1]

def scrape_reddit_user(username, max_items=15):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/114.0.0.0 Safari/537.36"
    }

    posts, comments = [], []

    # Fetch comments
    comment_url = f"https://www.reddit.com/user/{username}/comments/.json?limit={max_items}"
    try:
        comment_res = requests.get(comment_url, headers=headers, timeout=10)
        if comment_res.status_code == 200:
            comment_data = comment_res.json()
            for item in comment_data["data"]["children"]:
                comment_body = item["data"].get("body", "")
                if comment_body:
                    comments.append(comment_body.strip())
    except Exception as e:
        print(f"Error fetching comments: {e}")

    # Fetch posts
    post_url = f"https://www.reddit.com/user/{username}/submitted/.json?limit={max_items}"
    try:
        post_res = requests.get(post_url, headers=headers, timeout=10)
        if post_res.status_code == 200:
            post_data = post_res.json()
            for item in post_data["data"]["children"]:
                title = item["data"].get("title", "")
                selftext = item["data"].get("selftext", "")
                content = title
                if selftext:
                    content += " — " + selftext
                posts.append(content.strip())
    except Exception as e:
        print(f"Error fetching posts: {e}")

    return posts, comments

def analyze_content(posts, comments):
    all_text = ' '.join(posts + comments).lower()
    
    # Analyze interests
    common_words = [word for word, count in 
                   Counter(re.findall(r'\b\w{4,}\b', all_text)).most_common(20)
                   if word not in ['that', 'this', 'they', 'your', 'would', 'their']]
    
    # Determine personality traits
    traits = []
    word_count = len(all_text.split())
    if word_count > 1000:
        traits.append("Verbose")
    elif word_count < 300:
        traits.append("Concise")
    
    if sum(1 for c in all_text if c == '!') > 5:
        traits.append("Enthusiastic")
    if 'i think' in all_text or 'in my opinion' in all_text:
        traits.append("Analytical")
    if '?' in all_text and all_text.count('?') > 5:
        traits.append("Inquisitive")
    
    return common_words[:5], traits[:3] if traits else ["Balanced"]

def generate_persona(username, posts, comments):
    interests, traits = analyze_content(posts, comments)
    
    # Generate behaviors based on analysis
    behaviors = [
        f"{username} frequently participates in online discussions about {', '.join(interests[:-1])} and {interests[-1]}.",
        f"They tend to express opinions {'enthusiastically' if 'Enthusiastic' in traits else 'thoughtfully'} in their comments."
    ]
    
    if 'Verbose' in traits:
        behaviors.append("Writes long, detailed posts with comprehensive explanations.")
    else:
        behaviors.append("Prefers concise communication and gets straight to the point.")
    
    if 'Inquisitive' in traits:
        behaviors.append("Asks many questions and seeks deeper understanding of topics.")
    
    # Generate frustrations
    frustrations = [
        "When discussions become hostile or unproductive.",
        "Lack of detailed information on topics they care about."
    ]
    
    if 'Analytical' in traits:
        frustrations.append("When opinions aren't backed by facts or logical reasoning.")
    
    # Generate goals
    goals = [
        "To share knowledge and learn from online communities.",
        "To find like-minded individuals who share similar interests."
    ]
    
    if 'Enthusiastic' in traits:
        goals.append("To spread excitement about their passions.")
    
    persona = {
        "name": username.capitalize(),
        "age": "30-40",
        "occupation": "Tech Professional",
        "status": "Single",
        "location": "Urban",
        "traits": traits,
        "interests": interests,
        "motivations": ["KNOWLEDGE", "COMMUNITY", "CREATIVITY", "LEARNING", "CONNECTION"],
        "personality": [t.upper() for t in traits],
        "behaviors": behaviors,
        "goals": goals,
        "frustrations": frustrations,
        "quote": f"I want to connect with people who genuinely care about {interests[0]} as much as I do."
    }
    
    return persona