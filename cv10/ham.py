#!/bin/env python3

class HamiltonianCycle(object):
    
    def p(self, pos, i, n):
        return pos * n+i+1;
        
    def find(self, edges):
        """ Finds a hamiltonian cycle in the graph given by 'edges'
            or returns an empty list if there is none.

            @param edges an incidence matrix, edges[i][j] is True if there
            is an edge from i to j
        """

        n = len(edges) # number of vertices in the graph
        solver = sat.SatSolver()
        w = sat.DimacsWriter('ham_in_cnf_in.txt')
        
        #V pos: (p_pos_0 v p_pos_1 v ... v p_pos_(n-1))
        for pos in range(n):
            for i in range(n):
                w.writeLiteral(self.p(pos,i,n))
            w.finishClause()    

        #Vpos, Vi, Vj, i != j: -([p_posl_i,p_pos2_i)
        for pos in range(n):
            for i in range(n):
                for j in range(n):
                    if i!=j:
                        a = self.p(pos,i,n)
                        b = -self.p(pos,j,n)
                        w.writeImpl(a, b)

        for pos in range(n):
            for pos2 in range(n):
                for v in range(n):
                    if pos!=pos2:
                        a = self.p(pos,v,n)
                        b = -self.p(pos2,v,n)
                        w.writeImpl(a, b)
                        
        #ak nieje hrana z i do j, tak nemoze byt j hned za i
        
        for i in range(n):
            for j in range(n):
                if i!=j:
                    if edges[i][j]==False:
                        for pos in range(n):
                            a = self.p(pos%n,i,n)
                            b = -self.p((pos+1)%n,j,n)
                            w.writeImpl(a, b)           
        
        
        ok, sol = solver.solve(w, 'ham_in_cnf_out.txt')
        result = list()
        if ok:
            for x in sol:
                if x>0:
                    result.append((x-1)%n)
        else:
            result=[]
            
        return result
        
        #return [4, 5, 2, 1, 3, 0]
        return []

# vim: set sw=4 ts=4 sts=4 et :
