from flask import Flask, render_template
from flask_pymongo import PyMongo
from config import MongoDB

app = Flask(__name__)
app.config.from_object(MongoDB)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/test"

mongo = PyMongo(app)

# or use these two lines
# mongo.init_app(app,config_prefix="MONGO%")

@app.route('/')
def index():
    # test if connected
    onlines_users = mongo.db.system.users.find()
    return render_template('index.html', onlines_usersonlines_users=onlines_users)



@app.route('/add/<username>')
def add(username):
    user = mongo.db.users
    username = user.find_one({"username": username})
    if username:
        return "The user name: " + username["username"] + " has existed!"
    else:
        user.insert({"username": username, "password": "123456"})
        return "Added User!"



@app.route('/find/<username>')
def find(username):
    user = mongo.db.users
    username = user.find_one({"username": username})
    if username:
        return "The user name is: " + username["username"] + " The password is:" + username["password"]
    else:
        return "The user is not existed!"



@app.route('/update/<username>')
def update(username):
    user = mongo.db.users
    passwd = "abcd10023"
    username = user.find_one({"username": username})
    if username:
        username["password"] = passwd
        user.save(username)
        return "Update OK " + username["username"]
    else:
        return "The user is not existed!"



@app.route('/delete/<username>')
def delete(username):
    user = mongo.db.users
    username = user.find_one({"username": username})
    if username:
        user.remove(username)
        return "Remove " + username["username"] + " Ok!"
    else:
        return "The users is not existed!"


if __name__ == '__main__':
    app.run(debug=True)