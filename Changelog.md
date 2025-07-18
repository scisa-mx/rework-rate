# SCISA Benchmarks API

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