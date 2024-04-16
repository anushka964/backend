from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
uri = "mongodb+srv://anushkabhattcs22:1VO3QqgJUuu7wjYe@cluster1.qjgvh5c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
client = MongoClient(uri)
db = client.bucketlist_db
@app.route('/')
def home():
    return render_template('bucketlist.html')

@app.route('/bucket', methods = ["POST"])
def save_bucket():
    bucket_item = request.form['bucket_item']
    count = db.bucketlist_db.count_documents({})

    doc = {
        'index': count + 1,
        'bucket': bucket_item,
        'done': 0
    }
    
    db.bucketlist_db.insert_one(doc)
    return jsonify({
        'msg': 'save success'
    })

@app.route('/bucket', methods = ["GET"])
def get_bucket():
    bucket_list = list(db.bucketlist_db.find({}, {'_id':False}))
    return jsonify({'buckets':bucket_list})

@app.route('/done', methods = ["POST"])
def bucket_done():
    index = request.form['item_index']
    db.bucketlist_db.update_one({'index':int(index)}, {'$set':{'done':1}})
    return jsonify({'msg':'updated'})

@app.route('/delete', methods = ["POST"])
def bucket_delete():
    index = request.form['item_index']
    db.bucketlist_db.delete_one({'index':int(index)})
    return jsonify({'msg':'deleted'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
