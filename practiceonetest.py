from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Jesse's blog app!"

    if __name__ == '__main__':
        app.run()