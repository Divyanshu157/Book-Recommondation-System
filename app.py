from flask import Flask , url_for,request,render_template
import pandas as pd
import numpy as np
import joblib
import pickle
import warnings
warnings.filterwarnings('ignore')


#load the models
popular = pickle.load(open('popularity_based/popular.pkl','rb'))
pt =  joblib.load('collaborative_models/pivot_table_data.lb')
similarity_score=joblib.load('collaborative_models/similarity_score.lb')
books = joblib.load('collaborative_models/collaborative_recmdsystem_data.lb')


app=Flask(__name__,template_folder='templates')
@app.route('/')
def home():
    return render_template('index.html',
                           book_name= list(popular['Book-Title'].values),
                           author = list(popular['Book-Author'].values),
                           image=list(popular['Image-URL-M'].values),
                           votes=list(popular['num_rating'].values),
                           rating =list(popular['avg_rating'].values),
                           publisher =  list(popular['Publisher'].values))

#function to get BookName
@app.route('/BookName')
def get_book_name():
    book_name= list(pd.read_csv('collaborative_models/unique_book_name.csv')['Book-Title'].values)
    return render_template("bookname.html",list_of_book_name=book_name)

#to get popularity based recommendation system
@app.route('/recommend1')
def recommmend1():
    return render_template('popular.html',
                           book_name= list(popular['Book-Title'].values),
                           author = list(popular['Book-Author'].values),
                           image=list(popular['Image-URL-M'].values),
                           votes=list(popular['num_rating'].values),
                           rating =list(popular['avg_rating'].values),
                           publisher =  list(popular['Publisher'].values)
                           
                           )

@app.route('/recommend2')
def recommend2():
    return render_template('/recommondation.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    
    try:
        user_input=request.form.get('user_input')
        index=np.where(pt.index==user_input)[0][0]
        similar_item=sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:9]
    except:
        return render_template('error.html')
    else:
        data=[]
        for i in similar_item:
            item=[]
            temp_df = books[books['Book-Title']==pt.index[i[0]]]
            
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Publisher'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
            
            data.append(item)
            
        return render_template('/recommondation.html',data=data)
   


if __name__ == '__main__':
    app.run(debug=True)


