from flask import Flask, render_template, request, redirect, send_file
from scraper import get_jobs
from export import save_to_file

# Flask 이용하여 웹사이트 구축
app = Flask("SuperScraper")
# Faster Scrapper. db에 있는 경우 다시 scrapping하지 않도록.
db = {}


# decorator 아래에 함수만 사용 가능
@app.route("/")
def home():
    return render_template("potato.html")


@app.route("/report")
def report():
    word = request.args.get('word')  # query arguments에서 word 추출
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template("report.html",
                           searchingBy=word,
                           resultsNumber=len(jobs),
                           jobs=jobs)


@app.route("/export")
def export():
    try:
        word = request.args.get('word')  # query arguments에서 word 추출
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
          raise Exception()
        save_to_file(jobs) 
        return send_file("jobs.csv")
    except:
        return redirect("/")


app.run(host="0.0.0.0")
