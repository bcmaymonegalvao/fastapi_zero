from http import HTTPStatus
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title='Minha API')
database = []

# Diretório contendo arquivos estáticos
app.mount(
    '/static', StaticFiles(directory=str(BASE_DIR / 'static')), name='static'
)

# Diretório contendo os templates Jinja
templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}


@app.get(
    '/exercicio_1', status_code=HTTPStatus.OK, response_class=HTMLResponse
)
def exercicio_1():
    return """
        <html>
            <head>
                <title>Exercício: Aula 2</title>
            </head>
            <body>
                <h1>Olá Mundo!</h1>
            </body>
        </html>"""


# @app.get('/{nome}', response_class=HTMLResponse)
# def home(request: Request, nome: str):
#     return templates.TemplateResponse(
#         request=request, name='index.html', context={'nome': nome}
#     )


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.get(
        '/users/',
        status_code=HTTPStatus.OK,
        response_model=UserList
)
def read_users():
    return {'users': database}


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=user_id)

    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Deu ruim! Não achei...'
        )

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Deu ruim! Não achei...'
        )
    return database.pop(user_id - 1)
