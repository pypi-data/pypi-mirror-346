from numath.transformacion import crear_funcion

### BISECCION ###

def bisection(funcion, a, b, TOL=1e-5, N0=100):

    f = crear_funcion(funcion)

    if f(a) * f(b) >= 0:
        raise ValueError("El método de bisección requiere que f(a) y f(b) tengan signos opuestos.")

    i = 1
    FA = f(a)

    while i <= N0:
        p = a + (b - a) / 2.0
        FP = f(p)
        if FP == 0 or (b - a) / 2 < TOL:
            return p, i  
        i += 1
        if FA * FP > 0:
            a = p
            FA = FP 
        else:
            b = p

    raise ValueError(f"El método fracasó después de {N0} iteraciones.")

### ITERACION DE PUNTO FIJO ###

def fixed_point_iteration(funcion, p0, TOL=1e-5, N0=100):

    g = crear_funcion(funcion)
    i = 1  
    while i <= N0:  
        p = g(p0)  
        if abs(p - p0) < TOL:  
            return p, i  
        i += 1  
        p0 = p  

    raise ValueError(f"El método falló después de {N0} iteraciones.")

### METODO DE NEWTON  ###

def _derivative(f, TOL=1e-5):
    return lambda x: (f(x + TOL) - f(x - TOL)) / (2 * TOL)

def newton_method(funcion, p0, TOL=1e-5, N0=100, factor=1e-8):
  
    f = crear_funcion(funcion)
    df = _derivative(f, TOL)
    i = 1  

    while i <= N0:  
        derivada = df(p0)
        if abs(derivada) < factor:
            raise ValueError(f"Error: la derivada evaluada en p0 = {p0} es demasiado pequeña, no se puede continuar con el método de Newton")
        
        p = p0 - f(p0) / derivada
        if abs(p - p0) < TOL:
            return p, i
        i += 1
        p0 = p

    raise ValueError(f"El método falló después de {N0} iteraciones.")

### METODO DE LA SECANTE  ###

def secant_method(funcion, p0, p1, TOL=1e-5, N0=100):
   
    f = crear_funcion(funcion)
    i = 2 
    q0 = f(p0)
    q1 = f(p1)
    
    while i <= N0:
        if q1 - q0 == 0:
            raise ValueError("División por cero: f(p1) y f(p0) son iguales.")
        
        p = p1 - q1 * (p1 - p0) / (q1 - q0)
        if abs(p - p1) < TOL:
            return p, i
        i += 1
        p0, q0 = p1, q1
        p1 = p
        q1 = f(p1)
    
    raise ValueError(f"El método falló después de {N0} iteraciones.")

### METODO DE POSICION FALSA ###

def false_position(funcion, p0, p1, TOL=1e-5, N0=100):
    
    f = crear_funcion(funcion)
    if f(p0) * f(p1) >= 0:
        raise ValueError("Los puntos iniciales no encierran una raíz: f(p0) y f(p1) deben tener signos opuestos.")

    i = 2  
    q0 = f(p0)
    q1 = f(p1)
    
    while i <= N0:
        p = p1 - q1 * (p1 - p0) / (q1 - q0)
        if abs(p - p1) < TOL:
            return p, i
        i += 1
        q = f(p)
        if q * q1 < 0:
            p0 = p1
            q0 = q1
        p1 = p
        q1 = q

    raise ValueError(f"El método falló después de {N0} iteraciones.")

### METODO DE STEFFENSEN  ###

def steffensen_method(funcion, p0, TOL=1e-5, N0=100):
    
    g = crear_funcion(funcion)
    i = 1 
    while i <= N0:
        p1 = g(p0)    
        if abs(p1 - p0) < TOL:
            return p0, i  
        p2 = g(p1)      
        denominator = p2 - 2 * p1 + p0
        if denominator == 0:
            raise ValueError("Denominador cero en el cálculo de p; el método no puede continuar.")
       
        p = p0 - ((p1 - p0) ** 2) / denominator 
        if abs(p - p0) < TOL:  
            return p, i
        i += 1               
        p0 = p        

    raise ValueError(f"El método falló después de {N0} iteraciones.")

### METODO DE HORNER  ###

def horner_method(a, x0):
 
    n = len(a) - 1  
    y = a[0] 
    z = a[0] 
    for j in range(1, n):
        y = x0 * y + a[j]  
        z = x0 * z + y   
    y = x0 * y + a[n]
    return y, z

### METODO DE MÜLLER  ###

def muller_method(funcion, p0, p1, p2, TOL=1e-5, N0=100):
   
    f = crear_funcion(funcion)
    h1 = p1 - p0
    h2 = p2 - p1
    δ1 = (f(p1) - f(p0)) / h1
    δ2 = (f(p2) - f(p1)) / h2
    d = (δ2 - δ1) / (h2 + h1)
    i = 3
    while i <= N0:
        
        b = δ2 + h2 * d
        discriminant = b**2 - 4 * f(p2) * d
        if discriminant < 0:
            print("Discriminante negativo, la raíz será compleja o indefinida.")
            return "undefined" 
        D = discriminant**0.5  
        if abs(b - D) < abs(b + D):
            E = b + D
        else:
            E = b - D
        if E == 0:
            E = TOL 
        h = -2 * f(p2) / E
        p = p2 + h
        if abs(h) < TOL:
            return p
        p0 = p1
        p1 = p2
        p2 = p
        h1 = p1 - p0
        h2 = p2 - p1
        δ1 = (f(p1) - f(p0)) / h1
        δ2 = (f(p2) - f(p1)) / h2
        d = (δ2 - δ1) / (h2 + h1)
        i += 1
    
    raise RuntimeError(f"El método falló después de {N0} iteraciones")
