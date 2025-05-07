print("""

# server.py

import Pyro5.api

@Pyro5.api.expose
class StringService:
    def concatenate(self, s1, s2):
        return s1 + s2

def main():
    daemon = Pyro5.api.Daemon()                      # Create a Pyro server
    uri = daemon.register(StringService)             # Register the class
    print("Server is ready. Object URI =", uri)      # Print URI for client use
    daemon.requestLoop()                             # Start event loop

if __name__ == "__main__":                            # Corrected this line
    main()




# client.py

import Pyro5.api

# Use the URI printed by the server
uri = input("Enter the server URI (e.g., PYRO:obj_...@localhost:port): ")
string_service = Pyro5.api.Proxy(uri)  # Connect to remote object

# Send strings to server
s1 = input("Enter first string: ")
s2 = input("Enter second string: ")

result = string_service.concatenate(s1, s2)
print("Concatenated result from server:", result)



""")
