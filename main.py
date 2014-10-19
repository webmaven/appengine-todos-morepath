"""`main` is the top level module for your Morepath application."""

# Import the Morepath Framework
import morepath
from webob.exc import HTTPNotFound, HTTPInternalServerError

from todos import TodoList

"""Todo Flask backend demo.

This is a sample Flask JSON backend for a todo app.

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

app = morepath.App(name='Hello')
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.path('')
class Root(object):
    pass

@app.view(model=Root)
def hello_world(self, request):
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.path(model=TodoList, path='/todo')
def get_list(todo_list_name):
    return TodoList.get_or_create('default')

#@app.json(model=TodoList)
#def get_todos(self, request):
    #print self
    #todo_list =  self.get_all_todos()
    #print todo_list
    #return todo_list
    ##return {
        ##'id': self.key.id(),
        ##'text': self.text,
        ##'done': self.done,
        ##'created': self.created.isoformat()
            ##}


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
