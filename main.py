"""`main` is the top level module for your Morepath application."""

# Import the Morepath Framework
import morepath
from webob.exc import HTTPNotFound, HTTPInternalServerError

from todos import TodoList, Todo

"""Todo Morepath backend demo.

This is a sample Morepath JSON backend for a todo app.

It support the following methods:
- Create a new todo
POST /todos
> {"text": "do this"}
201 /todos/1
< {"id": 1, "text": "do this", "created": 1356724843.0, "done": false}
- Update an existing todo
PUT /todos/1
> {"id": 1, "text": "do this", "created": 1356724843.0, "done": true}
< {"id": 1, "text": "do this", "created": 1356724843.0, "done": true}
- List existing todos:
GET /todos
>
< [{"id": 1, "text": "do this", "created": 1356724843.0, "done": true},
   {"id": 2, "text": "do that", "created": 1356724849.0, "done": false}]
- Delete 'done' todos:
DELETE /todos
>
< [2]
"""

app = morepath.App(name='Todos')

@app.path('')
class Root(object):
    pass

@app.html(model=Root)
def hello_world(self, request):
    """Return a friendly HTTP greeting."""
    return '<p><a href="/todos/">/todos</a></p>'

alltodos = TodoList.get_or_create('default')

@app.path(model=TodoList, path='/todos')
def get_list(request):
    return alltodos

@app.json(model=TodoList, request_method='GET')
def get_all_todos(self, request):
    return self.get_all_todos()

@app.json(model=TodoList, request_method='POST')
def add_todo(self, request):
    return self.add_todo(request.title)

@app.json(model=TodoList, request_method='PUT')
def archive_todos(self, request):
    return self.update_todo(request.id, request.text, request.completed)

@app.json(model=TodoList, request_method='DELETE')
def add_todo(self, request):
    return self.archive_todos()


#@app.path(model=Todo, path='/todos/{id}')
#def get_todo(id):
    #return Todo.query(id=id)

#@app.json(model=Todo)
#def todo_data(self, request):
    #return self

#@app.

@app.view(model=HTTPNotFound)
def notfound_custom(self, request):
    """Return a custom 404 error"""
    def set_status_code(response):
        response.status = self.code  # pass along 404
    request.after(set_status_code)
    return "Sorry, Nothing at this URL."


@app.view(model=HTTPInternalServerError)
def servererror_custom(self, request):
    def set_status_code(response):
        response.status = self.code  # pass along 500
    request.after(set_status_code)
    return "Sorry, unexpected error: {}".format(self.detail)

config = morepath.setup()
config.scan()
config.commit()
