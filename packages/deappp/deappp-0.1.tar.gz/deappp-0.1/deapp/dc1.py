print("""

      
# DC code 1 server.py
      
from xmlrpc.server import SimpleXMLRPCServer
import threading

def factorial(n):
    if not isinstance(n, int) or n < 0:
        return "Error: Input must be a non-negative integer."
    result = 1
    for i in range(2, n + 1):
        result *= i
    return str(result)  # Return as string to avoid OverflowError

def shutdown():
    print("Shutting down the server...")
    threading.Thread(target=server.shutdown).start()
    return "Server is shutting down."

server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
print("Server is listening on port 8000...")
server.register_function(factorial, "factorial")
server.register_function(shutdown, "shutdown")
server.serve_forever()

      

# DC code 1 client.py
      

import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
while True:
    user_input = input("Enter a number to compute its factorial (or type 'exit' to quit): ").strip()
    if user_input.lower() == 'exit':
        try:
            print(proxy.shutdown())
        except:
            print("Server already shut down or unreachable.")
        break
    try:
        num = int(user_input)
        result = proxy.factorial(num)
        print(f"Factorial of {num} is:\n{result}")
    except ValueError:
        print("Please enter a valid integer or 'exit'.")



""")