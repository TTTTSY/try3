from flask import Flask, render_template, request
import google.generativeai as palm

# Configure API key from environment variable
palm.configure(api_key="AIzaSyCga2U1iWz65_J-q3UilS38wmrN8CdaEr4")
model = {"model": "models/chat-bison-001"}

app = Flask(__name__)

class Node:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.next = None

class Queue:
    def __init__(self):
        self.head = None

    def enqueue(self, username: str, password: str):
        new_node = Node(username, password)
        if self.head is None:
            self.head = new_node
        else:
            new_node.next = self.head
            self.head = new_node

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    queue = Queue()
    queue.enqueue("TaoSiyu", "Systemcall0122")
    queue.enqueue("T1", "Systemcall01")
    queue.enqueue("T2", "Systemcall0")
    queue.enqueue("T3", "Systemcall")

    r = request.form.get("q")
    v = request.form.get("t")

    if r is None or v is None:
        return render_template("index.html")

    current = queue.head
    found = 0
    while current:
        if current.username == r and current.password == v:
            found = 1
            break
        current = current.next

    if found == 1:
        return render_template("main.html", r=r)
    else:
        return render_template("index.html")

@app.route("/genAI", methods=["GET", "POST"])
def genAI():
    q = request.form.get("q")
    r = palm.chat(**model, messages=q)
    return render_template("genAI.html", r=r.last)

@app.route("/DApp", methods=["GET", "POST"])
def DApp():
    return render_template("DApp.html")

if __name__ == "__main__":
    app.run()
