from flask import Flask,render_template,request
import pickle
import pandas as pd
import numpy as np
import os 

MODEL_PATH = os.path.join(os.path.dirname(__file__),'model')

with open(os.path.join(MODEL_PATH,'popular.pkl'),'rb') as f :
    popular_df = pickle.load(f)

with open(os.path.join(MODEL_PATH,'pt.pkl'),'rb') as f :
    pt = pickle.load(f)
    
with open(os.path.join(MODEL_PATH,'similarity.pkl'),'rb') as f :
    similarity = pickle.load(f)
    
with open(os.path.join(MODEL_PATH,'book.pkl'),'rb') as f :
    books = pickle.load(f)



book_name = list(popular_df['Book-Title'].values)
author = list(popular_df['Book-Author'].values)
image = list(popular_df['Image-URL-M'].values)
votes = list(popular_df['num_rating'].values)
rating = list(popular_df['avg_rating'].values)    


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',book_name=book_name,author=author,image=image,votes=votes,rating=rating)


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_book = request.form.get('user_book')
    
    if user_book not in pt.index:
        return render_template('recommend.html',error = 'Sorry, the book cannot be found.')
    idx = np.where(pt.index==user_book)[0][0]
    distance = similarity[idx]
    book_list = sorted(list(enumerate(distance)),reverse=True, key = lambda x: x[1])[1:6]

    data=[]
    for i in book_list :
        item =[]
        # print (pt.index[i[0]])
        temp_df = books[books['Book-Title']==pt.index[i[0]]].drop_duplicates('Book-Title')
        # print(temp_df)
        item.extend(temp_df['Book-Title'].values)
        item.extend(temp_df['Book-Author'].values)
        item.extend(temp_df['Image-URL-M'].values)

        data.append(item)
    print(data)
    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)