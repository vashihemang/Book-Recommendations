from flask import Flask,render_template,request
import pickle
import numpy as np

popular=pickle.load(open(r"popular.pkl","rb"))
books=pickle.load(open(r"Books.pkl","rb"))
pt=pickle.load(open(r"pt.pkl","rb"))
similarity_scores=pickle.load(open(r"similarity_scores.pkl","rb"))

app = Flask(__name__,template_folder="template")

@app.route('/')
def home():
    return render_template('home.html',
                           book_name=list(popular["Book-Title"].values),
                           autor=list(popular["Book-Author"].values),
                           image=list(popular["Image-URL-M"].values),
                           rating=list(popular["avg_rating"].values))

@app.route('/rcommander')
def Recommender():
    return render_template('Recommander.html')

@app.route('/rcommander_book',methods=["POST"])
def recommend():
    user_input = request.form.get('user_input')
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

    return render_template('Recommander.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)