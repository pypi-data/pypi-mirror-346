print('''
# server.py
import Pyro5.api

@Pyro5.api.expose
class StringService:
    def concatenate(self, s1, s2):
        print(f"Received: {s1} + {s2}")
        return s1 + s2

def main():
    daemon = Pyro5.api.Daemon()
    uri = daemon.register(StringService)
    print("Server is ready. Object URI =", uri)
    daemon.requestLoop()

if __name__ == "__main__":
    main()

    

import Pyro5.api

# Use the URI printed by the server
uri = "PYRO:obj_9a05ab7def274c7283e001f384f7ab5b@localhost:64098"
string_service = Pyro5.api.Proxy(uri)  # Connect to remote object

# Send strings to server
s1 = input("Enter first string: ")
s2 = input("Enter second string: ")

# Call the remote method to concatenate the strings
result = string_service.concatenate(s1, s2)

# Output the concatenated result
print("Concatenated result from server:", result) 
#for output run this client code in diferent file and copy the the serever code in uri and run it
      ''')
