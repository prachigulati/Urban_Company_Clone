from flask import Flask # type: ignore
app=Flask(__name__)
@app.route("/")
def home():
    return "Welcome"
if __name__ == "__main__":
    app.run()

