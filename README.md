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
```

#### Paso 2: Ejecutar el script en Windows
Para ejecutar el script en un entorno Windows, puedes usar Git Bash, que es una terminal Bash proporcionada por Git para Windows. Si no tienes Git Bash, puedes descargarlo desde aquí.

Una vez que tengas Git Bash instalado, sigue estos pasos:
```bash
./nombre_del_script.sh
```
**Nota: Asegúrate de que el script tenga permisos de ejecución. Si no, puedes otorgarlos con el siguiente comando: **

```bash
chmod +x nombre_del_script.sh
```

#### Paso 3: Configurar el rango de fechas y archivos excluidos
Puedes configurar el script para que analice un rango de fechas específico y excluya archivos no deseados, como el CHANGELOG.md o package.json. Modifica las variables en la parte superior del script según tus necesidades.

Archivos generados
El script generará tres archivos:

- rework_changes.txt: Detalles generales de los cambios de rework, incluyendo los archivos modificados y las líneas que han sido modificadas más de dos veces.

- specific_rework_changes.txt: Detalles específicos de los cambios de rework, mostrando el commit exacto y las líneas modificadas.

- rework_percentage.txt: El porcentaje de líneas modificadas que corresponden a rework.

#### ¿Por qué es importante este benchmark?
El Rework Rate Benchmark es útil para medir el nivel de retrabajo en un proyecto. El retrabajo puede ser costoso y a menudo indica problemas en el proceso de desarrollo, como una mala planificación, especificaciones incompletas o errores de diseño. Este script te ayuda a identificar áreas del código que han sido modificadas repetidamente, lo que puede ser una señal de que se necesita una mejora en la calidad del código o en los procesos de desarrollo.


## ¿Cómo instalar y correr? 

Primero instala las librerias necesarias:
```sh
pip install -r requirements.txt
```

Enciende el servidor de uvicorn:
```sh
uvicorn main:app --reload
```

Puedes visitar swagger el la siguiente liga:

http://127.0.0.1:8000/docs#
