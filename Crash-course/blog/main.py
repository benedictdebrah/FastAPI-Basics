from fastapi import FastAPI, Depends, HTTPException, status, Response
import schemas
import models
from typing import List
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import hashing  
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.put('/blog/{id}', status_code=status.HTTP_200_OK, tags=['blogs'])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')

    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog {id} not found')  

    db.delete(blog)
    db.commit()
    return {'message': 'Blog deleted successfully'}


@app.get('/blog', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog], tags=['blogs']) 
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blogs'])
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    return blog









#USERS





@app.post('/user',response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    try:
        new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))  
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error creating user: {str(e)}')

@app.get('/user/{id}', response_model=schemas.ShowUser, status_code=status.HTTP_200_OK, tags=['users']) 
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f'User with id {id} not found')
    return user



