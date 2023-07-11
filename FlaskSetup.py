from flask import Flask, jsonify, request
import sqlite3
from pymongo import MongoClient
app = Flask(__name__)


# get api
@app.route('/data', methods=['GET'])
def get_data():
    """
    connects to a sqlite database and retrieves all data from 'companies' table.
    :return: returns the data in JSON
    """
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM companies")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)


# post api
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["purified"]
@app.route("/save", methods=["POST"])
def post_data():
    """
    connects to a mongoDB database and inserts the received data
    :return: JSON response indicating success
    """
    data = request.get_json()
    collection = db["companies"]
    collection.insert_many(data)
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(debug=True)
