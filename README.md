# Rework Rate Benchmark

Este proyecto contiene un script de Bash diseñado para analizar y calcular el porcentaje de "rework" (trabajo repetido o retrabajo) en un repositorio Git. El objetivo es identificar cuántas líneas de código han sido modificadas más de dos veces en un período determinado.

### ¿Qué hace este script?

El script examina los commits realizados en un repositorio Git dentro de un rango de fechas y calcula dos métricas principales:

1. **Rework Changes**: El número de veces que un archivo ha sido modificado más de dos veces.
2. **Rework Percentage**: El porcentaje de líneas modificadas que corresponden a cambios de rework (modificaciones repetidas).

Además, guarda detalles específicos de estos cambios, tales como:
- Archivos modificados.
- Las líneas específicas modificadas más de dos veces.
- Los commits donde ocurrieron estas modificaciones.

### Requisitos

- **Git**: El script depende de Git para acceder al historial de commits y las diferencias de archivos.
- **Bash**: El script está escrito en Bash y debe ejecutarse en un entorno que soporte Bash (como Git Bash o un terminal de Linux/Mac).

### ¿Cómo usar el script?

#### Paso 1: Clonar el repositorio

Primero, clona el repositorio que contiene el script:

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
