from calendar import c
from turtle import pos, st
from typing import Optional
from fastapi import FastAPI, HTTPException, status

from typing import Any
from pydantic import BaseModel, Field
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str = Field(..., min_length=3, max_length=300)
    content: str = Field(..., min_length=10, max_length=3000)
    is_published: Optional[bool] = Field(True)
    rating: Optional[float] = Field(None, ge=0, le=5)


posts = [
    {'id': 1, 'title': 'Post 1', 'content': 'Content of post 1',
        'is_published': True, 'rating': 4.5},
    {'id': 2, 'title': 'Post 2', 'content': 'Content of post 2',
        'is_published': False, 'rating': 4.0},
]


def find_post(id: int) -> Optional[dict]:
    for p in posts:
        if p['id'] == id:
            return p
    return None


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello World"}


# POSTS endpoint:
@app.get("/posts")
def get_posts() -> dict[str, list[dict]]:
    return {'data': posts}


@app.get('/posts/{id}')
def get_post(id: int) -> dict[str, Any]:
    result = find_post(id)

    print(type(id))

    if result:
        return {'data': result}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: Post) -> dict[str, bool | dict]:
    print(payload)

    print(payload.model_dump())

    post_dict = payload.model_dump()
    post_dict['id'] = randrange(0, 1000000000)

    posts.append(post_dict)

    return {
        'successfully_created': True,
        'data': post_dict
    }
