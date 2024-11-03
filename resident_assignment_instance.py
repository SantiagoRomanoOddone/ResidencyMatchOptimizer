import sys

class ResidentAssignmentInstance:
    def __init__(self):
        self.n = 0
        self.m = 0
        self.k = 0
        self.l = 0
        self.p = 0
        self.res = {}
        self.hos = {}
        self.cost = []
        self.penalty = 1.0
        self.var_idx = {} 


    def load(self,filename):

        # Abrimos el archivo.
        f = open(filename)

        # Leemos la primera linea con los parametros generales.
        row = f.readline().split(' ')
        self.n = int(row[0])
        self.m = int(row[1])
        self.k = int(row[2])
        self.l = int(row[3])
        self.p = int(row[4])

        # Leemos informacion de los residentes.
        for i in range(self.n):
            row = f.readline().split(' ')
            res_id = int(row[0])
            res_l = [int(x) for x in row[1:self.l+1]]
            self.res[res_id] = res_l

        # Leemos informacion de los hospitales.
        for j in range(self.m):
            row = f.readline().split(' ')
            hos_id = int(row[0])
            hos_l = [int(x) for x in row[1:self.k+1]]
            self.hos[hos_id] = hos_l
        # Cerramos el archivo.
        f.close()

    def get_resident_pref(self,res_id,hos_id):
        l = self.res[res_id]
        if hos_id in l:
            return 2.0*float(len(l) - l.index(hos_id))
        return -self.penalty

    def get_hospital_pref(self,hos_id,res_id):
        l = self.hos[hos_id]
        if res_id in l:
            return 2.0*float(len(l) - l.index(res_id))
        return -self.penalty
    
    
