#!flask/bin/python
from flask import Flask, jsonify, make_response, request, abort
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
import requests
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import exc

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import model
from model import User

def check_quorum():
    active_quorums = []
    list = json.load(open('list.json'))
    count_active_quorum = 0
    total_quorum = len(list)
    # return list, 1
    for item in list:
        print(item)
        r = requests.post('http://{}/ewallet/ping'.format(item['ip']))
        value = r.json()['pingReturn']
        print(value)
        if value == 1:
            count_active_quorum += 1
            active_quorums.append(item)
    persentage = count_active_quorum / total_quorum
    print(count_active_quorum)
    return active_quorums, persentage

@app.route('/ewallet/ping', methods=['POST'])
def get_ping():
    try:
        return jsonify({"pingReturn": 1})
    except Exception:
        return jsonify({"pingReturn": -99})

@app.route('/ewallet/register', methods=['POST'])
def register():
    if not request.json or not 'user_id' in request.json or not 'nama' in request.json: 
        abort(400)

    try:
        user_id = request.json["user_id"]
        nama = request.json["nama"]

        if not (check_quorum()[1] > 0.5):
            return jsonify({"registerReturn": -2})
        else:
            u = User(user_id=user_id, name=nama, saldo=0)
            db.session.add(u)
            db.session.commit()
            return jsonify({"registerReturn": 1})
    except exc.SQLAlchemyError:
        return jsonify({'registerReturn': -4})
    except:
        return jsonify({"registerReturn": -99})

@app.route('/ewallet/getSaldo', methods=['POST'])
def get_saldo():
    try:
        user_id = request.json["user_id"]
        user = User.query.get(user_id)

        if not user:
            return jsonify({'saldo': -1})
        elif not (check_quorum()[1] > 0.5):
            return jsonify({'saldo': -2})
        else:
            return jsonify({'saldo': user.saldo})
    except exc.SQLAlchemyError:
        return jsonify({'saldo': -4})
    except Exception:
        return jsonify({'transferReturn': -99})

@app.route('/ewallet/getTotalSaldo', methods=['POST'])
def get_total_saldo():
    if not request.json or not 'user_id' in request.json:
        abort(400)
    try:
        user_id = request.json["user_id"]
        user = User.query.get(user_id)

        if not user:
            return jsonify({'saldo': -1})
        elif not (check_quorum()[1] == 1):
            return jsonify({'saldo': -2})
        else:
            sum = 0
            kantorCabangDomisili = None
            active_quorums = check_quorum()[0]
            for item in active_quorums:
                if item['npm'] == user_id:
                    kantorCabangDomisili = item['ip']
            if kantorCabangDomisili != '127.0.0.1:80':
                r = requests.post('http://{}/ewallet/getTotalSaldo'.format(kantorCabangDomisili), json={"user_id": user_id})
                return r.text
            else:
                for item in active_quorums:
                    r = requests.post('http://{}/ewallet/getSaldo'.format(item['ip']), json={"user_id": user_id})
                    if r.json()["saldo"] < 0:
                        return jsonify({'saldo': -3})
                    sum += r.json()["saldo"]
                return jsonify({'saldo': sum})
    except requests.exceptions.ConnectionError:
        return jsonify({'saldo': -3})
    except Exception:
        return jsonify({'saldo': -99})

@app.route('/ewallet/transfer', methods=['POST'])
def transfer():
    if not request.json or not 'user_id' in request.json or not 'nilai' in request.json: 
        abort(400)

    try:
        user_id = request.json["user_id"]
        nilai = request.json["nilai"]
        user = User.query.get(user_id)

        if not user:
            return jsonify({'transferReturn': -1})
        elif not (check_quorum()[1] > 0.5):
            return jsonify({'transferReturn': -2})
        elif nilai > 1000000000 or nilai < 0:
            return jsonify({'transferReturn': -5})
        else:
            user.saldo = user.saldo + nilai
            db.session.commit()
            return jsonify({'transferReturn': 1})
    except exc.SQLAlchemyError:
        return jsonify({'transferReturn': -4})
    except Exception:
        return jsonify({'transferReturn': -99})

def kurangiSaldo():
    if not request.json or not 'user_id' in request.json or not 'nilai' in request.json: 
        abort(400)

    try:
        user_id = request.json["user_id"]
        nilai = request.json["nilai"]
        user = User.query.get(user_id)

        if not user:
            return jsonify({'transferReturn': -1})
        elif not (check_quorum()[1] > 0.5):
            return jsonify({'transferReturn': -2})
        elif nilai > 1000000000 or nilai < 0:
            return jsonify({'transferReturn': -5})
        else:
            user.saldo = user.saldo + nilai
            db.session.commit()
            return jsonify({'transferReturn': 1})
    except exc.SQLAlchemyError:
        return jsonify({'transferReturn': -4})
    except Exception:
        return jsonify({'transferReturn': -99})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=False)