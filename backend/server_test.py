from flask import Flask, request

app = Flask(__name__)

class Server:
    def print(self, message):
        print(f"Received message: {message}")

server_instance = Server()

@app.route('/print', methods=['POST'])
def print_message():
    data = request.json
    message = data.get('message')
    server_instance.print(message)
    return {"status": "Message printed"}

if __name__ == '__main__':
    app.run(debug=True, port=5001)
