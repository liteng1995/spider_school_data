from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():

    def aa(name=''):
        print("aaaa"+name)
        return None;

    return 'Hello World!'


if __name__ == '__main__':
    app.run()



