from resident_assignment_instance import *
import cplex
import numpy as np 

TOLERANCE = 1e-6

def greedy_solution(inst):
    print("------------------------- GREEDY ------------------------------")        
    # Approach / Enfoque que creemos que esta usando la competencia. 
    # Recibe una instancia de ResidentAssignmentInstance y  devuelve la satisfaccion global agregada y la solución 
    # Enunciado: "Su estrategia se basa en obtener una solucion utilizando tecnicas heurısiticas, en particular una de las 
    # denominadas greedy (codiciosas), buscando soluciones de buena calidad de manera rapida. Nuestro equipo 
    # de desarrollo nos provee una implementacion de lo que, se estima, serıa su enfoque para abordar el problema."
    arcs = [(i,j,inst.get_resident_pref(i,j) + inst.get_hospital_pref(j,i)) for i in range(inst.n) for j in range(inst.m)]    
    arcs = sorted(arcs, key = lambda x : x[2], reverse = True)
    res = [0]*inst.n 
    hos = [inst.p]*inst.m # indica cuantas vacantes libres van quedado a medida que se hace la asignación
    sol = []
    for elem in arcs:
        i = elem[0]
        j = elem[1]
        if res[i] == 0 and hos[j] > 0: # si el residente no esta asignado y el hospital tiene bacantes lo asigno
            sol.append((i,j)) 
            res[i] = 1
            hos[j] -= 1
            
    acum = 0.0 # para obtener el valor de la funcion objetivo 
    #res_prefs = []
    #hos_prefs = [] 
    count_res_not_desired = 0
    sum_resident_global = 0
    count_pref_res = 0
    count_pref_hos = 0
    count_pref_global = 0
    
    for i,j in sol:
        val = inst.get_resident_pref(i,j) + inst.get_hospital_pref(j,i)
        acum += val    
        # Se obtienen las nuevas métricas calculadas:
        # preferencia residentes
        if j in inst.res[i] :
            count_pref_res += 1 
              
        # preferencia hospitales      
        if i in inst.hos[j]:
            count_pref_hos += 1    
            
        # preferencia mutua 
        if i in inst.hos[j] and j in inst.res[i]:
            count_pref_global += 1    
               
        # Hospitales: Cantidad de residentes asignados que no estaban en la lista de deseados por parte de cada hspital
        if inst.get_hospital_pref(j,i) == -1: # se cuenta la cantidad de no deseados
             count_res_not_desired += 1  
        
        # Residentes: Se registra la posición de el hospital asignado. 
        # Para esto se utiliza la función get_resident_pref(i,j) y se divide por 2 para obtener la posición del hospital asignado al residente.
        sum_resident_global = sum_resident_global + (inst.get_resident_pref(i,j)  / 2)
        
    # Se otiene la posición promedio del hospital asignado en relación a la preferencia del residente.
    # Se suma 1 simplemente para indicar que 1 corresponde la posición ideal deseada para todos los residentes. 
    # En este escenario, a cada residente se le habría asignado el hospital de mayor preferencia.
    pos_resident_prom = inst.l -  (sum_resident_global / inst.n) + 1 
    
    # Se imprime la función objetivo greedy
    print("acum_greedy:", acum)       
    print('count_sat_res_greedy', count_pref_res)
    print('count_sat_hos_greedy', count_pref_hos)
    print('count_sat_global_greedy', count_pref_global)
    print('count_res_not_desired_greedy: ' , count_res_not_desired)
    print('desired_position_hos_for_res_greedy: ' , round(pos_resident_prom , 2) )
   
    
    return acum,sol,count_pref_res,count_pref_hos,count_pref_global, count_res_not_desired , pos_resident_prom


def add_residents_constraints(inst,myprob): 
    # agrega las restricciones referentes a los residentes a myprob
    vals = [1.0] * (inst.m) # posiciones de tupla con valroes distintos de cero

    for j in range(inst.n): # Se itera por los residentes
        ind = []      
        # Se recorreran las tuplas relevantes
        # Se agrega en cada caso el indice de la variable que representa al arco (i,j), gauardado en var_idx.
        for i in range(inst.m): # Se itera por los hospitales 
            ind.append(inst.var_idx[(i,j)])
        row = [ind,vals]          
        #print('row_residents', row)
        myprob.linear_constraints.add(lin_expr = [row], senses = ['E'], rhs = [1])
    
def add_hospital_constraints(inst,myprob):
    vals = [1.0]* (inst.n) # posiciones de tupla con valroes distintos de cero

    for i in range(inst.m): # Se itera por los hospitales 
         ind = []
         for j in range(inst.n): # Se itera por los residentes
             ind.append(inst.var_idx[(i,j)])
         row = [ind,vals]      
         #print('row_hospital', row)         
         myprob.linear_constraints.add(lin_expr = [row], senses = ['E'], rhs = [inst.p])
    

