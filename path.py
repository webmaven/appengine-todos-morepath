from main import App
from . import model

@App.path('')
class Root(object):
    pass

@App.path(model=model.TodoList, path='/{todolist}')
def get_list(todolist, request):
    return TodoList.get_or_create(todolist)

@App.path(model=model.Todo, path='/{todolist}/{id}')
def get_list_todo(todolist, id, request):
    return Todo.get_todo_object(todolist, int(id))


