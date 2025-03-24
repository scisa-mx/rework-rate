#!/bin/bash

# Variables
OUTPUT_CHANGES="rework_changes.txt"
OUTPUT_SPECIFIC="specific_rework_changes.txt"
OUTPUT_PERCENTAGE="rework_percentage.txt"
EXCLUDED_FILES="CHANGELOG.md package.json Directory.Build.targets"
DAYS=21

# Validar si el script se ejecuta en un repositorio Git
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    echo "Este script debe ejecutarse dentro de un repositorio Git."
    exit 1
fi

# Obtener el rango de commits de los últimos 80 días
START_DATE=$(date -d "-${DAYS} days" +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)
COMMITS=$(git rev-list --since="$START_DATE" --until="$END_DATE" HEAD)

if [ -z "$COMMITS" ]; then
    echo "No hay commits en los últimos $DAYS días."
    echo "0" > "$OUTPUT_PERCENTAGE"
    echo "" > "$OUTPUT_CHANGES"
    echo "" > "$OUTPUT_SPECIFIC"
    exit 0
fi

# Archivos excluidos
EXCLUDE_PATTERN=$(printf "|%s" $EXCLUDED_FILES)
EXCLUDE_PATTERN="${EXCLUDE_PATTERN:1}"

# Inicializar contadores
total_changes=0
rework_changes=0

# Inicializar un archivo vacío para los cambios específicos
echo "Detalles específicos de los cambios de rework:" > "$OUTPUT_SPECIFIC"
echo "Detalles generales de los cambios de rework:" > "$OUTPUT_CHANGES"

# Analizar las modificaciones en los últimos 80 días
declare -A file_change_count

for commit in $COMMITS; do
    # Obtener los archivos modificados en el commit, excluyendo los archivos especificados
    modified_files=$(git diff-tree --no-commit-id --name-only -r "$commit" | grep -Ev "$EXCLUDE_PATTERN")

    for file in $modified_files; do
        total_changes=$((total_changes + 1))

        # Incrementar el contador de cambios por archivo
        file_change_count["$file"]=$((file_change_count["$file"] + 1))

        # Registrar cambios específicos de rework si el archivo ya ha sido modificado más de dos veces
        if [ ${file_change_count["$file"]} -gt 2 ]; then
            echo "Rework specific detected: Commit $commit on file $file" >> "$OUTPUT_SPECIFIC"
            rework_changes=$((rework_changes + 1))
        fi
    done
done

# Calcular el porcentaje de rework
if [ $total_changes -eq 0 ]; then
    rework_percentage=0
else
    rework_percentage=$(awk "BEGIN {printf \"%.2f\", ($rework_changes/$total_changes)*100}")
fi

# Guardar el porcentaje de rework en el archivo
echo "$rework_percentage" > "$OUTPUT_PERCENTAGE"

echo "Cálculo completado."
echo "Detalles generales escritos en: $OUTPUT_CHANGES"
echo "Cambios específicos escritos en: $OUTPUT_SPECIFIC"
echo "Porcentaje de rework escrito en: $OUTPUT_PERCENTAGE"
