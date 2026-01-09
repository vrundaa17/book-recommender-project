import numpy as np
import pandas as pd

def recommend(book,similarity,books,pt):
    '''Recommend book function | book=book_name , similarity = similarity_score , books=list_of_books_df, pt=pivot_table'''
    idx = np.where(pt.index==book)[0][0]
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
    return data