"""Todos storage.

This module defines 2 models for modeling list of todos:
- TodoList
- Todo

And a set of common operations for managing them:
- TodoList.create        # create a new todo list.
- TodoList.add_todo      # add a new todo to the list.
- TodoList.update_todo   # update an existing todo in the list.
- TodoList.get_all_todos # get all todos from the list.
- TodoList.archive_todos # archive all done todos from the list.
- Todo.get # get the todo.
- Todo.update # update an existing todo.
- Todo.delete # delete the todo.
"""

from google.appengine.ext import ndb


class Todo(ndb.Model):
    """Todo item model.

    An Entity of kind Todo contains 3 properties:

    - a `text` string property: limited to 500 characters that default
      to empty string and is not indexed.
      - a `done` boolean property: that default to False and is indexed.
    - a `created` date time property: that default to the current time
    at the time of the creation of the entity and is indexed.
    """

    title = ndb.StringProperty(default='', indexed=False)
    completed = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_todo_object(cls, name, id):
        todolist = TodoList.get_or_insert(name)
        return Todo.get_by_id(id, parent=todolist.key)

    def get_todo(self):
        return {
                   "id": self.key.id(),
                   "title": self.title,
                   "completed": self.completed
               }

    def update_todo(self, id, text, completed):
        todo = Todo(id=id, title=text, completed=completed, parent=self.key)
        todo.put()
        return {
                   "id": todo.key.id(),
                   "title": todo.title,
                   "completed": todo.completed
               }

    def delete_todo(self):
        deleted_id = self.key.id()
        self.delete()
        return deleted_id

class TodoList(ndb.Model):
    """Todo list model.

    An Entity of kind TodoList contains no property and is used as the
    parent of Todo entity to define an entity group: a group of Todo
    entity with a common ancestor.

    It enable consistent queries and transactional update of a group
    of Todo entities.
    """

    @classmethod
    def get_or_create(cls, name):
        """Get or create a new Todo list.

        Use the `get_or_insert()` method to transactionaly lookup an
        entity by key or send an insert mutation to the datastore if
        the no matching entity is found:
        the entity key will be set to `ndb.Key('TodoList', name)` and
        the system will not auto allocate an id.
        """
        return TodoList.get_or_insert(name)

    def add_todo(self, text):
        """Create a new Todo entity in the Todo list.

        Construct a new Todo model with the `text` property set to the
        given `text` string, and its parent set to the current
        todo list.

        Use the `put()` method to send a mutation to the datastore
        service to transactionaly insert the new entity: a numeric
        id is auto-allocated by the service for the new entity.

        Because the all Todos of a given TodoList list belong to the
        same entity group, there is a limited number of transactional
        insert that can be sent per second.
        """

        todo = Todo(title=text, parent=self.key)
        todo.put()
        return {
                   "id": todo.key.id(),
                   "title": todo.title,
                   "completed": todo.completed
               }

    def update_todo(self, id, text, completed):
        """Update an existing Todo entity in the Todo list.

        Construct a new Todo model with the id set to the given
        `todo_id` numeric id and the `text` and `done` property set to
        the given args; the parent set to the current todo list.

        Use the `put()` method to send a mutation to the datastore
        service that transactionaly update the existing entity.

        Because the all Todos of a given TodoList list belong to the
        same entity group, there is a limited number of transactional
        insert that can be sent per second.
        """

        todo = Todo(id=id, title=text, completed=completed, parent=self.key)
        todo.put()
        return {
                   "id": todo.key.id(),
                   "title": todo.title,
                   "completed": todo.completed
               }

    def get_all_todos(self):
        """Query for all Todo items of the Todo list ordered by creation date.

        Because the query has an ancestor filter that scope the query
        to the entity group containing all the Todos of the TodoList,
        it returns strongly consistent result.
        """
        all_todos = []
        for todo in Todo.query(ancestor=self.key).fetch():
            all_todos.append(
                {
                    "id": todo.key.id(),
                    "title": todo.title,
                    "completed": todo.completed
                }
            )
        return all_todos

    @ndb.transactional
    def archive_todos(self):
        """Delete all Todo items that are done.

        `ndb.transactional` decorator creates a new transaction at the
        beginning of the method and commit the transaction at the end.

        Within this transaction, the method perform two operations:
        - Query for all the Todo entities with a `done` property set
          to `True` and returns only the keys.
        - Batch delete all the entities associated with those keys.

        Because those two operations are performed within a
        transaction, it is guaranteed that:
        - all read operations (including query) gets a strongly
          consistent view of the TodoList entity group at the
          beginning of the transaction.
        - all write operations succeeds if there is no current update
          to the same TodoList entity group.
        """

        keys = Todo.query(Todo.completed == True,
                          ancestor=self.key).fetch(keys_only=True)
        ndb.delete_multi(keys)
