from main import App
from . import model

@App.path(model=model.Root, path='')
def get_root():
    return model.Root


@App.path(model=model.TodoList, path='/{todolist}')
def get_list(todolist):
    if todolist != 'todos':
        return None
    else:
        return model.TodoList.get_or_create(todolist)

@App.path(model=model.Todo, path='/{todolist}/{id}')
def get_todo(todolist, id):
    return model.Todo.get_todo_object(todolist, int(id))


