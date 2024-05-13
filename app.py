from flask import Flask, request, jsonify
import json
import psycopg2

from psycopg2 import Error

      

app = Flask(__name__)
def connexion_db():
    try:
        connexion = psycopg2.connect('postgresql://postgres:admin@localhost:5432/books')
        return connexion
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None
    

@app.route('/',methods=['GET','POST'])     
def books():
    con=connexion_db()
    cursor=con.cursor()
    cursor.execute('SELECT * FROM books_listt') 
    if request.method == 'GET': 
        cursor.execute('SELECT * FROM books_listt')
        books_list=[
                  dict(id=row[0],title=row[1],author=row[2],read=row[3]) 
                  for row in cursor.fetchall()   
                  
              ]
        if books_list is not None:
                  return jsonify(books_list)
    elif request.method == 'POST':
     newtitle = request.form.get('title')
     newauthor = request.form.get('author')  
     newread = request.form.get('read')
    
    # Validation des données du formulaire
     if newtitle is None or newauthor is None or newread is None:
        return "Missing required fields", 400
    
     try:
        sql = '''INSERT INTO books_listt(title,author,read) VALUES(%s,%s,%s)'''
        cursor.execute(sql,(newtitle,newauthor,newread))
        con.commit()
        return f"Book id {cursor.lastrowid} created successfully", 201
     except psycopg2.Error as e:
        # Gestion des erreurs de base de données
        print(f"Error inserting data into database: {e}")
        return "Error inserting data into database", 500
        

@app.route('/books/<int:id>',methods=['GET','PUT','DELETE'])
def index(id):
     con=connexion_db()
     cursor=con.cursor()
     cursor.execute('SELECT * FROM books_listt') 
     book=None
     if request.method == 'GET':
        cursor.execute('SELECT * FROM books_listt WHERE id = %s', (id,))
        book = cursor.fetchone()
        if book is not None:
            return jsonify({'id': book[0], 'title': book[1], 'author': book[2], 'read': book[3]}), 200
        else:
            return 'Book not found', 404
    
     elif request.method == 'PUT':
        newtitle = request.form.get('title')
        newauthor = request.form.get('author')
        newread = request.form.get('read')

        if newtitle is None or newauthor is None or newread is None:
            return "Missing required fields", 400

        try:
            sql = '''UPDATE books_listt SET title = %s, author = %s, read = %s WHERE id = %s'''
            cursor.execute(sql, (newtitle, newauthor, newread, id))
            con.commit()
            return "Book updated successfully", 200
        except psycopg2.Error as e:
            print(f"Error updating data in database: {e}")
            return "Error updating data in database", 500
    
     elif request.method == 'DELETE':
        try:
            sql = '''DELETE FROM books_listt WHERE id = %s'''
            cursor.execute(sql, (id,))
            con.commit()
            return '', 204
        except psycopg2.Error as e:
            print(f"Error deleting data from database: {e}")
            return "Error deleting data from database", 500
if __name__ == '__main__':
    app.run(debug=True)
     