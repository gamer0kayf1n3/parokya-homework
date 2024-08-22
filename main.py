from flask import Flask, render_template
import notion_grabber
from threading import Thread
import sys
import os
import time
import shutil

app = Flask(__name__)

def save_pdf():
  # pc method
  from playwright.sync_api import sync_playwright

  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.emulate_media(media="print")
    page.goto("http://localhost:8080")
    page.pdf(path=".pdf", margin={"top": "0.25in", "bottom": "0.25in", "left": "0.25in", "right": "0.25in"})
    browser.close()

def watch_for_pdf():
  # android method
  while True:
    for x in os.listdir("../storage/downloads"):
      if x == "Today's Activities.PDF":
        file = os.path.join("../storage/downloads", "Today's Activities.PDF")
        shutil.copy2(file, ".", follow_symlinks=True)
        os.remove(file)
        break
    time.sleep(1)

@app.route("/")
def main():
  worklist = notion_grabber.Worklist()
  worklistData = worklist.fetch()
  print(worklistData)
  return render_template("index.html", worklistData=worklistData)


is_android: bool = hasattr(sys, 'getandroidapilevel')
print(is_android)
if is_android: # i host this script on termux too
  t = Thread(target=watch_for_pdf)
  t.start()
else:
  t = Thread(target=save_pdf)
  t.start()


app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(host="0.0.0.0", port=8080, debug=True)