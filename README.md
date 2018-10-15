Assume `python`, `pip`, `mongodb` have been installed.

In stall `flask` and `flask_pymong`
```
sudo pip install flask
sudo pip install flask_pymongo
```
Run
```
export FLASK_APP=blog-flask-mongodb
export FLASK_ENV=development
flask run
```

In a new terminal, run
`mongod`

In browser, test
```
http://localhost:5000/add/fanzhang
http://localhost:5000/find/fanzhang
http://localhost:5000/update/fanzhang
http://localhost:5000/delete/fanzhang
```

Inspired by:
```
https://www.58jb.com/html/170.html
```