def generate_constraints(inst,myprob):
    # genera las restricciones
    
    # Se agregan las restricciones de residentes
    add_residents_constraints(inst,myprob)

    # Se agregan las restricciones de hospitales
    add_hospital_constraints(inst,myprob)

# función auxiliar para calculo de la satisfacción global 
def generate_costs(inst):  
    cost = [[0] * inst.n for _ in range(inst.m)] # Matriz de m filas y n columnas inicializada  con 0
    
    for i in range(inst.m): # Se itera por los hospitales 
        for j in range(inst.n): # Se itera por los residentes       
            # satisfaccion total:
            sat_tot = inst.get_hospital_pref(i , j) + inst.get_resident_pref(j , i)
            cost[i][j] = sat_tot                          
            #print('residente:', j, '_ hospital:', i,'sat_res' , inst.get_resident_pref(j , i), 'sat_hos' , inst.get_hospital_pref(i , j) ,'sat_tot:', sat_tot)
    inst.cost = cost  
    
def generate_variables(inst,myprob):
    n_vars_tot = inst.n*inst.m
    obj = [0]*n_vars_tot
    lb = [0]*n_vars_tot
    names = []   
    var_cnt = 0 # var_cnt va a ser el valor que va llevando la cuenta de cuantas variables agregamos hasta el momento.
 
    # se generan los indices.
    for i in range(inst.m): # se recorren los hospitales 
        for j in range(inst.n): # se recorren los residentes 
            # se define el valor para (i,j). 
            #print((i,j), var_cnt) # la tupla i,j está representnando una variable, y el indice de esa variable va a ser var_cnt           
            inst.var_idx[(i, j)] = var_cnt # se guarda el indice para cada variable.
            obj[var_cnt] = inst.cost[i][j]           
            # se generan los nombres
            name =  'x_' + str(i) + '_' + str(j)
            names.append(name)
            # se incrementa el proximo indice no usado
            var_cnt = var_cnt + 1
    # Se agregan las variables al modelo.
    myprob.variables.add(obj = obj, lb = lb, names = names)

def populate_by_row(inst,myprob):

    # Se generan las variables.
    generate_variables(inst,myprob)

    # Se generan las restricciones.
    generate_constraints(inst,myprob)
    
    # Se configura el problema de maximización.
    myprob.objective.set_sense(myprob.objective.sense.maximize)



def solve_instance(inst):
    # resuelve la instancia del problena
    myprob = cplex.Cplex()
    myprob.set_results_stream(None) # para que cplex no muestre cosas por pantalla.
    
    # Se genera la matriz de costos
    generate_costs(inst)
    
    # Se crea el modelo.
    populate_by_row(inst,myprob)

    # Se resuelve el modelo.
    myprob.solve()

    # Se obtiene la info de la funcion.
    print("------------------------- LP-----------------------------------")    
    x = myprob.solution.get_values() 
    f_obj = myprob.solution.get_objective_value() 
    #print('Funcion objetivo: ', f_obj)
    #print('x :' , x)
    sol = []
    acum = 0.0 # para obtener el valor de la funcion objetivo 
    count_res_not_desired = 0  # Métrica hospitales: cantidad de residentes no deseados por hospital
    sum_resident_global = 0  # Métrica Residentes: posición promedio del hospital asignado en relación a la preferencia del residente.
    count_pref_res = 0
    count_pref_hos = 0
    count_pref_global = 0
    
    for i in range(inst.m): # Se itera por los hospitales 
        for j in range(inst.n):  # Se itera por los residentes         
            val = x[inst.var_idx[(i , j)]]
            if val > TOLERANCE:                           
                #print('x_' + str(i) + '_' +str(j) , val)
                acum = acum + inst.cost[i][j]
                sol.append((i,j))  

    # se obtienen las métricas calculadas
    for i,j in sol:  
        # preferencia residentes
        if i in inst.res[j] :
            count_pref_res += 1 
            
        # preferencia hospitales
        if j in inst.hos[i]:
             count_pref_hos += 1     
            
        # preferencia mutua 
        if j in inst.hos[i] and i in inst.res[j]:
            count_pref_global += 1
            
        # Hospitales: Cantidad de residentes asignados que no estaban en la lista de deseados por parte de cada hspital
        if inst.get_hospital_pref(i,j) == -1: # se cuenta la cantidad de no deseados
              count_res_not_desired += 1  
         
        # Residentes: Se registra la posición de el hospital asignado. 
        # Para esto se utiliza la función get_resident_pref(j,i) y se divide por 2 para obtener la posición del hospital asignado al residente.
        sum_resident_global = sum_resident_global + (inst.get_resident_pref(j,i)  / 2)          
        
    # Se otiene la posición promedio del hospital asignado en relación a la preferencia del residente.
    # Se suma 1 simplemente para indicar que 1 corresponde la posición ideal deseada para todos los residentes. 
    # En este escenario, a cada residente se le habría asignado el hospital de mayor preferencia.
    pos_resident_prom = inst.l -  (sum_resident_global / inst.n) + 1 
       
    # Se imprime la función objetivo LP
    print("acum_lp", acum)       
    print('count_sat_res_lp', count_pref_res)
    print('count_sat_hos_lp', count_pref_hos)
    print('count_sat_global_lp', count_pref_global)
    print('count_res_not_desired_lp: ' , count_res_not_desired)
    print('desired_position_hos_for_res_lp:' , round(pos_resident_prom , 2) ) 
        
    return acum,sol,count_pref_res,count_pref_hos,count_pref_global,count_res_not_desired,pos_resident_prom 
    
                
                
