from main import App
from . import model

@App.path(path='')
class Root(object):
    pass

@App.path(model=model.TodoList, path='/{todolist}')
def get_list(todolist):
    if todolist != 'todos':
        return None
    else:
        return TodoList.get_or_create(todolist)

@App.path(model=model.Todo, path='/{todolist}/{id}')
def get_todo(todolist, id):
    return Todo.get_todo_object(todolist, int(id))


