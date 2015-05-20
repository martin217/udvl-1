#!/bin/env python3


import os
import sys
sys.path[0:0] = [os.path.join(sys.path[0], '../examples/sat')]
import sat

class HamiltonianCycle(object):
    
    def p(self, pos, i, n):
        return pos * n+i+1;
        
    def find(self, edges):
        """ Finds a hamiltonian cycle in the graph given by 'edges'
            or returns an empty list if there is none.
            @param edges an incidence matrix, edges[i][j] is True if there
            is an edge from i to j
        """
        solver = sat.SatSolver()
        w = sat.DimacsWriter('ham_in_cnf_in.txt')
        lenNodes = len(edges)
      
        #V pos: (p_pos_0 v p_pos_1 v ... v p_pos_(lenNodes-1))
        for pos in range(lenNodes):
            for i in range(lenNodes):
                w.writeLiteral(self.p(pos,i,lenNodes))
            w.finishClause()    

        #Vpos, Vi, Vj, i != j: -([p_posl_i,p_pos2_i)
        for pos in range(lenNodes):
            for i in range(lenNodes):
                for j in range(lenNodes):
                    if i!=j:
                        a = self.p(pos,i,lenNodes)
                        b = -self.p(pos,j,lenNodes)
                        w.writeImpl(a, b)

        for pos in range(lenNodes):
            for pos2 in range(lenNodes):
                for v in range(lenNodes):
                    if pos!=pos2:
                        a = self.p(pos,v,lenNodes)
                        b = -self.p(pos2,v,lenNodes)
                        w.writeImpl(a, b)
                        
        #ak nieje hrana z i do j, tak nemoze byt j hned za i
        
        for i in range(lenNodes):
            for j in range(lenNodes):
                if i!=j:
                    if edges[i][j]==False:
                        for pos in range(lenNodes):
                            a = self.p(pos%lenNodes,i,lenNodes)
                            b = -self.p((pos+1)%lenNodes,j,lenNodes)
                            w.writeImpl(a, b)           
        
        
        ok, sol = solver.solve(w, 'ham_in_cnf_out.txt')
        result = list()
        if ok:
            for x in sol:
                if x>0:
                    result.append((x-1)%lenNodes)
        else:
            result=[]
            
        return result

# vim: set sw=4 ts=4 sts=4 et :
