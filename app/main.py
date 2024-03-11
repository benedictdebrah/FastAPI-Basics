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
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,
                   (new.title, new.content, new.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"message" : "Post created successfully", "data" : new_post}


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
@app.delete("/posts/{id}")
def delete_post(id: int,response : Response):
    #find index
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} does not exit")
    
    #delete it using pop
    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

 
#UPDATE OPERATIONS
@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    #find index
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} does not exit")
    
    #update the post
    my_posts[index] = post.dict()
    return {
        "message" : "Post updated successfully",
        "data" : my_posts[index]
    }

