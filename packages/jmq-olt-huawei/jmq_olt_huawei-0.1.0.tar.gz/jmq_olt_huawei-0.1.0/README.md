# README - jmq_olt_huawei

**Paquete de integración con OLTs Huawei MA56XXT (como MA5603T) vía Telnet, diseñado para automatizar la recolección de información GPON desde Python.**

## 🛰️ ¿Qué hace este paquete?

Permite conectarse a una OLT Huawei MA56XXT y ejecutar operaciones como:

- Listar slots activos (`display board 0`)
- Consultar puertos GPON por slot
- Obtener ONTs conectadas a cada puerto
- Realizar un escaneo completo (slots → puertos → ONTs)
- Manejar paginación, prompts dinámicos y errores comunes de sesión

## 📦 Instalación

```bash
pip install jmq_olt_huawei
```

ó

```bash
pip install git+https://github.com/juaquicar/jmq_olt_huawei.git
```


O si lo tienes clonado localmente:

```bash
pip install .
```

> Requiere Python >= 3.6.

## 🧪 Ejemplo de uso

```python
from jmq_olt_huawei.ma56xxt import APIMA56XXT, UserBusyError
from pprint import pprint

api = APIMA56XXT(
    host='192.168.88.25',
    user='root',
    password='admin',
    prompt='MA5603T',
    debug=True
)

try:
    api.connect()
    result = api.scan_all()
    pprint(result)
except UserBusyError as e:
    print(f"ERROR: {e}")
finally:
    api.disconnect()
```

## 📁 Estructura del paquete

```
jmq_olt_huawei/
│
├── ma56xxt.py          # Lógica principal de conexión y parsing
├── __init__.py         # Archivo de inicialización del paquete
├── Examples/           # Scripts de ejemplo (opcional)
├── tests/              # Pruebas automatizadas (pendiente)
├── requirements.txt    # Requisitos opcionales para desarrollo
├── pyproject.toml      # Configuración de build con setuptools
├── LICENSE             # Licencia MIT
└── README.md           # Este archivo
```

## 🧩 Funcionalidades destacadas

* Prompt dinámico configurable
* Manejador de errores comunes como bloqueo de usuario
* Soporte para múltiples niveles de lectura (slots → puertos → ONTs)
* Debug opcional para inspeccionar línea a línea

## ⚖️ Licencia

MIT © [Juanma Quijada](mailto:quijada.jm@gmail.com)

## 🌐 Enlace al proyecto

[Repositorio en GitHub](https://github.com/juaquicar/jmq_olt_huawei)




