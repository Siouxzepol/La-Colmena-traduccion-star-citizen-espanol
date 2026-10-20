# Star Citizen — traducción + BP al español de España

Traducción comunitaria no oficial para Star Citizen Alpha 4.10.2 LIVE. El archivo `global.ini` está preparado para la carpeta de localización `spanish_(spain)`.

## Compatibilidad y versión de la traducción

**Juego: Alpha 4.10.2 LIVE · Traducción: v1.0.30** — Actualizado el 20/10/2026. [Descargar el parche](https://github.com/Siouxzepol/traduccion-BP-star-citizen-espanol/releases/latest/download/Traduccion_SC_es-ES_LIVE.zip).

La localización añade marcadores `[BP]` y `[REP n]` a los títulos de misión cuando las recompensas son inequívocas para todas las variantes que comparten ese título. También añade reputación y posibles planos a ciertas descripciones de misión cuando pueden asociarse sin ambigüedad. Los planos pueden ser aleatorios y no se garantiza que se entreguen todos. El número de versión se incrementará con cada nueva publicación del parche.

## Instalación sencilla (LIVE)

1. Cierra Star Citizen.
2. Descarga el [paquete ZIP de la última versión](https://github.com/Siouxzepol/traduccion-BP-star-citizen-espanol/releases/latest/download/Traduccion_SC_es-ES_LIVE.zip).
3. Extrae su contenido en la carpeta raíz de Star Citizen, la que contiene la carpeta `LIVE` (por ejemplo, `C:\\Program Files\\Roberts Space Industries\\StarCitizen\\`).
4. Si Windows pregunta si quieres reemplazar archivos, confirma después de guardar una copia del archivo anterior.
5. Inicia el juego y selecciona español de España.

El ZIP ya incluye la ruta `LIVE/data/Localization/spanish_(spain)/global.ini`; no lo extraigas dentro de `LIVE`, porque se duplicaría esa carpeta. El paquete es solo para LIVE, no para PTU.

## Instalación manual

Si prefieres no usar el ZIP, copia el [`global.ini`](https://github.com/Siouxzepol/traduccion-BP-star-citizen-espanol/blob/main/global.ini) en `LIVE/data/Localization/spanish_(spain)/global.ini`, guardando antes una copia del archivo original.

Las actualizaciones del juego pueden sobrescribir el archivo o añadir cadenas nuevas; revisa este repositorio después de cada actualización.

## Uso con Smart Citizen (opcional)

[Smart Citizen](https://github.com/Osiris-DevWorks/smart-citizen) es una aplicación independiente para gestionar la localización del juego. Si ya la utilizas, selecciona español en **Configuración → Idioma** y, en **Asignar archivo de idioma** (Map Language File), asigna a Spanish la URL directa de nuestro archivo:

```text
https://raw.githubusercontent.com/Siouxzepol/traduccion-BP-star-citizen-espanol/main/global.ini
```

Usa esta dirección del `global.ini`, no la del ZIP de la versión. Smart Citizen guarda la descarga en caché por idioma y su cuadro de configuración indica que solo vuelve a obtenerla si cambia la fuente; publicar cambios en esta misma URL no garantiza una actualización automática. Tras una actualización de Star Citizen, su documentación indica repetir **Extraer desde Data.p4k** y después **Aplicar mejoras**. Smart Citizen no crea por sí mismo nuevas traducciones ni actualiza este repositorio.

## Datos de misiones

Los títulos de misión incluyen `[BP]` si todas las variantes identificadas ofrecen planos y `[REP n]` si todas comparten la misma recompensa de reputación de facción. Las descripciones de ciertas misiones incluyen más detalles de sus recompensas. Los planos de un grupo pueden ser aleatorios; no se garantiza que se entreguen todos. El [catálogo completo de recompensas por contrato](datos/misiones_reputacion_planos.json) y el [catálogo de componentes de nave](datos/componentes_nave.json) sirven también como referencias complementarias. Consulta [cómo leer y actualizar los catálogos](datos/README.md).

## Créditos

Autor y responsable de la traducción: **Sioux_Atreides**  
Clan: **La Colmena**

Este proyecto es comunitario y no está afiliado a Cloud Imperium Games ni a Roberts Space Industries. Star Citizen y sus marcas pertenecen a sus respectivos titulares.
