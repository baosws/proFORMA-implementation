import queue

# return iff a augmenting path is found
def bfs(adj, Fx, Fy, matchX, matchY):
    n = len(adj)
    q = queue.Queue()
    for u in range(n):
        if matchX[u] == 0:
            q.put(u)

    pre = [-1] * n
    while not q.empty():
        u = q.get()
        for v, w in adj[u]:
            if pre[v] == -1 and w - Fx[u] - Fy[v] == 0:
                pre[v] = u
                if matchY[v] == -1:
                    return v
                else:
                    q.put(matchY[v])
    
    return -1

def rematch(src, matchX, matchY, pre):
    v, u = src, pre[v]
    while u != -1:
        old_matchX = matchX[u]
        matchX[u], matchY[v] = v, u
        v, u = old_matchX, pre[v]

def update(src, adj, Fx, Fy, pre):
    n = len(adj)
    visitedX = [False] * n
    visitedY = [False] * n
    visitedX[src] = True
    for v in range(n):
        if pre[v] != -1:
            visitedY[v] = visitedX[matchY[v]] = True

    delta = INF
    for u in range(n):
        if visitedX[u]:
            for v, w in adj[u]:
                if not visitedY[v]:
                    delta = min(delta, w - Fx[u] - Fy[v])

        for u in range(n):
            if visitedX[u]:
                Fx[u] -= delta
        for v in range(n):
            if visitedY[v]:
                Fy[v] += delta

def hungarian_match(adj):
    n = len(graph)
    Fx = [0] * n
    Fy = [0] * n
    matchX = [-1] * n
    matchY = [-1] * n
    pre = [-1] * n
    for i in range(n):
        while True:
            u = bfs(adj, Fx, Fy, matchX, matchY, pre)
            if u == -1:
                update(i, adj, Fx, Fy, pre)
            else:
                rematch(u, matchX, matchY, pre)
                break
