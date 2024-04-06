from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

uri = "mongodb+srv://anushkabhattcs22:1VO3QqgJUuu7wjYe@cluster1.qjgvh5c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
client  = MongoClient(uri)
db = client.mars_db

@app.route('/')
def home():
    return render_template('mars.html')

@app.route('/mars', methods = ['POST'])
def save_data():
    name = request.form['name']
    address = request.form['address']
    size = request.form['size']
    print(name,address,size)
    db.mars_orders.insert_one({
        'name':name,
        'address':address,
        'size':size
    })
    return jsonify({'msg':'Data saved successfully!'})

@app.route('/mars', methods = ['GET'])
def get_data():
    orders = list(db.mars_orders.find({},{'_id':False}))
    return jsonify({'orders': orders})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)