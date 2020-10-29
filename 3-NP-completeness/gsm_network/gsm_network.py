# python3
n, m = map(int, input().split())
edges = [list(map(int, input().split())) for i in range(m)]
C = 3 * len(edges) + n # we have to check for every edge for every color the consistency  + every vertex one color
V = n * 3 # each vertex has three possible colors
cnt = 1
print("{} {}".format(C, V))

# this one represents that every vertex has at least one color
for i in range(1, n+1):
    print("{} {} {} 0".format(cnt, cnt+1, cnt+2))
    cnt += 3

# this one represents that if we assign a color to one, we cannot have a neighbour with the same color
for edge in edges:
    print("{} {} 0".format(-((edge[0] - 1) * 3 + 1), -((edge[1] - 1) * 3 + 1)))
    print("{} {} 0".format(-((edge[0] - 1) * 3 + 2), -((edge[1] - 1) * 3 + 2)))
    print("{} {} 0".format(-((edge[0] - 1) * 3 + 3), -((edge[1] - 1) * 3 + 3)))

