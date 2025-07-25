# SCISA Benchmarks API


## 0.5.0 - 16/07/2025
Se agregan etiquetas a los repositorios, filtros más avanzados para el historial de rework, y se mejora la validación al actualizar etiquetas.

### Added
- [] Se agregan relaciones entre repositorios y etiquetas.
- [] Se expone una mutación para crear etiquetas y otra para asignarlas a un repositorio.
- [] Se agrega filtrado por nombre y etiquetas en la consulta del historial de rework.
- [] Se agrega validación de color hexadecimal al actualizar una etiqueta.

### Fixed
- [] Ahora se puede cambiar el color de una etiqueta sin necesidad de modificar su nombre.
- [] Se corrige un bug donde los repositorios sin etiquetas generaban errores en el filtrado.
- [] Mejor manejo de errores cuando se intenta crear o actualizar una etiqueta con un nombre duplicado.

### Changed
- [] Refactor del TagService y separación de lógica de validación en colors.py.
- [] Se actualiza la lógica de actualización de etiquetas para evitar validaciones innecesarias si no hay cambios en el nombre.

### Deprecated


### Removed


### Security

## 0.4.0 - 18/07/2025
### Resumen
Se mejora la API para manejar mejor los repositorios y se agrega un nuevo campo para el historial de rework. 

### Fixed
- [] Se corrige el manejo de errores al buscar repositorios por ID.
- [] Se arregla el formato de las fechas en las respuestas de la API.

### Added
- [] Se agrega un nuevo campo `createdAtDate` en el historial de re
work para distinguir entre el lapso del rework y la fecha de creación del reporte.

### Changed
- [] Se mejora la documentación de la API para mayor claridad en el uso de los endpoints.



## 0.3.1 - 09/05/2025

### Resumen
Se agrega un campo nuevo para poder dicernir entre el lapso del rework y cuando se creo el reporte. 
Se añade tambien mejoras para el docker.

### Fixed
    - [220] Ahora al devoler el historico del rework se hace mediante el lapso del tiempo en el que se hizo el reporte, y no el lapso de tiempo del análisis.
    - [220] Se arregla formato de fechas para las peticiones.

### Added
    - [220] Se agrega un campo nuevo llamado createdAtDate como punto de partida del reporte.

### Changed
//
### Deprecated
//
### Removed
//
### Security
//

## 0.2.0-rc - 04/25/257

### Resumen
Se agregan facilidades para manejar la API y que los usuarios puedan eliminar repositorios mediante su url.

### Fixed
    - [101] El usuario puede buscar los historiales mediante fechas.

### Added
    - [199] Se agrega una mutación para eliminar los repositorios mediante una url. 

### Changed
    - [198] Se agrega un mejor sistema de logs para informar de nuevas inserciones a la base de datos.

### Deprecated

### Removed

### Security