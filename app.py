#!/usr/bin/python
from datetime import datetime
from flask import Flask, render_template, redirect, request, jsonify
from flask_mongokit import MongoKit, Document

app = Flask(__name__)

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
        if request.get_json() is None:
            data = dict(request.form)
            del data['register-submit']
            for i,j in data.iteritems():
                data[i] = data[i][0]
        collection = conn['test'].registrations
        user = collection.User()
        for i,j in data.iteritems():
            user[i] = data[i]
        user.save()
        return redirect("/register")

if __name__ == "__main__":
    app.run(port = 3000)
