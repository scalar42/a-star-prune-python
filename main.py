###################################################
## Title: Algorithm inplementation for A *Prune ##
##          Date: July 19, 2019                  ##
##          Author: Daoxu Sheng                  ##
## Environments: Python 3.7.3 with networkx 2.3  ##
###################################################

import networkx as nx
# import matplotlib.pyplot as plt

def SIMPLE_PATH(): return True

def astar_prune(G, s, t, w, C, K, R):
    
    #print("Calls for astar_prune function.")
    
    ######################################
    #########   [1] preprocess   #########
    ######################################
    C_r = {}
    D = {}
    D[s] = {}
    for i in range(DG.number_of_nodes()):
        if i != s : # Paper is wrong, should not give the i != t condition or you won't get the C_r(s,t) value
            D[i] = {}
            C_r[i] = {}
            D[i][t] = {}
            D[s][i] = {}
            C_r[i][t] = {}
            for r in range(1, R+1):
                try:
                    D[i][t][r] = nx.dijkstra_path_length(G, i, t)
                    D[s][i][r] = nx.dijkstra_path_length(G, s, i)
                    C_r[i][t][r] = C_r[s][t][r] - D[s][i][r]
                except:
                    pass
    # print("D matrix:")
    # pp.pprint(D)
    # print("C_r(i,t) matrix:")
    # pp.pprint(C_r)

    A = {}
    for i in range(DG.number_of_nodes()):
        if i != s : #same as the loop before, deleted the i != t condition
            A[i] = {}
            A[i][t] = {}
            A[i][t][str(C_r[i][t])] = {}
            for r in range(1, R+1):
                try:
                    A[i][t][str(C_r[i][t])][r] = D[i][t][r]
                except:
                    print(D[i][t][r])
                    pass
            # calulate A_0, sum of all the R-dimen A metrics  which is not specifically pointed out in the pseudocode 
            A[i][t][str(C_r[i][t])][0] = sum([A[i][t][str(C_r[i][t])][key] for key in A[i][t][str(C_r[i][t])]])
    # print("A matrix:")
    # pp.pprint(A)

    ######################################
    #########   [2] initialize   #########
    ######################################
    k = 0
    W = {}
    H = {}
    W[str((s,))] = {}
    for r in range(0, R+1):
        W[str((s,))][r] = 0
    H[str((s,))] = {r: nx.dijkstra_path_length(G, s, t)
          for r in range(1, R+1)}
    AHP_heap = [(s,)]
    CSP_list = set()

    ######################################
    #########    [3] calculate   #########
    ######################################
    while k < K and AHP_heap: # The paper is wrong, should be k<K, not k<=K
        q_s_u = AHP_heap.pop(0)
        heapsort(AHP_heap, W, A, C_r)
        u = q_s_u[-1]  # the end node of q[s][u]
        if u == t:
            CSP_list.add(q_s_u)  # insert q[s][u] into CSP_list
            k += 1
            continue
        OutEdges = {e for e in G.edges if e[0] == u} # OutEdges = {all edges outgoing from node u}
        while OutEdges:
            e_u_v = OutEdges.pop()
            p_s_v = q_s_u + e_u_v[1:]
            W[str(p_s_v)] = {r: (W[str(q_s_u)][r] + w[e_u_v][r]) for r in range(1, R+1)}
            # calulate W_0, sum of all the R-dimen W metrics which is not specifically pointed out in the pseudocode 
            W[str(p_s_v)][0] = sum([W[str(p_s_v)][key] for key in W[str(p_s_v)]])
            if SIMPLE_PATH() and e_u_v[-1] in q_s_u:
                continue
            for r in range(1, R+1):
                # Caution: I directly compute the H_r value 
                # instead of inlementing a function for that
                if W[str(p_s_v)][r] + A[e_u_v[-1]][t][str(C_r[e_u_v[-1]][t])][r] > C[r]:
                    continue
                if p_s_v not in AHP_heap:
                    AHP_heap.append(p_s_v)  # insert p_s_u into AHP_heap
                heapsort(AHP_heap, W, A, C_r)
    return CSP_list

def heapsort(AHP_heap, W, A, C_r):
    # a bit of hack here
    AHP_heap.sort(key=lambda x: W[str(x)][0] + A[x[-1]][t][str(C_r[x[-1]][t])][0])

if __name__ == "__main__":
    # [0] import data
    # this is a fake data I made up for test
    s = 6
    t = 0
    R = 3
    K = 2

    DG = nx.DiGraph()
    nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    edges = [(1, 0), (2, 1), (3, 2), (4, 1), (5, 1),
              (6, 7), (7, 2), (7, 5), (8, 2), (9, 1)]
    DG.add_nodes_from(nodes)
    DG.add_edges_from(edges, weight=1)

    w = {}
    for edge in edges:
        w[edge] = {}
        for r in range(1, R+1):
            w[edge][r] = 1

    C = {}
    for r in range(1, R+1):
        C[r] = 100

    # ![0] import data #


    # # #   show this graph   # # #
    # uncomment below if wanna see the graph
    # print(list(DG.nodes))
    # print(list(DG.edges))
    # nx.draw(DG, with_labels=True)
    # plt.show()
    # # # # # # # # # # # # # # # #

    CSP = astar_prune(DG, s, t, w, C, K, R)

    print("The CSP list is:")
    print(CSP)

    # if K >= 2 the results print on screen should be:
    # (6, 7, 2, 1, 0)
    # (6, 7, 5, 1, 0)
