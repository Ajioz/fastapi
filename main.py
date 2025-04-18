from typing import Union, List, Optional
from enum import IntEnum
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException

api = FastAPI()


class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1



class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=512, description="The name of the todo item")
    todo_description: str = Field(..., description="The description of the todo item")
    priority: Priority = Field(default=Priority.LOW, description="The priority of the todo item")
    todo_name: str = Field(..., min_length=3, max_length=512, description="The name of the todo item")
    todo_description: str = Field(..., description="The description of the todo item")
    priority: Priority = Field(default=Priority.LOW, description="The priority of the todo item")


class TodoCreate(TodoBase):
    pass 

class TodoUpdate(TodoBase):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512, description="The name of the todo item")
    todo_description: Optional[str] = Field(None, description="The description of the todo item")
    priority: Optional[Priority] = Field(None, description="The priority of the todo item")


class Todo(TodoBase):
    todo_id:int= Field(..., description='Unique identifier of th todo')


all_todos = [
    Todo(todo_id=1, todo_name="Clean house", todo_description="Cleaning the house thoroughly", priority=Priority.HIGH),
    Todo(todo_id=2, todo_name="Sports", todo_description="Going to the gym for workout", priority=Priority.MEDIUM),
    Todo(todo_id=3, todo_name="Read", todo_description="Read chapter 5 of the book", priority=Priority.LOW),
    Todo(todo_id=4, todo_name="Work", todo_description="Complete project documentation", priority=Priority.MEDIUM),
    Todo(todo_id=5, todo_name="Study", todo_description="Prepare for upcoming exam", priority=Priority.LOW)
]



# This is a path operation function
@api.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")



# this is a query parameter approach
@api.get("/todos", response_model=List[Todo])
def get_todos(first_n:int=None):
    if first_n:
        return all_todos[:first_n]
    return all_todos



# This is a regualr path operation function
@api.get("/todos")
def read_todos():
    return all_todos


@api.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@api.post("/items", response_model=Todo)
def create_item(item: TodoCreate):
    new_item_id = max(item['todo_id'] for item in all_todos) + 1
    new_todo = Todo(todo_id= new_item_id,
                    todo_name= item.todo_name,
                    todo_description= item.todo_description, 
                    priority=item.priority)    
    all_todos.append(new_todo)
    return new_todo


# for uodating the items
# we are using the PUT method to update the item
@api.put("/items/{item_id}", response_model=Todo)
def update_item(item_id: int, item: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == item_id:
            if update_item.todo_name:
                todo.todo_name = update_item.todo_name
            if update_item.todo_description:
                todo.todo_description = update_item.todo_description
            if update_item.priority:
                todo.priority = update_item.priority
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


# for deleting the items
# we are using the DELETE method to delete the item
@api.delete("/items/{item_id}")
def delete_item(item_id: int):
    for todo in all_todos:
        if todo.todo_id == item_id:
            all_todos.remove(todo)
            return delete_item
    raise HTTPException(status_code=404, detail="Todo not found")


'''
# for deleting the items --> Altenative approach
@api.delete("/items/{item_id}")
def delete_item2(item_id: int):
    for index, todo in enumerate(all_todos):
        if todo['todo_id'] == item_id:
            del all_todos[index]
            return {"message": "Todo deleted"}      
    return {"error": "Todo not found"}
'''