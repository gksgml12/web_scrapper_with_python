from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

app = Flask("Superscrapper")

db={}

# @app.route("/<username>")
# def potato(username):
#       return f"Hello {username}!"

@app.route("/") #홈으로 접속하면
def home():
    return render_template("search.html")

# @app.route("/<username>")
# def potato(username):
#     return f"<h1>hello name is {username}</h1><form><input placeholder='What job do you want?' required/><button>Search</button>"

@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
      word = word.lower()
      existingJobs =db.get(word)
      if existingJobs: #이미 검색해서 가져온 이력이 있다면 재실행 X
        jobs = existingJobs
      else:
        jobs=get_jobs(word)
        db[word]=jobs
    else:
      return redirect("/")
    return render_template(
      "report.html",
      searchingBy=word, #report.html 템플릿 가져올때 변수도 넘겨줌
      resultsNumber=len(jobs),
      jobs=jobs
    )
    
@app.route("/export")
def export():
  try:
    word = request.args.get('word')
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