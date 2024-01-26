from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
popular_df1 = pickle.load(open('popular1.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
print(popular_df1.columns)


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", book_name = list(popular_df1['Book-Title'].values)
                           ,author=list(popular_df1['Book-Author'].values)
                           ,image=list(popular_df1["Image-URL-M"].values)
                           ,rating=list(popular_df1['num_ratings'].values)
                           ,avg_rating=list(popular_df1['avg-ratings'].values))



@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('User Input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)




if __name__ == "__main__":
    app.run(debug=True)