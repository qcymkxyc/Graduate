from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap()
bootstrap.init_app(app)


@app.route('/',methods=["GET","POST"])
def hello_world():
    return render_template("/base.html")


if __name__ == '__main__':
    app.run(debug=True)
