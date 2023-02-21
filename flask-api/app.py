from flask import Flask
import time

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def hello():
    return "hello world!"
    
@app.route("/slow")
def slow():
    time.sleep(20) # slower than the idle timeout configured in nginx.conf so will return a 504
    return "hello world!"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
