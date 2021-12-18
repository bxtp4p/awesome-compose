#!/usr/bin/env python
import os
import random

from splunk_otel.tracing import start_tracing
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry._metrics import get_meter

from flask import Flask
from pymongo import MongoClient

# splunk-py-trace didn't actually produce any traces so added this manually instead
start_tracing()

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

client = MongoClient("mongo:27017")
db = client.blog_db

tracer = trace.get_tracer(__name__)

meter = get_meter(__name__)
viewCounter = meter.create_counter(name="blog_views", description="number of blog post views")

@app.route('/')
def todo():
    try:
        # retrieve a random blog post
        post = get_random_post(random.randint(1,5))

        viewCounter.add(1, {"post_author": post["author"], "post_title": post["title"]})
        return f'{post["title"]} by {post["author"]}'
    except:
        return "Server Error"

def get_random_post(idx):
    with tracer.start_as_current_span("get_random_post") as span:
        post = db.posts.find_one({"title": f'post {idx}'})

        # add span tags
        span.set_attribute("blog_post_id", idx)
        span.set_attribute("blog_post_title", post['title'])
        span.set_attribute("blog_post_author", post['author'])

        return post

if __name__ == "__main__":
    # adding an example db with some data
    blog_count = db.posts.insert_many([
        {"title": "post 1", "author": "bart"},
        {"title": "post 2", "author": "tom"},
        {"title": "post 3", "author": "steve"},
        {"title": "post 4", "author": "julie"},
        {"title": "post 5", "author": "anne"},
    ])

    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)

