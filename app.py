from flask import Flask, render_template, redirect, request
app = Flask(__name__)

@app.route("/")
def main():
    return redirect(u'/\u03BCpy')

@app.route("/repo")
def repo():
    return redirect('https://github.com/PyPals')

@app.route("/website-repo")
def web_repo():
    return redirect('https://github.com/PyPals/pypals-website')

@app.route(u'/\u03BCpy')
def mu_py():
    return render_template('index.html')

@app.route("/py")
def py():
    return render_template('test.py')

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

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    _email = request.form['email']
    _password = request.form['password']
    print _email
    return redirect('/login')

@app.route('/validateSignup',methods=['POST'])
def validateSignup():
    _username = request.form['username']
    _email = request.form['email']
    _password = request.form['password']
    _tshirt_size = request.form['tshirt_size']
    print _tshirt_size
    return redirect('/signup')

if __name__ == "__main__":
    app.run(port = 3000)
