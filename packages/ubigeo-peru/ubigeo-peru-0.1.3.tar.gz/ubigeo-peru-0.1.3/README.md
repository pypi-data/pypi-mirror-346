# Ubigeo Peru

Este paquete proporciona acceso a los datos de los UBIGEO de Perú, permitiendo consultas por código de UBIGEO y devolviendo información sobre distritos, provincias y departamentos.


## Uso en Python

> Para utilizar el paquete en un script de Python, simplemente importa la función buscar_por_ubigeo y proporciona el código de UBIGEO como argumento.
>
>> Esto devolverá un diccionario con la información del distrito, provincia y departamento.

```
from ubigeo_peru import buscar_por_ubigeo

codigo_ubigeo = '010101' 
resultado = buscar_por_ubigeo(codigo_ubigeo)

print(resultado)

Salida esperada:
{
    'Ubigeo': '010101',
    'Distrito': 'Chachapoyas',
    'Provincia': 'Chachapoyas',
    'Departamento': 'Amazonas'
}
```

## Uso en Django

> En Django, puedes utilizar el paquete en cualquier vista o modelo donde necesites obtener la información del UBIGEO.
>
>> Por ejemplo, puedes utilizarlo en una vista para mostrar información del distrito, provincia y departamento basado en el código de UBIGEO.

```
from django.shortcuts import render
from ubigeo_peru import buscar_por_ubigeo

def ubigeo_view(request):
    # Ejemplo de consulta por UBIGEO
    codigo_ubigeo = '010101'  # UBIGEO de Chachapoyas
    resultado = buscar_por_ubigeo(codigo_ubigeo)

    return render(request, 'ubigeo_template.html', {'resultado': resultado})
```

## Uso en Flask
> En Flask, puedes utilizar el paquete de manera similar. Aquí te mostramos cómo integrarlo en una ruta para consultar la información del UBIGEO.
>

```
from flask import Flask, render_template
from ubigeo_peru import buscar_por_ubigeo

app = Flask(__name__)

@app.route('/ubigeo/<codigo_ubigeo>')
def ubigeo(codigo_ubigeo):
    # Consulta por UBIGEO
    resultado = buscar_por_ubigeo(codigo_ubigeo)
    return render_template('ubigeo_template.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True) 
```

## Instalación

Puedes instalar el paquete usando pip:

```bash
pip install ubigeo-peru