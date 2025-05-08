# Documentación de la clase Transformación

Este módulo permite convertir cadenas de texto con funciones matemáticas en _callables_ de Python (funciones `lambda`) que aceptan hasta tres variables (`x`, `y`, `z`) de forma muy flexible, insertando automáticamente las transformaciones y los operadores de multiplicación implícita necesarios.

## `reemplazar_funciones(funcion_entrada)`

Convierte la notación “amigable” en expresiones válidas de Python:

- **Reemplazos básicos**  
  Sustituye funciones y constantes por sus equivalentes en el módulo `math`:
  ```python
  {
    'sin(':   'math.sin(',
    'cos(':   'math.cos(',
    'tan(':   'math.tan(',
    'asin(':  'math.asin(',
    'acos(':  'math.acos(',
    'atan(':  'math.atan(',
    'exp(':   'math.exp(',
    'ln(':    'math.log(',
    'sqrt(':  'math.sqrt(',
    '^':      '**',
    'pow(':   'math.pow(',
    'pi':     'math.pi'
  }
  ```

- **Multiplicación implícita**  
  1. Inserta `*` cuando hay un dígito seguido de letra o función, p.ej.  
     `3x` → `3*x`  o  `2sin(x)` → `2*math.sin(x)`.  
  2. Inserta `*` cuando hay dos variables adyacentes (`x`,`y` o `z`), p.ej.  
     `xy` → `x*y`,  `yz` → `y*z`,  `zx` → `z*x`.


```python
# Ejemplo de transformación
reemplazar_funciones("3x^2 + sin(x) + yz")
"3*x**2 + math.sin(x) + y*z"
```

## `crear_funcion(funcion_entrada)`

Construye y devuelve una función `lambda` con **firma fija** `(x=0, y=0, z=0)`.  

- **Variables**  
  - Si la expresión sólo usa `x`, basta llamar `f(2)` o `f(x=2)`.  
  - Si usa `y`, llamar `f(y=3)` o `f(0,3)`.  
  - Si usa `z`, llamar `f(z=4)` o `f(0,0,4)`.  
  - Si mezcla varias, usar posiciónales o keywords según convenga.  
- **Errores**  
  - Cualquier keyword distinto de `x`, `y` o `z` (p.ej. `w=…`) levantará un `TypeError`.
  - Si la expresión no es válida tras el reemplazo, se lanza `ValueError`.

### Ejemplos de uso

```python
f1 = crear_funcion("3x + 2")
print(f1(2))        # 3*2 + 2 = 8

f2 = crear_funcion("5y - 1")
print(f2(y=4))      # 5*4 - 1 = 19

f3 = crear_funcion("z^2 + 1")
print(f3(z=3))      # 3**2 + 1 = 10

f4 = crear_funcion("x*y + 1")
print(f4(2, 3))     # 2*3 + 1 = 7
print(f4(x=4,y=2))  # 4*2 + 1 = 9

f5 = crear_funcion("x*y*z + z")
print(f5(2,3,4))    # 2*3*4 + 4 = 28

f6 = crear_funcion("xy + z")
print(f6(x=2, y=5, z=1))  # x*y + z = 2*5 + 1 = 11
```

### Seguridad y extensibilidad

- El entorno de `eval` queda restringido a `{'math': math}`.  
- Para incluir otras librerías (p.ej. `numpy`), pasar un diccionario ampliado a `eval`.  
- Para soportar más variables (p.ej. `t`), basta con:
  1. Añadir esa letra en la regex de `reemplazar_funciones`.  
  2. Cambiar la firma a `lambda x=0, y=0, z=0, t=0: …`.  
