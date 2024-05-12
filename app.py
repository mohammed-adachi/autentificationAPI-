from flask import Flask, request, jsonify

app = Flask(__name__)
books_list = [ 
    {   'id': 1,
        'title': 'Clean Code',
        'author': 'Robert C. Martin',
        'read': True
    },
    {   'id': 2,
        'title': 'The Pragmatic Programmer',
        'author': 'Andrew Hunt & David Thomas',
        'read': False
    }
]   
@app.route('/',methods=['GET','POST'])     
def books():
        if request.method == 'GET':
            return jsonify(books_list)
        elif request.method == 'POST':
            newtitle = request.form.get('title')
            newauthor = request.form.get('author')  
            newread = request.form.get('read')
            newid = books_list[-1]['id'] + 1
            newbook = {
                'id': newid,
                'title': newtitle,
                'author':  newauthor,
                'read': newread
            }
            books_list.append(newbook)
            return jsonify(books_list), 201
        

@app.route('/books/<int:id>',methods=['GET','PUT','DELETE'])
def index():
    if request.method == 'GET':
        for book in books_list:
            if book['id'] == id:
                return jsonify(book)
        return 'Book not found', 404
    elif request.method == 'PUT':
        for book in books_list:
            if book['id'] == id:
                book['title'] = request.form.get('title')
                book['author'] = request.form.get('author')
                book['read'] = request.form.get('read')
                updated_book = {
                    'id': id,
                    'title': book['title'],
                    'author': book['author'],
                    'read': book['read']
                }
                return jsonify(updated_book)
        return 'Book not found', 404
    elif request.method == 'DELETE':
        for book in books_list:
            if book['id'] == id:
                books_list.pop(book)
                return jsonify(books_list)
        return 'Book not found', 404
if __name__ == '__main__':
    app.run(debug=True)
     