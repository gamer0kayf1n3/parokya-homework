from flask import Flask, render_template
import notion_grabber
from threading import Thread
app = Flask(__name__)

def save_pdf():
  from playwright.sync_api import sync_playwright

  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.emulate_media(media="print")
    page.goto("http://localhost:8080")
    page.pdf(path=".pdf", margin={"top": "0.25in", "bottom": "0.25in", "left": "0.25in", "right": "0.25in"})
    browser.close()

@app.route("/")
def main():
  worklist = notion_grabber.Worklist()
  worklistData = worklist.fetch()
  print(worklistData)
  return render_template("index.html", worklistData=worklistData)
app.config['TEMPLATES_AUTO_RELOAD'] = True
t = Thread(target=save_pdf)
t.start()
app.run(host="0.0.0.0", port=8080, debug=True)