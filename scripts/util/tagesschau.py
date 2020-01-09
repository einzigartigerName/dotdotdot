import feedparser
import subprocess
import sys

baseUrl = "https://www.tagesschau.de/export/video-podcast/webxl/tagesschau"
NewsFeed = feedparser.parse(baseUrl)

video = NewsFeed.entries[0].links[0].href
subprocess.run(["vlc", "--play-and-exit", "-f", video])