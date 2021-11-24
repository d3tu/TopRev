#!/usr/bin/env python

from flask import Flask, jsonify, request, render_template, make_response, redirect
from lotusdb import Database
import uuid

db = Database()
users = Database('./users.db')
posts = Database('./posts.db')
app = Flask(__name__)


def f_topics(max=5):
    i = 0
    data = []

    def find_topics(x):
        if i == max: return True
        if x['t'] == 't':
            ++i
            data.append(x['n'])
        db.find(find_topics)
        return data


@app.route('/')
def index():
    logged = False
    user = None
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    if username:
        if password:
            userdb = users.find(lambda x: x['u'] == username)
            if userdb:
                if userdb['p'] == password:
                    logged = True
                    user = userdb
    return render_template('index.html',
                           d_topics=f_topics(),
                           logged=logged,
                           user=user)


@app.route('/perfil')
def perfil():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    res = make_response(redirect('/login'))
    if username:
        if password:
            userdb = users.find(lambda x: x['u'] == username)
            if userdb:
                if userdb['p'] == password:
                    return render_template('perfil.html', user=userdb)
                else:
                    return res
            else:
                return res
        else:
            return res
    else:
      return res

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route('/logout')
def logout():
    res = make_response(redirect('/'))
    res.set_cookie('username', '', max_age=0)
    res.set_cookie('password', '', max_age=0)
    return res


@app.route('/login', methods=['POST'])
def login_post():
    f = request.form
    if not f['username'] or not f['password']:
        return make_response(redirect('/login'))
    user = users.find(lambda x: x['u'] == f['username'])
    if user:
        if user['p'] == f['password']:
            res = make_response(redirect('/'))
            res.set_cookie('username', f['username'])
            res.set_cookie('password', f['password'])
            return res
        else:
            return make_response(redirect('/login'))
    else:
        users.put({
            'i': str(uuid.uuid4()),
            'u': f['username'],
            'p': f['password']
        })
        res = make_response(redirect('/'))
        res.set_cookie('username', f['username'])
        res.set_cookie('password', f['password'])
        return res


@app.route('/posts')
def route_posts():
  i = 0; data = []
  def find(x):
    if i > 10: --i; data.pop(0)
    if not 'r' in x: data.append(x)
  posts.find(find); return jsonify(data)

app.run(host='0.0.0.0', port=8080)
