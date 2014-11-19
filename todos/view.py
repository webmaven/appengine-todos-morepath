from main import App
from . import model
from webob.exc import HTTPNotFound, HTTPInternalServerError


@App.html(model=model.Root)
def hello_world(self, request):
    """Return a friendly HTTP greeting."""
    return '<p><a href="/todos/">/todos</a></p>'

@App.json(model=model.TodoList, request_method='GET')
def get_all_todos(self, request):
    return self.get_all_todos()

@App.json(model=model.TodoList, request_method='POST')
def add_todo(self, request):
    @request.after
    def return_code(response):
        response.status_code = 201
    return self.add_todo(request.json['title'])

@App.json(model=model.TodoList, request_method='PUT')
def archive_todos(self, request):
    return self.update_todo(request.json['id'],
                            request.json['text'],
                            request.json['completed'])

@App.view(model=model.TodoList, request_method='DELETE')
def delete_todos(self, request):
    @request.after
    def return_code(response):
        response.status_code = 204
    return self.archive_todos()


@App.json(model=model.Todo, request_method='GET')
def get_todo(self, request):
    return self.get_todo()

@App.json(model=model.Todo, request_method='PUT')
def put_todo(self, request):
    return self.update_todo(request.json['title'],
                            request.json['completed'])


@App.json(model=model.Todo, request_method='DELETE')
def delete_todo(self, request):
    @request.after
    def return_code(response):
        response.status_code = 204
        response.content_type='text/plain'
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

