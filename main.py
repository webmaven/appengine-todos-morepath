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

class App(morepath.App):
    pass


@App.path('')
class Root(object):
    pass

@App.html(model=Root)
def hello_world(self, request):
    """Return a friendly HTTP greeting."""
    return '<p><a href="/todos/">/todos</a></p>'

@App.path(model=TodoList, path='/{todolist}')
def get_list(todolist, request):
    return TodoList.get_or_create(todolist)

@App.json(model=TodoList, request_method='GET')
def get_all_todos(self, request):
    return self.get_all_todos()

@App.json(model=TodoList, request_method='POST')
def add_todo(self, request):
    @request.after
    def return_code(response):
        response.status_code = 201
    return self.add_todo(request.json['title'])

@App.json(model=TodoList, request_method='PUT')
def archive_todos(self, request):
    return self.update_todo(request.json['id'],
                            request.json['text'],
                            request.json['completed'])

@App.view(model=TodoList, request_method='DELETE')
def delete_todos(self, request):
    @request.after
    def return_code(response):
        response.status_code = 204
    return self.archive_todos()


@App.path(model=Todo, path='/{todolist}/{id}')
def get_list_todo(todolist, id, request):
    return Todo.get_todo_object(todolist, id)

@App.json(model=Todo, request_method='GET')
def get_todo(self, request):
    return self.get_todo()

@App.json(model=Todo, request_method='PUT')
def put_todo(self, request):
    return self.update_todo(request.json['id'],
                            request.json['text'],
                            request.json['completed'])


@App.json(model=Todo, request_method='DELETE')
def delete_todo(self, request):
    @request.after
    def return_code(response):
        response.status_code = 204
    return self.delete_todo()

@App.view(model=HTTPNotFound)
def notfound_custom(self, request):
    """Return a custom 404 error"""
    def set_status_code(response):
        response.status = self.code  # pass along 404
    request.after(set_status_code)
    return "Sorry, Nothing at this URL."


@App.view(model=HTTPInternalServerError)
def servererror_custom(self, request):
    def set_status_code(response):
        response.status = self.code  # pass along 500
    request.after(set_status_code)
    return "Sorry, unexpected error: {}".format(self.detail)

app = App(name='Todos')
config = morepath.setup()
config.scan()
config.commit()
