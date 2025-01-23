import pathlib

import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from transify import *

app = FastAPI(title='transify', version='1.0.0')

# Mount static resources
app.mount(
    '/resources',
    StaticFiles(directory=f'{pathlib.Path(__file__).resolve().parent}/resources', html=False),
    name='static'
)

# Jinja2 template setup
templates = Jinja2Templates(
    directory=f'{pathlib.Path(__file__).resolve().parent}/resources'
)

# Update the template environment with the trans function
templates.env.globals.update(trans=trans)

def startup():
    load_languages(path='tests/lang', default_fallback='en')

app.add_event_handler('startup', startup)

@app.get('/', response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request, 'lang': get_locale()})

if __name__ == '__main__':
    uvicorn.run('test_webapp:app', host='localhost', port=8000, reload=True)
