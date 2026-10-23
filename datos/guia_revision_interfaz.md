# Guía de revisión de la interfaz

Estado: 23/10/2026. Esta guía registra qué pantalla se está revisando; **«parcial» no significa que toda la sección esté terminada**. El catálogo `global.ini` contiene unas 91.000 entradas, incluidas misiones, diálogos, objetos y nombres propios. Que una cadena coincida con el original inglés no demuestra por sí solo que falte traducirla.

| Sección visible en el juego | Familias principales del catálogo | Estado | Trabajo comprobado |
| --- | --- | --- | --- |
| Cabina, HUD y avisos de vuelo | `DXSM_`, `DXSH_`, `HUD_`, `dfm_ui_`, `mfd_` | Parcial | Avisos de escudos y misiles; etiquetas de resultados y escaneo; armamento, reaparición, autodestrucción y estados de salto/acoplamiento. Revisadas las entradas `mfd_` y varias `UI_MF_`. Corregidos avisos de presión atmosférica, esclusa y fijación de misiles; distinguidos la carga y la calibración del motor cuántico. Revisadas varias categorías de escaneo, instrucciones de aterrizaje, mensajes de baliza de rescate/incapacitación y avisos de zonas legales. Primer repaso de mensajes de objetivo por fabricante; detectados errores de sentido en CNOU y Drake. Falta contrastar estas cadenas dentro del juego y continuar con el resto de fabricantes. |
| mobiGlas: contratos, diario y notificaciones | `MG_`, `mobiGlas_`, `MissionManager_`, `Notification_` | Parcial | Varias fichas de misión y textos del diario; falta revisar cada pestaña como pantalla. |
| Minería, reciclaje y carga | `HUD_`, `DXSM_`, `UI_` | Parcial | Términos SCU y algunas etiquetas vistas en capturas; falta un repaso sistemático. |
| Inventario, tiendas y refinería | `UI_`, `shop_`, `itemPort_`, `port_`, `vehicle_focus_`, `vehicle_class_`, `kiosk_` | Parcial | Algunas etiquetas de refinería. En la tienda de naves, identificado que enfoque y clase se concatenan: corregidas combinaciones duplicadas como «Transporte: Pasajeros» y «Competición: Carreras», además de varias clases que seguían en inglés o estaban mal traducidas. La pantalla inicial de Buy-&-Fly sigue mostrando «TOUCH SCREEN TO START» aunque `kiosk_TouchStart` ya está traducida tanto en el repositorio como en el archivo instalado; no se ha identificado otra cadena en `global.ini` que explique esa pantalla. Queda pendiente comprobar si ese rótulo procede de un recurso de interfaz ajeno al catálogo. Falta comprobar el resultado en el juego y revisar el resto de inventario y tiendas. |
| Menús, ajustes y controles | `UI_`, `PAUSE_`, `input_` | Parcial | Dos opciones sociales corregidas en el primer barrido; falta revisar los menús completos. |
| Interacciones, ascensores y terminales | `UI_`, `HUD_` y claves específicas | Parcial | Casos señalados en capturas; falta comprobar el resto de naves y terminales. |
| Textos de misiones y diálogos | Claves de cada personaje o facción | En curso | Battaglia revisado por bloques; Bit Zeros iniciado. Restituida en «Golpe en el espacio profundo» (Headhunters) la sección de planos posibles y detalles de misión omitidos en español; el plano está garantizado, pero el modelo concreto sale de un grupo regional. No equivale a una revisión completa de la interfaz. |

## Orden de trabajo

1. Cabina y HUD: avisos, armamento, escaneo, MFD y etiquetas de objetivos.
2. mobiGlas: inicio, contratos, diario, mapas, vehículos y reputación.
3. Minería, reciclaje y carga: mensajes contextuales y unidades.
4. Inventario, tiendas, refinería, terminales e interacciones.
5. Menús, ajustes, controles, avisos sociales y notificaciones.
6. Misiones y diálogos por facción, como revisión paralela y separada.

Para cada bloque: comparar con el inglés original, corregir solo las cadenas claras, conservar variables como `~mission(...)` y comprobar etiquetas y recompensas. Después, indicar qué se revisó, qué quedó pendiente y si los cambios siguen en local o se publicaron.

**Punto a comprobar:** varias entradas españolas llevan el sufijo `,P` en la clave y el original inglés no. No cambiarlo en masa hasta confirmar su función en el juego. Por ahora se conserva.

**Siguiente bloque:** comprobar en el juego cómo se muestran las parejas enfoque/clase de la tienda de naves y revisar las demás categorías de vehículos; después, retomar los mensajes de objetivo y combate por fabricante. Las coincidencias que quedan con el inglés incluyen nombres propios, abreviaturas, códigos y nombres de minerales que deben conservarse.
