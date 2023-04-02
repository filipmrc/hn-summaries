import os
import openai
import requests
import tkinter as tk

from bs4 import BeautifulSoup
from typing import List

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

# Get URLs for the stories
def get_post_urls(url: str, num_stories: int) -> List[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.find_all("tr", class_="athing")[:num_stories]
    post_urls = [url + "item?id=" + story["id"] for story in posts]
    return post_urls


# Get a post's title
def get_post_title(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("title").text
    return title


# Get the first n comments for a post
def get_first_n_comments(url: str, num_comments: int) -> List[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    raw_comments = soup.select(".comment > span")
    comments = []
    for i, comment in enumerate(raw_comments[:num_comments], start=1):
        comments += [comment.text.strip()]
    return comments


# Generate summaries for all posts
def get_summary():
    num_posts = int(num_posts_entry.get())
    num_comments = int(num_comments_entry.get())
    web_url = "https://news.ycombinator.com/"
    story_urls = get_post_urls(web_url, num_posts)
    summaries = []
    for url in story_urls:
        title = get_post_title(url).removesuffix(" | Hacker News")
        comments = get_first_n_comments(url, num_comments)
        content = "Title: " + title + "| Top comments to the post: \n"
        for comment in comments:
            content += comment + "\n"
        content += "Please summarize these comments."
        query = {"role": "user", "content": content}
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a powerful AI assistant that analyzes comments in hackernews posts. You will summarize what the commenters think. If the post links to an online article, you will attempt to summarize the article.",
                },
                query,
            ],
        )
        summaries += [
            title
            + "\n\n"
            + response["choices"][0]["message"]["content"]
            + "\n"
            + "-------------------------------"
        ]

    summaries = "\n".join(summaries)
    summaries_text_widget.insert(tk.END, summaries)


if __name__ == "__main__":
    app = tk.Tk()
    app.title("Hacker News Summaries")

    summaries_button = tk.Button(app, text="Get summaries", command=get_summary)
    summaries_button.pack()

    # create GUI elements
    num_posts_label_frame = tk.Frame(app)
    num_posts_label_frame.pack()
    num_posts_label = tk.Label(num_posts_label_frame, text="num posts:")
    num_posts_label.pack(side=tk.LEFT)
    num_posts_entry = tk.Entry(num_posts_label_frame)
    num_posts_entry.pack(side=tk.LEFT)

    num_comments_label_frame = tk.Frame(app)
    num_comments_label_frame.pack()
    num_comments_label = tk.Label(num_comments_label_frame, text="num comments:")
    num_comments_label.pack(side=tk.LEFT)
    num_comments_entry = tk.Entry(num_comments_label_frame)
    num_comments_entry.pack(side=tk.LEFT)

    summaries_text_widget = tk.Text(app, wrap=tk.WORD)
    summaries_text_widget.pack()

    app.mainloop()
