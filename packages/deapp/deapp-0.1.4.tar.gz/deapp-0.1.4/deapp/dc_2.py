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


 ---------------------- java -----------------------------------

# mkdir service
# cd service

# nano ConcatService.java


# service code

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ConcatService extends Remote {
    String concatenate(String str1, String str2) throws RemoteException;
}



# nano ConcatServer.java

# server code

import java.rmi.Naming;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class ConcatServer extends UnicastRemoteObject implements ConcatService {

    protected ConcatServer() throws RemoteException {
        super();
    }

    @Override
    public String concatenate(String str1, String str2) throws RemoteException {
        return str1 + str2;
    }

    public static void main(String[] args) {
        try {
            ConcatServer server = new ConcatServer();
            Naming.rebind("rmi://localhost/ConcatService", server);
            System.out.println("Server is running...");
        } catch (Exception e) {
            System.err.println("Server exception: " + e.getMessage());
            e.printStackTrace();
        }
    }
}


# nano ConcatClient.java

# client code

import java.rmi.Naming;
import java.util.Scanner;

public class ConcatClient {
    public static void main(String[] args) {
        try {
            ConcatService service = (ConcatService) Naming.lookup("rmi://localhost/ConcatService");
            Scanner scanner = new Scanner(System.in);

            while (true) {
                System.out.println("Menu:");
                System.out.println("1. Concatenate Strings");
                System.out.println("2. Exit");
                System.out.print("Enter choice: ");
                int choice = scanner.nextInt();
                scanner.nextLine(); // Consume newline

                if (choice == 1) {
                    System.out.print("Enter first string: ");
                    String str1 = scanner.nextLine();
                    System.out.print("Enter second string: ");
                    String str2 = scanner.nextLine();
                    String result = service.concatenate(str1, str2);
                    System.out.println("Concatenated Result: " + result);
                } else if (choice == 2) {
                    System.out.println("Exiting...");
                    break;
                } else {
                    System.out.println("Invalid choice. Please try again.");
                }
            }

            scanner.close();
        } catch (Exception e) {
            System.err.println("Client exception: " + e.getMessage());
            e.printStackTrace();
        }
    }
}

# commands
# javac ConcatService.java ConcatServer.java ConcatClient.java

# rmiregistry &

# open new terminal then
# java ConcatServer

# open new terminal then
# java ConcatClient




""")
