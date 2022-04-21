import networkx as nx
import copy
import itertools

G = nx.DiGraph()

G.add_edges_from(
    [
        (1, 2),
        (2, 3),
        (4, 5),
        (5, 3),
        (4, 6),
        (6, 7),
        (8, 9),
        (9, 10),
        (10, 7),
        (9, 11),
        (11, 12),
        (11, 17),
        (13, 14),
        (14, 16),
        (15, 16),
        (16, 17),
    ]
)


def checkEdge(G, S, T):

    if type(S) == type(1) and type(T) == type(1):
        if G.has_edge(S, T):
            return True

    elif type(S) == type(1):
        for i in T:
            if G.has_edge(S, i):
                return True

    elif type(T) == type(1):
        for i in S:
            if G.has_edge(i, T):
                return True

    else:
        for i in S:
            for j in T:
                if G.has_edge(i, j):
                    return True

    return False


def findMinCut(G, S, T):
    # Returns a list of MinCut
    pass


def checkMinCut(G, S, T):

    temp = []

    if type(S) == type(1) and type(T) == type(1):
        temp = temp.extend(list(nx.minimum_node_cut(G, S, T)))

    elif type(S) == type(1):
        for i in T:
            temp = temp.extend(list(nx.minimum_node_cut(G, S, i)))

    elif type(T) == type(1):
        for i in S:
            temp = temp.extend(list(nx.minimum_node_cut(G, i, T)))

    else:
        for i in S:
            for j in T:
                temp = temp.extend(list(nx.minimum_node_cut(G, i, j)))

    return temp


def checkForW(G, allS, allT):

    Sall = [j for sub in allS for j in sub]
    Tall = [j for sub in allT for j in sub]

    NT = (set(G.nodes) - set(Sall)) - set(Tall)

    for i in NT:
        if checkEdge(G, allS[-1], i) and checkEdge(G, i, Tall):
            return i

    return -1


def getExtendedVertex(G, allS, allT):

    Sall = [j for sub in allS for j in sub]
    Tall = [j for sub in allT for j in sub]

    NT = list((set(G.nodes) - set(Sall)) - set(Tall))

    for i in NT:
        if checkEdge(G, allS[-1], i) == True and checkEdge(G, i, Tall) == False:
            return i

    return -1


def checkFVS(G, X):

    for i in X:
        G.remove_node(i)

    return nx.simple_cycles(G)


def SMC(G, S, T, k):

    Gcpy = copy.deepcopy(G)

    if len(S) == 1:
        # print("Use the MinCut Algorithm for O(kn^2) solution.\n")
        return findMinCut(G, S, T)

    Sl = S[-1]
    Tall = [j for sub in T for j in sub]

    R2 = checkEdge(G, Sl, Tall)

    if R2 or k < 0:
        return -1

    R1 = findMinCut(G, Sl, Tall)

    if len(R1) == 0:
        return SMC(G, S[:-1], T[:-1], k)

    R3 = checkForW(G, S, T)

    if R3 != -1:
        G.remove_node(R3)
        temp = [R3]
        temp.extend(SMC(G, S, T, k - 1))
        return temp

    u = getExtendedVertex(G, S, T)

    if u == -1:
        print("Cannot find extended vertex !!")
        return -1

    minL = findMinCut(G, Sl, Tall)

    if len(minL) > k:
        return -1

    SlD = Sl.copy()
    SlD.extend([u])

    minLD = findMinCut(G, SlD, Tall)

    if len(minL) == len(minLD):
        S.pop()
        S.append(SlD)
        return SMC(G, S, T, k)

    else:
        Gcpy.remove_node(u)
        X = SMC(Gcpy, S, T, k - 1)
        if X != -1:
            X.extend([u])
            return X
        else:
            S.pop()
            S.append(SlD)
            return SMC(G, S, T, k)


def DBF(G, D1, D2, k):

    GD2 = G.subgraph(D2)

    for order in nx.all_topological_sorts(GD2):

        GP = copy.deepcopy(G)
        S = []
        T = []
        for i in order:

            for j in list(G.in_edges(i)):
                GP.add_node(i + 1000)
                T.append(i + 1000)
                GP.add_edge([j[0], i + 1000])

            for j in list(G.out_edges(i)):
                GP.add_node(i + 2000)
                S.append(i + 2000)
                GP.add_edge([i + 2000, j[0]])

            GP.remove_node(i)

        X = list(SMC(GP, S, T, k))

        if all(x in D1 for x in X) and len(X) <= k and len(checkFVS(G, X)) != 0:
            return X

    return -1


def DFVSR(G, F, k):

    for i in range(k):
        sub = list(itertools.combinations(set(F), i))

        for F2 in sub:
            if len(nx.simple_cycles(G.subgraph(list(set(F) - set(F2))))) != 0:
                F1 = DBF(
                    G.subgraph(list(set(G.nodes) - set(F2))),
                    list(set(G.nodes) - set(F)),
                    list(set(F) - set(F2)),
                    k - i,
                )
                if F1 != -1:
                    F1.extend(F2)
                    return F1

    return -1


def DFVS(G, k):

    X = []

    V0 = list(range(1, k + 2))
    F0 = list(range(1, k + 1))

    G0 = G.subgraph(V0)

    VE = list(set(G.nodes) - set(V0))

    Gi = copy.deepcopy(G0)
    Vi = V0.copy()
    Fi = F0.copy()

    n = len(list(G.nodes))

    for i in range(1, n - k):

        Fi.append(i + k + 1)
        Vi.append(i + k + 1)
        Gi = G.subgraph(Vi)

        X = DFVSR(Gi, Fi, k)

        if X == -1:
            return -1

    return X
