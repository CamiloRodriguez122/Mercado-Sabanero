# Mercado Sabanero – Módulo de liquidación de compras

Lógica de negocio (sin interfaz ni base de datos) que liquida una compra de la
tienda en línea Mercado Sabanero (Sincelejo, Sucre). Desarrollado con **TDD**.
Electiva Profesional en Ingeniería de Software – Agilidad Continua – CECAR.

## Herramientas
 Propósito | Herramienta |

 Lenguaje | Python 3.10 o superior |
 Pruebas unitarias | pytest |
 Dobles de prueba (mock del inventario) | unittest.mock |
 Cobertura | coverage.py |
 Control de versiones | Git + GitHub |

## Instalación
```bash
git clone https://github.com/CamiloRodriguez122/Mercado-Sabanero
cd mercado-sabanero
python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
# Linux / macOS:         source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar las pruebas
```bash
pytest                      # todas las pruebas
pytest tests/test_iva.py    # un solo archivo
pytest -k "cupon"           # pruebas cuyo nombre contenga "cupon"
```

## Cobertura
```bash
coverage run -m pytest
coverage report -m          # tabla en consola (falla si hay menos de 80 %)
coverage html               # reporte navegable en htmlcov/index.html
```

## Estructura
```
mercado_sabanero/   código de negocio (una responsabilidad por módulo)
tests/              pruebas unitarias (patrón AAA)
```

## Supuestos de diseño
* Dinero en pesos enteros; redondeo al peso más cercano (la mitad sube).
* El límite de 1 a 50 unidades se valida **por operación**; el stock se valida
  contra la cantidad **total** resultante en el carrito.
* "Productos con IVA" del envío gratis = líneas cuya tarifa es 5 % o 19 %, sumadas **antes** del descuento.
* El descuento se reparte proporcionalmente: el IVA de cada línea se calcula sobre su valor con descuento.
* SABANERO10 con subtotal menor a $50.000 se rechaza con `CuponInvalidoError`.
* Los cupones vencen el 31/12/2026 (configurable en `cupones.py`).

## Equipo
 Integrante

 Camilo Andrés Rodríguez Arrieta
 Jesús Villalba

