from flask import Flask
import requests
app = Flask(__name__)

@app.route('/')
def hello_world():
    inputStr = requests.args.get('inputstr','')
    response = requests.get('https://httpbin.org/anything')
    print('Hello, World!')
    return {
        response.json()
    }
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=50004)