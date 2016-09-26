#!/usr/bin/python
from datetime import datetime
from flask import Flask, render_template, redirect, request, jsonify
from flask_mongokit import MongoKit, Document
import requests

app = Flask(__name__)

recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
recaptcha_key = '***REMOVED***'

class User(Document):
    __collection__ = 'test'
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
    collection = conn['test'].registrations
    a = list(collection.find())
    return jsonify(str(a))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        data = {}
        payload = {}
        if request.get_json() is None:
            data = dict(request.form)
            del data['register-submit']
            for i,j in data.iteritems():
                data[i] = data[i][0]
            needed = ''
            try:
                payload['response'] = data['g-recaptcha-response']
            except Exception:
                payload['response'] = ''
        payload['secret'] = recaptcha_key
        res = requests.post(recaptcha_url, data = payload)
        print res.json()['success']
        if res.json()['success']:
        # if True:
            collection = conn['test'].registrations
            query = {}
            options = []
            options.append({'email': data['email']})
            options.append({'college_id': data['college_id']})
            query['$or'] = options
            entries = list(collection.find(query))#.count()
            if len(entries) == 0:
                del data['g-recaptcha-response']
                user = collection.User()
                for i,j in data.iteritems():
                    user[i] = data[i]
                user.save()
                return render_template('register.html', success = True)
            else:
                message = "User already registered."
                return render_template('register.html', success = False, \
                    message = "User already registered.")
        else:
            return render_template('register.html', success = False,\
             message = 'Invalid captcha')

if __name__ == "__main__":
    app.run(port = 3000)