def get_instance_set(size):
    # Esta funcion toma todos los paths/rutas de los archivos de tamaño size 
    # que se encuentren en el directorio data/ y devuelve una lista
    base = 'data/test_inst_'

    ret = []
    for i in range(10):
        filename = base + size + '_' + str(i) + '.in' 
        ret.append(filename)
    return ret

def main():


    #obtención de todos los nombres de archivo de las instancias "pequeñas" o "small". 
    #instances = get_instance_set('small')
    instances = get_instance_set('medium')
    #instances = get_instance_set('large')

    # se resuelven las instnacias del grupo elegido.
    greedy_results = [] # Resultados métrica inicial greedy
    greedy_count_pref_res = []
    greedy_count_pref_hos = []
    greedy_count_pref_global = []
    greedy_count_res_not_desired = [] # Resultados métrica hospital greedy
    greedy_pos_resident_prom = [] # Resultado métrica residente greedy
    
    lp_results = [] # Resultados métrica inicial lp
    lp_count_pref_res = []
    lp_count_pref_hos = []
    lp_count_pref_global = []
    lp_count_res_not_desired = [] # Resultados métrica hospital lp
    lp_pos_resident_prom = [] # Resultados métrica hospital lp
    
    gap = [] # Diferencia entre greedy y lp
    for filename in instances:
        inst = ResidentAssignmentInstance()
        inst.load(filename)
        
        # se resuelve la instancia
        lp_ret,lp_sol, count_pref_res_linear, count_pref_hos_linear, count_pref_global_linear,count_res_not_desired_linear , pos_resident_prom_linear  = solve_instance(inst) # se resuelve el problema con programacion lineal    
        lp_results.append(lp_ret)
               
        g_ret,g_sol, count_pref_res, count_pref_hos, count_pref_global, count_res_not_desired, pos_resident_prom  = greedy_solution(inst) # se resuelve el problema con la soluciíon greedy        
        greedy_results.append(g_ret)       
        # para cada instancia se registra la diferencia entre ambas soluciones
        gap.append(round((lp_ret - g_ret) /  g_ret ,4 ) )
        
        # para cada instancia se obtienen las nuevas métricas definidas para evaluar la satisf. de los residentes y de los hospitales
        # lp:
        lp_count_pref_res.append(count_pref_res_linear)
        lp_count_pref_hos.append(count_pref_hos_linear)
        lp_count_pref_global.append(count_pref_global_linear)
        
        lp_count_res_not_desired.append(count_res_not_desired_linear)
        lp_pos_resident_prom.append(round(pos_resident_prom_linear  , 2 ) )
        
        # greedy:
        greedy_count_pref_res.append(count_pref_res)
        greedy_count_pref_hos.append(count_pref_hos)
        greedy_count_pref_global.append(count_pref_global)   
            
        greedy_count_res_not_desired.append(count_res_not_desired )
        greedy_pos_resident_prom.append(round(pos_resident_prom , 2 ) )
    
    
    print('--------------RESULTADOS CONSOLIDADOS--------------------------')
    print('lp_results_global: ', lp_results)
    
    print('lp_count_pref_res: ', lp_count_pref_res)
    print('lp_count_pref_hos: ', lp_count_pref_hos)
    print('lp_count_pref_global: ', lp_count_pref_global)
    
    print('count_res_not_desired_lp_global: ', lp_count_res_not_desired)
    print('desired_position_hos_for_res_lp_global: ', lp_pos_resident_prom)
    
    print('----------------------------------------')
    print('greedy_results_global', greedy_results)
    
    print('greedy_count_pref_res: ', greedy_count_pref_res)
    print('greedy_count_pref_hos: ', greedy_count_pref_hos)
    print('greedy_count_pref_global: ', greedy_count_pref_global)
    
    print('count_res_not_desired_greedy_global: ', greedy_count_res_not_desired)
    print('desired_position_hos_for_res_greedy_global:', greedy_pos_resident_prom)
    
    
    print('----------------------------------------')
    print('gap_results: ', gap)  
    print('gap_mean: ',round( np.mean(gap) * 100  ,4), '%')
    


if __name__ == "__main__":
    main()
