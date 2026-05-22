# DAVS Mecanografia TEST

Test de velocidad de escritura construido con [Reflex](https://reflex.dev). Muestra un párrafo aleatorio, mide el tiempo desde la primera tecla hasta completar el texto, y presenta estadísticas al finalizar.

## Características

- Visualización carácter a carácter con colores (correcto, incorrecto, cursor, pendiente)
- Barra de progreso en tiempo real
- Estadísticas al finalizar: WPM, precisión, caracteres correctos, errores, tiempo y racha
- Protección contra copy-paste
- Reinicio con el botón del header o con la tecla Tab
- Párrafos en español cargados desde un archivo JSON

## Requisitos

- Python 3.10+
- Node.js 18+

## Instalación

```bash
git clone <url-del-repositorio>
cd DAVS_Mecanografia_test

python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Uso

```bash
reflex run
```

La aplicación queda disponible en `http://localhost:3000`.

## Estructura del proyecto

```
DAVS_mecanografia_test/
├── main/
│   ├── main.py              # Página principal y configuración de la app
│   ├── state.py             # Estado y lógica del test
│   ├── paragraphs.json      # Textos disponibles para el test
│   └── components/
│       ├── header.py        # Header con logo y botón de reinicio
│       ├── typing_area.py   # Área de texto y input de escritura
│       └── stats_bar.py     # Tarjetas de estadísticas
├── assets/
│   └── styles.css           # Estilos globales
└── rxconfig.py              # Configuración de Reflex
```

## Agregar textos

Para agregar nuevos párrafos al test, edita `main/paragraphs.json` siguiendo el mismo formato:

```json
{
  "paragraphs": [
    { "text": "Tu texto aquí." },
    { "text": "Otro texto aquí." }
  ]
}
```

El texto se selecciona aleatoriamente en cada reinicio. Se recomienda tener al menos 15-20 párrafos para evitar repeticiones frecuentes.

## Cómo se calcula el WPM

Se usa la fórmula estándar: caracteres correctos dividido en 5 (longitud promedio de una palabra), dividido por los minutos transcurridos. El cronómetro arranca con la primera tecla y se detiene al completar el texto.

## Dependencias

| Paquete | Versión |
|---|---|
| reflex | 0.9.2.post1 |
