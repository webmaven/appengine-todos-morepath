"""`main` is the top level module for your Morepath application."""

# Import the Morepath Framework
import morepath

"""Todo Morepath backend demo.

This is a sample Morepath JSON backend for a todo app.

It support the following methods:
- Create a new todo
POST /todos
> {"text": "do this"}
201 /todos/1
< {"id": 1, "text": "do this", "completed": false}
- Update an existing todo
PUT /todos/1
> {"id": 1, "text": "do this", "completed": true}
< {"id": 1, "text": "do this", "completed": true}
- List existing todos:
GET /todos
>
< [{"id": 1, "text": "do this", "completed": true},
   {"id": 2, "text": "do that", "completed": false}]
- Delete 'done' todos:
DELETE /todos
>
< [2]
"""

class App(morepath.App):
    pass

app = App(name='Todos')
config = morepath.setup()
config.commit()

