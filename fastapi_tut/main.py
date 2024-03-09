from fastapi import FastAPI, HTTPException,Response,status
from typing import Optional
from pydantic import BaseModel
from fastapi.params import Body
from random import randrange

#instantiating the class
app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : Optional[bool] = True
    rating : Optional[int] = None


#to store values
my_posts = [
       {"title" : "my favourite food",
     "content" : "my favourite food is fufu and abenkwan",
     "rating" : 5,
     "id" : 2},
      {"title" : "my favourite game",
     "content" : "my favourite game is minecraft",
     "rating" : 7,
     "id" : 4}
]

# function to find_by _index
def find_post(id):
    for i in my_posts:
        if i['id'] == id:
            return i
        

#function to delete post
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


#GET OPERATIONS
@app.get("/")
def root():
    return {"Message" : "This is my first CRUD operation"}

#get all post
@app.get("/posts/")
def get_post():
    return {
        "data" : my_posts
    }


#retrieving an individual 
@app.get("/posts/{id}")
def get_post(id : int):
    post = find_post(id)

    #invalid id
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")


    print(post)
    return {"post detail" : post}



#POST OPERTIONS
@app.post("/posts/")
def create_post(new : Post):
    new_dict = new.dict()
    new_dict['id'] = randrange(1,1000000)
    my_posts.append(new_dict)

    return {
        "message" : "Post created successfully",
        "data" : new_dict
    }

    
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
