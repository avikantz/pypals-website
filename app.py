#!/usr/bin/python

import json
from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, request, jsonify
from flask_mongokit import MongoKit, Document
import requests

app = Flask(__name__)

recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
recaptcha_key = '***REMOVED***'
app_key = '***REMOVED***'

class User(Document):
    __collection__ = 'pypals'
    structure = {
        'name': unicode,
        'college_id': unicode,
        'college_name': unicode,
        'email': unicode,
        'tshirt_size': unicode,
        'phone': unicode,
        'time': datetime,
    }
    required_fields = ['name', 'college_id', 'email']
    default_values = {'time': datetime.now()}
    use_dot_notation = True

class Attendance(Document):
    __collection__ = 'pypals'
    structure = {
        'college_id': unicode,
        'talks_attended': list
    }
    required_fields = ['college_id', 'talks_attended']
    default_values = {'talks_attended': []}
    use_dot_notation = True

conn = MongoKit(app)
conn.register(User)
conn.register(Attendance)


@app.route("/")
def main():
    return redirect(u'/\u03BCpy')

@app.route("/repo")
def repo():
    return redirect('https://github.com/PyPals')

@app.route(u'/\u03BCpy')
def mu_py():
    return render_template('index.html', title="MUPy 2018", subtitle="MUPy")

@app.route(u'/mupy2016')
def mupy2016_1():
    return redirect(u'/\u03BCpy2016')

@app.route(u'/\u03BCpy2016')
def mupy2016():
    data = []
    with open('photos.json') as photos_data:
        data = json.load(photos_data)
    return render_template('mupy2016.html', subtitle=" ", photos=data)

@app.route(u'/mupy2017')
def mupy2017_1():
    return redirect(u'/\u03BCpy2017')

@app.route(u'/\u03BCpy2017')
def mupy2017():
    data = []
    with open('photos.json') as photos_data:
        data = json.load(photos_data)
    return render_template('mupy2017.html', subtitle=" ", photos=data)

@app.route("/LUGM")
def lugm():
    return redirect('http://lugm.xyz/')

@app.route("/mupy2017")
def norm_mupy_1():
    return redirect(u'/\u03BCpy')

@app.route("/mupy")
def norm_mupy():
    return redirect(u'/\u03BCpy')

@app.route("/MU3.14159")
def mu_pynum():
    return redirect(u'/\u03BCpy')

@app.route("/snake-charming")
def challenge():
    return redirect(u'https://www.hackerearth.com/mupy')

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

@app.route('/sabdedobc')
@app.route('/sabdedobc/')
def curr_reg():
    collection = conn['pypals'].registrations
    a = list(collection.find())
    dat = []
    for l in a:
        d = {}
        d['name'] = l['name']
        d['phone'] = l['phone']
        d['tshirt_size'] = l['tshirt_size']
        d['email'] = l['email']
        d['college_id'] = l['college_id']
        if l.get('college_name') is not None:
            d['college_name'] = l['college_name']
        dat.append(d)
    return jsonify(dat)

@app.route('/sabdedobc/<key>')
@app.route('/sabdedobc/<key>/')
def curr_reg_detail(key):
    collection = conn['pypals'].registrations
    a = list(collection.find())
    key = str(key)
    dat = []
    for l in a:
        dat.append(l.get(key))
    return jsonify(dat)

@app.route('/count')
@app.route('/count/')
def total_reg():
    collection = conn['pypals'].registrations
    t = len(list(collection.distinct("college_id")))
    count = {}
    count['count'] = t
    return jsonify(count)

@app.route('/register', methods=['POST', 'GET'])
@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html', subtitle="Register", \
            title="Register")
    elif request.method == 'POST':
        data = request.get_json()
        payload = {}
        if data is None:
            data = dict(request.form)
            del data['register-submit']
            for i,j in data.iteritems():
                data[i] = data[i][0]
            try:
                payload['response'] = data['g-recaptcha-response']
                del data['g-recaptcha-response']
            except Exception:
                payload['response'] = ''
            payload['secret'] = recaptcha_key
            res = requests.post(recaptcha_url, data = payload)
            if res.json()['success']:
                return add_reg(data)
            else:
                return render_template('register.html', success = False,\
                 message = 'Invalid captcha', subtitle="Register", \
                 title="Register")
        else:
            if request.headers.get("PyPals-Authorization") != app_key:
                res = {}
                res['success'] = 'false'
                res['error'] = 'invalid source'
                return jsonify(res)
            return add_reg(data, json = True)


def add_reg(data, json = False):
    """
    Function to facilitate adding registrations to the database.
    """
    data['time'] = datetime.now()
    res = {}
    collection = conn['pypals'].registrations
    query = {}
    options = []
    options.append({'email': data['email']})
    options.append({'college_id': data['college_id']})
    query['$or'] = options
    entries = list(collection.find(query))
    if len(entries) == 0:
        user = collection.User()
        for i,j in data.iteritems():
            user[i] = data[i]
        user.save()
        if not json:
            return render_template('register.html', success = True, \
                subtitle="Successfully registered.")
        res['success'] = 'true'
    else:
        message = "User already registered."
        if not json:
            return render_template('register.html', success = False, \
                message = message, subtitle="Failed.")
        res['success'] = 'false'
        res['error'] = message
    return jsonify(res)


