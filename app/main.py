from fastapi import FastAPI, HTTPException,Response,status
from typing import Optional
from pydantic import BaseModel
from fastapi.params import Body
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
#instantiating the class
app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True

#making connection to the database
while True:
    try:
        conn = psycopg.connect(host='localhost', dbname='fastapi', user='posttest', 
                            password='test1234', row_factory=dict_row)
        cursor = conn.cursor()
        print('Databse connection was successful')
        break

    except Exception as error:
        print('databse connection failed')
        print('error :', error)
        time.sleep(2)




#GET OPERATIONS
@app.get("/")
def root():
    return {"Message" : "This is my first CRUD operation"}

#get all post
@app.get("/posts/")
def get_post():
    cursor.execute("""SELECT * FROM  posts""")
    posts = cursor.fetchall()
    return {"data" : posts}




#POST OPERTIONS
@app.post("/posts/",status_code=status.HTTP_201_CREATED)
def create_post(new : Post):
    try:
        cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,
                       (new.title, new.content, new.published))
        new_post = cursor.fetchone()
        conn.commit()
        return {"message" : "Post created successfully", "data" : new_post}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to create post: " + str(e))


#retrieving an individual 
@app.get("/posts/{id}")
def get_post(id : int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id {id} was not found")

    return {"post detail" : post}
    
#DELETE OPERATIONS
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(id,))
    conn.commit()
    deleted_post = cursor.fetchone()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Post with id {id} does not exist")
 
    return Response(status_code=status.HTTP_204_NO_CONTENT)

 
#UPDATE OPERATIONS
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id:int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *
                   """,(post.title, post.content, post.published, id))
    conn.commit()
    updated_post = cursor.fetchone()

    if updated_post is None:
        raise HTTPException(status_code=404, detail= f"Post with id {id} does not exist")
    
    return {"message" : "Post updated successfully", "data" : updated_post}

