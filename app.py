"""
To run this in a publically available setting, use --host=0.0.0.0
at the command line
"""


from flask import Flask, render_template, request
from typing import Dict
from src.video_captions import Video
import datetime


app = Flask(__name__)



@app.route("/",  methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html", transcript={}, default_url="")

    elif request.method == "POST":
        url = request.form["url"]
        transcript = create_transcript_from_url(url)
        return render_template('index.html', transcript=transcript, default_url=url)

@app.route("/json/<string:id>")
def create_transcript(id: str) -> Dict:
    """
    Accepts a url of a youtube video and returns a dictionary mapping timestamps to their transcript text
    """
    url = fr"https://www.youtube.com/watch?v={id}"
    video = Video(url)
    caption_dict = video.get_caption_dict()
    caption_json = jsonify_caption_dict(caption_dict)
    return caption_json

def create_transcript_from_url(url: str) -> Dict:
    """
    Accepts a url of a youtube video and returns a dictionary mapping timestamps to their transcript text
    """
    video = Video(url)
    caption_dict = video.get_caption_dict()
    caption_json = jsonify_caption_dict(caption_dict)
    return caption_json






def jsonify_caption_dict(caption_dict, format="%H:%M:%S"):
    """
    This function converts a caption dict into a valid json output. expects a
    """
    DATETIME = 0
    TITLE = 1
    caption_json = dict()
    for key, captions in caption_dict.items():  # key is a tuple (datetime, title: str)
        dt = key[DATETIME]
        title = key[TITLE]
        time_str = datetime.datetime.strftime(dt, format)
        json_key = f"{time_str} {title}"
        json_captions = " ".join([str(caption) for caption in captions])
        json_captions = json_captions.replace("  ", " ")
        caption_json[json_key] = json_captions


    return caption_json



if __name__ == '__main__':
    url = r"https://www.youtube.com/watch?v=ClxRHJPz8aQ&t=3734s"
    video = Video(url)
    caption_dict = video.get_caption_dict()
    caption_json = jsonify_caption_dict(caption_dict)
    print(caption_json)