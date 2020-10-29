# python3
"""
we determine all strongly connected components using the Kosaraju algorithm.
If a variable xn is in the same component as ¬xn, then no solutions exist and the algorithm terminates.
"""
import sys
import threading

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size
clock = 1


def DFS_2(i, graph, visited, post):
    global clock
    visited[i] = True
    for v in graph[i]:
        if not visited[v]:
            DFS_2(v, graph, visited, post)
    post[i] = clock
    clock += 1


def DFS(n, graph):
    global clock
    visited = [False] * (2 * n + 1)
    post = [0] * (2 * n + 1)
    for v in range(1, 2 * n + 1):
        if not visited[v]:
            DFS_2(v, graph, visited, post)
    post = list(enumerate(post[1:], start=1))
    post.sort(key=lambda x: x[1], reverse=True)
    post_vertex = []
    for v, order in post:
        post_vertex.append(v)
    return post_vertex


def add_vertices_to_scc(i, graph, visited, scc, scc_number, u):
    visited[i] = True
    scc.append(i)
    scc_number[i] = u
    for v in graph[i]:
        if not visited[v]:
            add_vertices_to_scc(v, graph, visited, scc, scc_number, u)


def find_strongly_connected_components(n, rev_graph, graph):
    finishing_times = DFS(n, rev_graph)
    visited = [False] * (2 * n + 1)
    sccs = []
    scc_number = [0] * (2 * n + 1)
    u = 1
    for i in finishing_times:
        if not visited[i]:
            scc = []
            add_vertices_to_scc(i, graph, visited, scc, scc_number, u)
            sccs.append(scc)
            u += 1
    return sccs, scc_number


def two_SAT(n, rev_graph, graph):
    sccs, scc_number = find_strongly_connected_components(n, rev_graph, graph)
    # check if there is any variable with its negative literal in the same scc
    for i in range(1, n + 1):
        if scc_number[i] == scc_number[i + n]:
            return False
    solution = [[] for _ in range(2 * n + 1)]
    assigned = [False] * (2 * n + 1)
    for scc in sccs:
        for v in scc:
            if not assigned[v]:
                assigned[v] = True
                solution[v] = 1
                if v > n:
                    solution[v - n] = 0
                    assigned[v - n] = True
                else:
                    solution[v + n] = 0
                    assigned[v + n] = True
    return solution

def main():
    n, m = map(int, input().split())
    graph = [[] for _ in range(2 * n + 1)]
    rev_graph = [[] for _ in range(2 * n + 1)]
    for _ in range(m):
        a, b = map(int, input().split())
        if a > 0 and b > 0:
            graph[a + n].append(b)
            graph[b + n].append(a)
            rev_graph[b].append(a + n)
            rev_graph[a].append(b + n)
        elif a < 0 and b < 0:
            graph[-a].append(-b + n)
            graph[-b].append(-a + n)
            rev_graph[-b + n].append(-a)
            rev_graph[-a + n].append(-b)
        elif a < 0 and b > 0:
            graph[-a].append(b)
            graph[b + n].append(-a + n)
            rev_graph[b].append(-a)
            rev_graph[-a + n].append(b + n)
        elif a > 0 and b < 0:
            graph[a + n].append(-b + n)
            graph[-b].append(a)
            rev_graph[-b + n].append(a + n)
            rev_graph[a].append(-b)
    result = two_SAT(n, rev_graph, graph)
    if not result:
        print('UNSATISFIABLE')
    else:
        print('SATISFIABLE')
        for i in range(1, n + 1):
            if result[i] > 0:
                print(i, end=' ')
            else:
                print(-i, end=' ')


# This is to avoid stack overflow issues
threading.Thread(target=main).start()
