from helper import Helper
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

helper = Helper()

@app.route('/health/', methods=['GET'])
def health_check():
    return jsonify("Service is healthy.")

@app.route('/books/', methods=['POST'])
def retrieve_books():
    data = request.get_json()
    query = data.get('query')

    books = helper.retrieve_books_helper(query)
    return books

@app.route('/books/<string:ia_id>/words/', methods=['GET'])
def retrieve_words(ia_id):
    return helper.retrieve_words_helper(ia_id)

if __name__=="__main__":
    app.run(host='0.0.0.0', port=105)