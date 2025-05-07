print('''
from xmlrpc.server import SimpleXMLRPCServer
import threading
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def shutdown():
    print("Shutting down the server...")
    threading.Thread(target=server.shutdown).start()
    return "Server is shutting down."

def run_server():
    global server
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True, logRequests=False)
    print("Server is listening on port 8000...")
    server.register_function(factorial, "factorial")
    server.register_function(shutdown, "shutdown")
    server.serve_forever()

# Start the server in a daemon thread
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()








import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

while True:
    user_input = input("Enter a number to compute its factorial (or type 'exit' to quit): ").strip()

    if user_input.lower() == 'exit':
        try:
            print(proxy.shutdown())
        except:
            print("Server already shut down.")
        break

    try:
        num = int(user_input)
        result = proxy.factorial(num)
        print(f"Factorial of {num} is {result}")
    except ValueError:
        print("Please enter a valid integer or 'exit'.")

      ''')
