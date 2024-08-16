from flask import Flask, render_template
import notion_grabber
app = Flask(__name__)

@app.route("/")
def main():
  worklist = notion_grabber.Worklist()
  worklistData = worklist.fetch()
  print(worklistData)
  return render_template("index.html", worklistData=worklistData)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(host="0.0.0.0", port=8080, debug=True)