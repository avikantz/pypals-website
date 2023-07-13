#!/usr/bin/python

from flask import Flask, render_template, redirect, request, jsonify
from datetime import datetime, timedelta
import json

app = Flask(__name__)

@app.route("/")
def main():
    return redirect(u'/mupy')

@app.route("/repo")
def repo():
    return redirect('https://github.com/PyPals')

@app.route(u'/mupy')
def mu_py():
    return render_template('index.html', title="MUPy 2018", subtitle="MUPy")

@app.route(u'/mupy2016')
def mupy2016():
    data = []
    with open('photos.json') as photos_data:
        data = json.load(photos_data)
    return render_template('mupy2016.html', subtitle=" ", photos=data)

@app.route(u'/mupy2017')
def mupy2017():
    data = []
    with open('photos.json') as photos_data:
        data = json.load(photos_data)
    return render_template('mupy2017.html', subtitle=" ", photos=data)

@app.route("/LUGM")
def lugm():
    return redirect('https://lugm.xyz/')

@app.route("/mupy2017")
def norm_mupy_1():
    return redirect(u'/mupy')

@app.route("/MU3.14159")
def mu_pynum():
    return redirect(u'/mupy')

@app.route("/proposal")
def proposal():
    return render_template('proposal.html', subtitle="Call for Proposals")

@app.route("/conduct")
def conduct():
    return render_template('conduct.html', subtitle="Code of Conduct")

@app.route("/team")
def team():
    return render_template('team.html', subtitle="Team")

@app.route("/faq")
def faq():
    return render_template('faq.html', subtitle="Frequently Asked Questions")

@app.route("/lightningproposal")
def lightningproposal():
    return render_template('lightningproposal.html', subtitle="Lightning Talk CFP")

@app.route("/windows")
def windows():
    return redirect('http://i0.kym-cdn.com/photos/images/original/000/232/114/e39.png')

@app.route("/schedule")
def sched():
    data = []
    with open('talk.json') as data_file:
        data = json.load(data_file, strict = False)
    return jsonify(data)

@app.route("/gallery")
def gallery():
    data = []
    with open('photos.json') as photos_data:
        data = json.load(photos_data)
    return render_template('photos.html', photos=data, subtitle="Gallery", title="Gallery")

@app.route("/schedule/<talk_id>")
def sched_detail(talk_id):
    data = []
    with open('talk.json') as data_file:
        data = json.load(data_file, strict = False)

    talk_data = {}
    for datum in data:
        if talk_id == datum["talk_id"]:
            talk_data = datum.copy()
            timestamp = talk_data["begin_time"]
            time = datetime.strptime(timestamp, "%Y%m%d%H%M")
            datestr = time.strftime("%b %d, %Y")
            timestr = time.strftime("%I:%M %p")
            talk_data["begin_time"] = timestr
            talk_data["date"] = datestr
            break
    return jsonify(talk_data)

@app.route("/talk")
@app.route("/talk/")
def talk():
    data = []
    with open('talk.json') as data_file:
        data = json.load(data_file, strict = False)

    data = sorted(data, key=lambda k: k['begin_time'])

    day1 = []
    day2 = []

    for dat in data:
        timestamp = dat["begin_time"]
        time = datetime.strptime(timestamp, "%Y%m%d%H%M")
        datestr = time.strftime("%b %d, %Y")
        timestr = time.strftime("%I:%M %p")
        dat["begin_time"] = timestr
        dat["date"] = datestr
        if (datestr == "Oct 21, 2017"):
            day1.append(dat)
        else:
            day2.append(dat)

    # talkdata = [{"day": "Day 1 (Oct 21, 2017)", "data": day1}, \
    # {"day": "Day 2 (Oct 22, 2017)", "data": day2}]
    talkdata = [{"day": "Oct 28, 2018", "data": day2}]

    return render_template("talk.html", talkdata=talkdata, \
        subtitle="Talks Schedule")

@app.route("/talk/<talk_id>")
@app.route("/talk/<talk_id>/")
def talk_detail(talk_id):
    data = []
    with open('talk.json') as data_file:
        data = json.load(data_file, strict = False)

    talk_data = {}
    for datum in data:
        if talk_id == datum["talk_id"]:
            talk_data = datum.copy()
            timestamp = talk_data["begin_time"]
            time = datetime.strptime(timestamp, "%Y%m%d%H%M")
            datestr = time.strftime("%b %d, %Y")
            timestr = time.strftime("%I:%M %p")
            talk_data["begin_time"] = timestr
            talk_data["date"] = datestr
            break

    if not talk_data:
        return render_template('404.html', title="Not Found"), 404
    else:
        talk_title = talk_data["title"]
    return render_template("talk_detail.html", subtitle = talk_title, \
        details = talk_data)

@app.route('/android')
@app.route('/android/')
def android():
    return redirect("https://play.google.com/store/apps/details?id=com.pypals.bennyhawk.mupy18")

@app.route('/ios')
@app.route('/ios/')
def ios():
    return redirect("https://appsto.re/in/cAEifb.i")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="Not Found"), 404

@app.errorhandler(400)
def bad_request(e):
    return render_template('404.html', title="Bad request"), 400

# if __name__ == "__main__":
#     app.run(port = 3000, debug=True)
