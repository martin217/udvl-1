import os
import sys
sys.path[0:0] = [os.path.join(sys.path[0], '../examples/sat')]
import sat
P = 3 # pocet ludi
Agatha = 0
Butler = 1
Charles = 2
def killed(p1, p2):
    # p1 a p2 su vymenene
    # aby killed(X,Agatha) zodpovedalo 1, 2, 3
    return 0 * P * P + p2 * P + p1 + 1
def hates(p1, p2):
    return 1 * P * P + p1 * P + p2 + 1
def richer(p1, p2):
    return 2 * P * P + p1 * P + p2 + 1
def writeProblem(w):
    # Niekto v Dreadsburskom panstve zabil Agátu
    # Ex killed(x, A)
    # killed(A,A) | killed(B,A) | killed(C,A)
    for x in range(P):
        w.writeLiteral(killed(x, Agatha))
    w.finishClause()
    # A killer always hates his victim
    # VxVy (killed(x,y)-> hates(x, y))
    for x in range(P):
        for y in range(P):
            w.writeImpl(killed(x,y), hates(x, y))
            # A killer is no richer than his victim
            w.writeImpl(killed(x,y), -richer(x,y))
    #w.finishClause()
    # Charles hates noone that Agatha hates
    for x in range(P):
        w.writeImpl(hates(Agatha, x), -hates(Charles, x))
        # Agatha hates everybody except the butler
        if x != Butler:
            w.writeClause([ hates(Agatha, x)])
    # The butler hates everyone not richer than Aunt Agatha
    for x in range(P):
        w.writeImpl(-richer(x, Agatha), hates(Butler, x))
        # butler hates everyone whom Agatha hates
        w.writeImpl(hates(Agatha, x), hates(Butler, x))
    # Noone hates everyone
    for x in range(P):
        for y in range(P):
            w.writeLiteral(-hates(x, y))
        w.finishClause()
            
w = sat.DimacsWriter("agatha-cnf.txt")
writeProblem(w)
s = sat.SatSolver()
satisfiable, solution, = s.solve(w, "agatha-out.txt")
if not satisfiable:
    print("Teoria je nekonzistentna")
    sys.exit(1)
# Who killed Agatha?
w = sat.DimacsWriter("agatha-cnf-vrah.txt")
writeProblem(w)
vrah = Agatha
w.writeClause([ - killed(vrah, Agatha)])
satisfiable, solution, = s.solve(w, "agatha-vrah-out.txt")
if satisfiable:
    print("{} nie je vrahom, lebo {}".format(vrah, solution))
else:
    print("{} je vrahom".format(vrah))
