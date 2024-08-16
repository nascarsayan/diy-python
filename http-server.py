# create an http server with PUT, PATCH, DELETE, GET, POST methods on TODO list

todos = [
  { "id": 1, "name": "buy groceries", "done": False },
  { "id": 2, "name": "cook dinner", "done": False }
]

def get_todo(id):
  for todo in todos:
    if todo["id"] == id:
      return todo
  return None

def create_todo(todo):
  todo["id"] = len(todos) + 1
  todos.append(todo)
  return todo

def update_todo(id, todo):
  for i in range(len(todos)):
    if todos[i]["id"] == id:
      todos[i] = todo
      return todo
  return None

def delete_todo(id):
  for i in range(len(todos)):
    if todos[i]["id"] == id:
      return todos.pop(i)
  return None

import json

from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path == '/todos':
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      self.wfile.write(json.dumps(todos).encode())
    elif self.path.startswith('/todos/'):
      todo_id = int(self.path.split('/')[-1])
      todo = get_todo(todo_id)
      if todo:
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(todo).encode())
      else:
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Todo not found')
    else:
      self.send_response(404)
      self.send_header('Content-type', 'text/plain')
      self.end_headers()
      self.wfile.write(b'Invalid path')

  def do_POST(self):
    if self.path == '/todos':
      content_length = int(self.headers['Content-Length'])
      post_data = self.rfile.read(content_length)
      new_todo = json.loads(post_data)
      created_todo = create_todo(new_todo)
      if created_todo:
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(created_todo).encode())
      else:
        self.send_response(500)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Failed to create todo')
    else:
      self.send_response(404)
      self.send_header('Content-type', 'text/plain')
      self.end_headers()
      self.wfile.write(b'Invalid path')

  def do_PUT(self):
    if self.path.startswith('/todos/'):
      todo_id = int(self.path.split('/')[-1])
      content_length = int(self.headers['Content-Length'])
      put_data = self.rfile.read(content_length)
      updated_todo = json.loads(put_data)
      updated_todo["id"] = todo_id
      result = update_todo(todo_id, updated_todo)
      if result:
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
      else:
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Todo not found')
    else:
      self.send_response(404)
      self.send_header('Content-type', 'text/plain')
      self.end_headers()
      self.wfile.write(b'Invalid path')

  def do_PATCH(self):
    if self.path.startswith('/todos/'):
      todo_id = int(self.path.split('/')[-1])
      content_length = int(self.headers['Content-Length'])
      patch_data = self.rfile.read(content_length)
      updated_fields = json.loads(patch_data)
      todo = get_todo(todo_id)
      if todo:
        for key, value in updated_fields.items():
          todo[key] = value
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(todo).encode())
      else:
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Todo not found')
    else:
      self.send_response(404)
      self.send_header('Content-type', 'text/plain')
      self.end_headers()
      self.wfile.write(b'Invalid path')

  def do_DELETE(self):
    if self.path.startswith('/todos/'):
      todo_id = int(self.path.split('/')[-1])
      result = delete_todo(todo_id)
      if result:
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
      else:
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Todo not found')
    else:
      self.send_response(404)
      self.send_header('Content-type', 'text/plain')
      self.end_headers()
      self.wfile.write(b'Invalid path')

def run(server_class=HTTPServer, handler_class=RequestHandler):
  server_address = ('', 8000)
  httpd = server_class(server_address, handler_class)
  httpd.serve_forever()

run()
