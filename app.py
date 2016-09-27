#!/usr/bin/python
from datetime import datetime
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
        'email': unicode,
        'tshirt_size': unicode,
        'phone': unicode,
        'time': datetime,
    }
    required_fields = ['name', 'college_id', 'email']
    default_values = {'time': datetime.now()}
    use_dot_notation = True
conn = MongoKit(app)
conn.register(User)


@app.route("/")
def main():
    return redirect(u'/\u03BCpy')

@app.route("/repo")
def repo():
    return redirect('https://github.com/PyPals')

@app.route(u'/\u03BCpy')
def mu_py():
    return render_template('index.html')

@app.route("/LUGM")
def lugm():
    return redirect('http://lugm.xyz/')

@app.route("/mupy")
def norm_mupy():
    return redirect(u'/\u03BCpy')

@app.route("/MU3.14159")
def mu_pynum():
    return redirect(u'/\u03BCpy')

@app.route("/proposal")
def proposal():
    return render_template('proposal.html')

@app.route("/conduct")
def conduct():
    return render_template('conduct.html')

@app.route("/faq")
def faq():
    return render_template('faq.html')

@app.route('/sabdedobc')
def curr_reg():
    collection = conn['pypals'].registrations
    a = list(collection.find())
    return jsonify(str(a))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        data = request.get_json()
        payload = {}
        if data is None:
            data = dict(request.form)
            del data['register-submit']
            for i,j in data.iteritems():
                data[i] = data[i][0]
            needed = ''
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
                 message = 'Invalid captcha')
        else:
            if request.headers.get("PyPals-Authorization") != app_key:
                res = {}
                res['success'] = 'false'
                res['error'] = 'invalid source'
                return jsonify(res)
            return add_reg(data, True)

def add_reg(data, json = False):
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
            return render_template('register.html', success = True)
        res['success'] = 'true'
    else:
        message = "User already registered."
        if not json:
            return render_template('register.html', success = False, \
                message = message)
        res['success'] = 'false'
        res['error'] = message
    return jsonify(res)


if __name__ == "__main__":
    app.run(port = 3000)
