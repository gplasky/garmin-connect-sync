# Homework
# Using the json file and python code from class,
# set up a flask program to receive:
#   GET call: return the name of a customer given the customer email
#   POST call: change the name of an existing customer given the name and email

import json
from flask import Flask, request, abort

app = Flask(__name__, template_folder='')
app.config['TEMPLATES_AUTO_RELOAD'] = True


class EmailList():

    def __init__(self):
        with open('flask_data.json') as f:
            self.data = json.load(f)

    def print_list(self):
        return self.data

    def update_email_if_exists(self, name, email):
        if not self.find_name_by_email(email):
            return False

        self.data[email] = name
        with open('flask_data.json', 'w') as f:
            json.dump(self.data, f)

        return True

    def find_name_by_email(self, email):
        for k, v in self.data.items():
            if k == email:
                return v

        return False


@app.route('/', methods=["GET"])
def slash():
    abort(418)


@app.route('/hello_world', methods=["GET"])
def hell_world():
    return "Hello World"


@app.route('/get_data', methods=["GET"])
def get_data():
    el = EmailList()
    email = request.args.get('email')

    if email is None:
        abort(400)

    name = el.find_name_by_email(email)

    return name if name else abort(404, description="Email {} not found.".format(email))


@app.route('/post_data', methods=["POST"])
def post_data():
    el = EmailList()
    email = request.args.get('email')
    name = request.args.get('name')

    if name is None or email is None:
        abort(400)

    update = el.update_email_if_exists(name, email)

    if not update:
        # Email not found
        abort(404)

    return el.print_list()


if __name__ == "__main__":
    app.run()
