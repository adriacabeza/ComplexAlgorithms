# python3
import queue

class Edge:

	def __init__(self, u, v, capacity):
		self.u = u
		self.v = v
		self.capacity = capacity
		self.flow = 0


class FlowGraph:
	def __init__(self, n, flights):
		# List of all - forward and backward - edges
		self.edges = []
		# These adjacency lists store only indices of edges in the edges list
		self.graph = [[] for _ in range(n)]
		self.flights = flights

	def add_edge(self, from_, to, capacity):
		# Note that we first append a forward edge and then a backward edge,
		# so all forward edges are stored at even indices (starting from 0),
		# whereas backward edges are stored at odd indices.
		forward_edge = Edge(from_, to, capacity)
		backward_edge = Edge(to, from_, 0)
		self.graph[from_].append(len(self.edges))
		self.edges.append(forward_edge)
		self.graph[to].append(len(self.edges))
		self.edges.append(backward_edge)

	def size(self):
		return len(self.graph)

	def get_ids(self, from_):
		return self.graph[from_]

	def get_edge(self, id):
		return self.edges[id]

	def add_flow(self, id, flow):
		# To get a backward edge for a true forward edge (i.e id is even), we should get id + 1
		# due to the described above scheme. On the other hand, when we have to get a "backward"
		# edge for a backward edge (i.e. get a forward edge for backward - id is odd), id - 1
		# should be taken.
		#
		# It turns out that id ^ 1 works for both cases. Think this through!
		self.edges[id].flow += flow
		self.edges[id ^ 1].flow -= flow
		self.edges[id].capacity -= flow
		self.edges[id ^ 1].capacity += flow


	def max_flow(self, src, dst):
		flow = 0
		while True:
			has_path, path, flow_to_add = self.bfs(src, dst)
			if not has_path:
				return flow
			for id in path:
				self.add_flow(id, flow_to_add)
			flow += flow_to_add
		return flow

	def bfs(self, src, dst):
		flow = float('inf')
		has_path = False
		n = self.size()
		dist = [float('inf')] * n
		path = []
		parent = [(None, None)] * n
		q = queue.Queue()
		dist[src] = 0
		q.put(src)
		while not q.empty():
			current = q.get()
			for id in self.get_ids(current):
				current_edge = self.get_edge(id)
				if dist[current_edge.v] == float('inf') and current_edge.capacity > 0:
					dist[current_edge.v] = dist[current] + 1
					parent[current_edge.v] = (current, id)
					q.put(current_edge.v)
					if current_edge.v == dst:
						while True:
							path.insert(0, id)
							flow = min(self.get_edge(id).capacity, flow)
							if current == src:
								break
							current, id = parent[current]
						has_path = True
						return has_path, path, flow
		return has_path, path, flow

	def print_solution(self):
		jobs = list()
		for i in range(self.flights):
			job = -1
			for id in self.get_ids(i+1):
				edge = self.get_edge(id)
				if edge.flow == 1:
					job = edge.v - self.flights
					break
			jobs.append(job)
		print(*jobs)


def read_data():
	flights, crew = map(int, input().split())
	flow_graph = FlowGraph(flights+crew+2, flights)


	# edges on the left bipartite graph to right
	for flight in range(1, flights+1):
		# source node to flights
		flow_graph.add_edge(0, flight, 1)

		people = list(map(int, input().split()))
		for num, bit in enumerate(people):
			if bit:
				flow_graph.add_edge(flight, flights+num+1, 1)

	# add sink node
	last = flow_graph.size() -1
	for i in range(flights+1, flights+crew+1):
		flow_graph.add_edge(i, last, 1)


	return flow_graph



if __name__ == '__main__':
	flow_graph = read_data()
	flow_graph.max_flow(0, flow_graph.size()-1)
	flow_graph.print_solution()
