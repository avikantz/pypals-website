from flask import Flask, render_template, redirect
app = Flask(__name__)

@app.route("/")
def main():
    return redirect('/MU3.14159', code = 302)
    
@app.route("/repo")
def repo():
    return redirect('https://github.com/PyPals')

@app.route("/website-repo")
def web_repo():
    return redirect('https://github.com/PyPals/pypals-website')

@app.route("/MU3.14159")
def mu_py():
    return render_template('index.html')

if __name__ == "__main__":
    app.debug = True
    app.run(port = 3000)

