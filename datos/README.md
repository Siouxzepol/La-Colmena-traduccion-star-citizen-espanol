# Catálogo de recompensas de contratos

`misiones_reputacion_planos.json` recoge los contratos que tienen configurada reputación o una recompensa de planos en el DataCore analizado. Los títulos y contratistas se incluyen en español e inglés cuando existe una cadena localizada; los identificadores originales se conservan para poder contrastarlos con el juego. El script `../herramientas/integrar_recompensas_misiones.py` añade `[BP]` y `[REP n]` a los títulos de misión cuando la recompensa indicada es común a todas las variantes que comparten el título. También añade recompensas a ciertas descripciones cuando el identificador del título se puede vincular a una descripción y todos los contratos que comparten esa clave tienen las mismas recompensas. Las claves ambiguas se omiten para no mostrar información incorrecta.

`componentes_nave.json` contiene componentes de nave con nombre localizado, categoría, tamaño, grado, masa y los flujos de recursos que declara el juego (por ejemplo, consumo eléctrico o producción de refrigerante, escudos o energía).

## Cómo interpretar los datos

- `reputacion[].cantidad` es la cantidad configurada en los registros del juego para el resultado satisfactorio seleccionado. Puede haber más de una entrada por contrato y se conserva el ámbito mediante su ID de localización.
- `planos[]` indica una recompensa que apunta a un grupo (`pool`). `opciones` enumera los planos incluidos en ese grupo, su peso relativo y el objeto asociado cuando el juego lo declara. Son opciones del grupo, no una promesa de que se entreguen todas.
- Los identificadores de naves, objetos, contratos y planos se mantienen tal como aparecen en los datos del juego; no se traducen nombres propios.
- El catálogo es una instantánea de datos de juego; la integración en `global.ini` es texto estático y no puede consultar el contrato activo en tiempo real. Solo se muestran las recompensas de claves asociables sin ambigüedad. Los parches pueden cambiar contratos y recompensas.

## Regeneración

El script de `../herramientas/extraer_datos_misiones.py` recibe el directorio JSON de DataCore extraído, además de los `global.ini` inglés y español:

```powershell
python herramientas/extraer_datos_misiones.py <DataCore-json> <english/global.ini> <publicacion/global.ini> datos/misiones_reputacion_planos.json
python herramientas/integrar_recompensas_misiones.py datos/misiones_reputacion_planos.json publicacion/global.ini
python herramientas/extraer_datos_componentes.py <DataCore-json> <english/global.ini> <publicacion/global.ini> datos/componentes_nave.json
```

Los registros se pueden extraer de `Data.p4k` con [StarBreaker](https://github.com/diogotr7/StarBreaker). No se redistribuyen aquí los archivos originales del juego, solo el catálogo derivado.
