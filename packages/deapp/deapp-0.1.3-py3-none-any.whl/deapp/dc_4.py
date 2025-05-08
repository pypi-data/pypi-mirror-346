
print("""
import time
import random

# Round Robin Load Balancing Algorithm
class RoundRobin:
    def __init__(self, servers):
        self.servers = servers
        self.current_index = -1

    def get_next_server(self):
        self.current_index = (self.current_index + 1) % len(self.servers)
        return self.servers[self.current_index]


# Weighted Round Robin Load Balancing Algorithm
class WeightedRoundRobin:
    def __init__(self, servers, weights):
        self.servers = servers
        self.weights = weights
        self.current_index = -1
        self.current_weight = 0

    def get_next_server(self):
        while True:
            self.current_index = (self.current_index + 1) % len(self.servers)
            if self.current_index == 0:
                self.current_weight -= 1
            if self.current_weight <= 0:
                self.current_weight = max(self.weights)
            if self.weights[self.current_index] >= self.current_weight:
                return self.servers[self.current_index]


# Least Connections Load Balancing Algorithm
class LeastConnections:
    def __init__(self, servers):
        self.servers = {server: 0 for server in servers}

    def get_next_server(self):
        # Find the minimum number of connections
        min_connections = min(self.servers.values())
        # Get all servers with the minimum number of connections
        least_loaded_servers = [server for server, connections in
                                self.servers.items() if connections == min_connections]
        # Select a random server from the least loaded servers
        selected_server = random.choice(least_loaded_servers)
        self.servers[selected_server] += 1
        return selected_server

    def release_connection(self, server):
        if self.servers[server] > 0:
            self.servers[server] -= 1


# Least Response Time Load Balancing Algorithm
class LeastResponseTime:
    def __init__(self, servers):
        self.servers = servers
        self.response_times = [0] * len(servers)

    def get_next_server(self):
        min_response_time = min(self.response_times)
        min_index = self.response_times.index(min_response_time)
        return self.servers[min_index]

    def update_response_time(self, server, response_time):
        index = self.servers.index(server)
        self.response_times[index] = response_time


# Simulate random response time
def simulate_response_time():
    # Simulating response time with random delay
    delay = random.uniform(0.1, 1.0)
    time.sleep(delay)
    return delay


# Demonstration function to show the algorithms
def demonstrate_algorithm(algorithm_name, load_balancer, iterations=6, use_response_time=False, use_connections=False):
    print(f"\\n---- {algorithm_name} ----")
    for i in range(iterations):
        server = load_balancer.get_next_server()
        print(f"Request {i + 1} -> {server}")
        if use_response_time:
            response_time = simulate_response_time()
            load_balancer.update_response_time(server, response_time)
            print(f"Response Time: {response_time:.2f}s")
        if use_connections:
            load_balancer.release_connection(server)


if __name__ == "__main__":
    servers = ["Server1", "Server2", "Server3"]

    # Round Robin
    rr = RoundRobin(servers)
    demonstrate_algorithm("Round Robin", rr)

    # Weighted Round Robin
    weights = [5, 1, 1]
    wrr = WeightedRoundRobin(servers, weights)
    demonstrate_algorithm("Weighted Round Robin", wrr, iterations=7)

    # Least Connections
    lc = LeastConnections(servers)
    demonstrate_algorithm("Least Connections", lc, use_connections=True)

    # Least Response Time
    lrt = LeastResponseTime(servers)
    demonstrate_algorithm("Least Response Time", lrt, use_response_time=True)


---------------------------- method 2 ----------------------------------


import itertools

servers = ["S1", "S2", "S3"]

# Round Robin
def round_robin(servers, requests):
    print("\\n--- Round Robin ---")
    rr = itertools.cycle(servers)
    for i in range(requests):
        print(f"Request {i+1} -> {next(rr)}")

# Weighted Round Robin
def weighted_round_robin(servers, weights, requests):
    print("\\n--- Weighted Round Robin ---")
    weighted_servers = [s for s, w in zip(servers, weights) for _ in range(w)]
    wrr = itertools.cycle(weighted_servers)
    for i in range(requests):
        print(f"Request {i+1} -> {next(wrr)}")


# Least Connections
def least_connections(servers, requests):
    print("\\n--- Least Connections ---")

    connections = {server: 0 for server in servers}

    for i in range(requests):
        least_loaded = min(connections, key=connections.get)

        print(f"Request {i+1} -> {least_loaded}")

        connections[least_loaded] += 1


    print("\\nFinal connection count per server:")
    for server, count in connections.items():
        print(f"{server}: {count}")

least_connections(["S1", "S2", "S3"], 10)


round_robin(servers, 6)
weighted_round_robin(servers, [3, 1, 2], 10)




""")
