#uses python3

import sys
import threading

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size


class Vertex:
    def __init__(self, weight):
        self.weight = weight
        self.children = []


def ReadTree():
    size = int(input()) # number of people
    tree = [Vertex(w) for w in map(int, input().split())] # each vertex contains how funny is and its subordinates
    for i in range(1, size):
        a, b = list(map(int, input().split()))
        tree[a - 1].children.append(b - 1)
        tree[b - 1].children.append(a - 1)
    return tree


def dfs(tree, vertex, parent, sum):
    if sum[vertex] == -1:
        if not tree[vertex].children: # if it does not have children
            sum[vertex] = tree[vertex].weight
        else:
            weight = tree[vertex].weight # we check the option of taking the father and its grandchildren omitting the children
            for child in tree[vertex].children:
                if child != parent:
                    for child2 in tree[child].children:
                        if child2 != vertex:
                            weight += dfs(tree, child2, child, sum)
            weight1 = 0 # we check the option of omitting the parent and starting from the children
            for child in tree[vertex].children:
                if child != parent:
                    weight1 += dfs(tree, child, vertex, sum)
            sum[vertex] = max(weight, weight1) # we set the vertex as the best option

    return sum[vertex]


def MaxWeightIndependentTreeSubset(tree):
    size = len(tree)
    if size == 0:
        return 0
    s = [-1] * size
    return dfs(tree, 0, -1, s)



def main():
    tree = ReadTree()
    weight = MaxWeightIndependentTreeSubset(tree)
    print(weight)


# This is to avoid stack overflow issues
threading.Thread(target=main).start()