@app.route('/checkregistration', methods=['POST'])
@app.route('/checkregistration/', methods=['POST'])
def check_reg():
    data = request.get_json()
    if data is None:
        data = dict(request.form)
        for i,j in data.iteritems():
            data[i] = data[i][0]
        res = {}
        collection = conn['pypals'].registrations
        query = {}
        options = []
        options.append({'college_id': data['college_id']})
        query['$or'] = options
        entries = list(collection.find(query))
        if len(entries) == 0:
            res['isRegistered'] = False
            res['message'] = "User not registered."
        else:
            res['name'] = entries[0]['name']
            res['isRegistered'] = True
            res['message'] = "User already registered."
        res['success'] = True
        return jsonify(res)
    else:
        res = {}
        res['success'] = 'false'
        res['error'] = 'invalid source'
        return jsonify(res)

@app.route('/getattendance', methods=['GET'])
@app.route('/getattendance/', methods=['GET'])
def attendance():
    if request.headers.get('PyPals-Authorization') != app_key:
        return "Unauthorised"
    college_id = request.args.get("college_id")
    if college_id is None:
        res = {}
        res['message'] = "Invalid args"
        return jsonify(res)
    else:
        collection = conn['pypals'].attendance
        query = {}
        options = []
        options.append({'college_id':str(college_id)})
        query['$or'] = options
        talks_attended = list(collection.find(query))
        if len(talks_attended) > 0:
            return jsonify(talks_attended[0]['talks_attended'])
        else:
            return jsonify([])

@app.route('/attendance', methods=[ 'POST'])
@app.route('/attendance/', methods=[ 'POST'])
def post_attendance():
    if request.headers.get('PyPals-Authorization') != app_key:
        return "Unauthorised"
    data = request.get_json()
    if data is None:
        data = dict(request.form)
        for i,j in data.iteritems():
            data[i] = data[i][0]
    college_id = data['college_id']
    eventid = data['eventid']
    registrations = conn['pypals'].registrations
    query = {}
    options = []
    options.append({'college_id':str(college_id)})
    query['$or'] = options

    if len(list(registrations.find(query))) < 1:
        return jsonify({"success": False, "message" : "unregistered"})

    talk_data = []
    with open('talk.json') as data_file:
        talk_data = json.load(data_file, strict = False)

    talk_time = None
    for datum in talk_data:
        if eventid == datum["talk_id"]:
            talk_data = datum.copy()
            timestamp = talk_data["begin_time"]
            talk_time = datetime.strptime(timestamp, "%Y%m%d%H%M")
            # talk_time += timedelta(minutes = 45)
    if talk_time is None:
        return jsonify({"success": False, "message" : "Invalid talk"})
    else:
        return add_attendance(college_id, eventid)
        # curr_time = datetime.now()
        # curr_time = datetime.strptime("201610231336", "%Y%m%d%H%M") #For testing
        # Move this registration window to something in the middle of the talk, as decided.
        # diff = (curr_time - talk_time).total_seconds()
        # print curr_time, talk_time, diff
        # if diff < 0:
        #    return jsonify({"success":False, "message": "Talk yet to start."})
        # elif diff > 300:
        #    return jsonify({"success":False, "message": "Sorry Bruh! You couldn't make it."})
        # else:
        #    return add_attendance(college_id, eventid)

@app.route('/android')
@app.route('/android/')
def android():
    return redirect("https://play.google.com/store/apps/details?id=com.pypals.gilgamesh.mupy")

@app.route('/ios')
@app.route('/ios/')
def ios():
    return redirect("https://appsto.re/in/cAEifb.i")

@app.route('/attendance/most')
@app.route('/attendance/most/')
def most_attendance():
    if request.headers.get('PyPals-Authorization') != app_key:
            return "Unauthorised"
    min_talk = None
    res = []
    entries = list(conn['pypals'].attendance.find({}, {'_id':0}))
    entries = sorted(entries, key = lambda k: len(k['talks_attended']), \
        reverse = True)
    if request.args.get('count') is None:
        return jsonify(entries)
    else:
        count = int(request.args.get('count'))
        if count > len(entries):
            return jsonify(entries)
        return jsonify(entries[:count])

def add_attendance(college_id, eventid):
    collection = conn['pypals'].attendance
    options = [{'college_id': college_id}]
    query = {'$or': options}
    entries = list(collection.find(query))

    if len(entries) == 0:
        attend = collection.Attendance()
        attend['college_id'] = college_id
        attend['talks_attended'] = [str(eventid)]
        attend.save()
        return jsonify({ "success": True, "message": "Congratulations " + str(college_id) + " on attending your first talk!" })
    else:
        cursor = collection.find(query)
        attend = [doc for doc in cursor][0]
        ta = attend['talks_attended']
        if eventid not in ta:
            ta.append(eventid)
            attend['talks_attended'] = ta
            collection.update(
            {"college_id": college_id},
            {
            "$set": {
                "talks_attended":ta
            }
            }, upsert=False, multi=False)
            return jsonify({ "success": True, "message": "Thank you " + str(college_id) + " for attending another talk." })
        else:
            return jsonify({ "success": True, "message": "You've already attended this talk, " + str(college_id) + "." })


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="Not Found"), 404

@app.errorhandler(400)
def bad_request(e):
    return render_template('404.html', title="Bad request"), 400

if __name__ == "__main__":
    app.run(port = 8000, debug=True)
