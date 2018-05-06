import queue
INF = 10 ** 9

def bfs(cost_mat, fx, fy, matchX, matchY, pre):
    n = len(cost_mat)
    q = queue.Queue()
    for u in range(n):
        if matchX[u] == -1:
            q.put(u)

    for i in range(n):
        pre[i] = -1
    while not q.empty():
        u = q.get()
        for v, w in zip(range(n), cost_mat[u]):
            if pre[v] == -1 and w - fx[u] - fy[v] == 0:
                pre[v] = u
                if matchY[v] == -1:
                    return v
                else:
                    q.put(matchY[v])
    
    return -1

def enlarge(src, matchX, matchY, pre):
    v = src
    while v != -1:
        u = pre[v]
        old_matchX = matchX[u]
        matchX[u], matchY[v] = v, u
        v = old_matchX

def update(src, cost_mat, fx, fy, matchY, pre):
    n = len(cost_mat)
    visitedX = [False] * n
    visitedY = [False] * n
    visitedX[src] = True
    for v in range(n):
        if pre[v] != -1:
            visitedY[v] = visitedX[matchY[v]] = True

    delta = INF
    for u in range(n):
        if visitedX[u]:
            for v, w in zip(range(n), cost_mat[u]):
                if not visitedY[v]:
                    delta = min(delta, w - fx[u] - fy[v])

    for u in range(n):
        if visitedX[u]:
            fx[u] += delta
    for v in range(n):
        if visitedY[v]:
            fy[v] -= delta

def hungarian_match(cost_mat):
    n = len(cost_mat)
    fx = [0] * n
    fy = [0] * n
    matchX = [-1] * n
    matchY = [-1] * n
    pre = [-1] * n
    for i in range(n):
        while True:
            u = bfs(cost_mat, fx, fy, matchX, matchY, pre)
            if u == -1:
                update(i, cost_mat, fx, fy, matchY, pre)
            else:
                enlarge(u, matchX, matchY, pre)
                break
    cost = 0
    for i in range(n):
        cost += fx[i] + fy[i]

    return matchX, matchY
