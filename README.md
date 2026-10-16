# Fichas de la comunidad

Catálogo público de fichas para **Creador Ficha de Personaje**.

La app consulta `catalog.json`, muestra una vista previa y descarga una copia de la ficha. Las fichas descargadas funcionan sin conexión y se pueden editar o borrar. Las partidas personales no se incluyen en el catálogo.

## Fichas disponibles

- **El juicio del diablo**, compartida por JoseTamayoMaluenda. Incluye dos hojas y sus imágenes de fondo.

## Organización

- `catalog.json`: listado publicado que consulta la app.
- `packages/`: fichas completas en archivos `.ficha`.
- `previews/`: imágenes de muestra.
- `tools/pack_sheet.py`: herramienta para preparar una ficha y actualizar el catálogo.

## Publicar una ficha

Las aportaciones se revisan antes de incorporarlas a la rama `main`. Para esta primera versión la publicación es manual; la descarga desde la app es directa y no necesita cuenta de GitHub.

Cada ficha debe contener sus imágenes y todas sus hojas. Indica su nombre, autor y librojuego y comparte únicamente contenido que tengas permiso para distribuir. No incluyas partidas ni información personal de jugadores.

Un archivo `.ficha` es un ZIP con esta estructura:

```
manifest.json
sheet.json
images/fondo.jpg
```

El manifiesto debe ser:

```json
{"format":"creador-ficha","version":1,"sheet":"sheet.json"}
```

`sheet.json` contiene la ficha del editor. Sus fondos se identifican con el nombre del archivo, sin carpetas; las imágenes correspondientes van dentro de `images/`.

Para preparar una ficha a partir de su JSON y sus imágenes:

```
python tools/pack_sheet.py ruta/ficha.json ruta/imagenes --id nombre-del-librojuego --author TuNombre --preview ruta/vista-previa.jpg
```

La herramienta copia los recursos al catálogo y calcula la huella SHA-256 del paquete. Publica juntos el paquete, la vista previa y el índice actualizado.

## Catálogo

Cada entrada incluye `id`, `name`, `author`, `gamebook`, `description`, `version`, `package`, `thumbnail` y `sha256`. Las rutas son relativas a `catalog.json` y deben pertenecer a este repositorio.

El formato actual del índice es `creador-ficha-catalogue`, versión `1`.

