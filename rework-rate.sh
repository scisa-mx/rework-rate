#!/bin/bash

# Variables
OUTPUT_CHANGES="rework_changes.txt"
OUTPUT_SPECIFIC="specific_rework_changes.txt"
OUTPUT_PERCENTAGE="rework_percentage.txt"
EXCLUDED_FILES="azure-pipelines.yml CHANGELOG.md appsettings.json appsettings.*.json \ bin/ obj/ \*.csproj *.sln \wwwroot/ \Migrations/ \*.g.cs *.g.i.cs \*.designer.cs \*.razor.g.cs *.dll"
DAYS=21

rm -f "$OUTPUT_CHANGES" "$OUTPUT_SPECIFIC" "$OUTPUT_PERCENTAGE"

# Validar si el script se ejecuta en un repositorio Git
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    echo "Este script debe ejecutarse dentro de un repositorio Git."
    exit 1
fi

# Obtener el rango de commits de los últimos X días
START_DATE=$(date -d "-${DAYS} days" +%Y-%m-%dT00:00:00Z)
END_DATE=$(date +%Y-%m-%dT23:59:59Z)
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
total_lines=0
rework_lines=0
total_files=0
total_commits=0

# Inicializar un archivo vacío para los cambios específicos
echo "Detalles específicos de los cambios de rework:" > "$OUTPUT_SPECIFIC"
echo "Detalles generales de los cambios de rework:" > "$OUTPUT_CHANGES"

# Analizar las modificaciones en los últimos 80 días
declare -A file_change_count
declare -A file_modified_lines

for commit in $COMMITS; do
    total_commits=$((total_commits + 1))

    # Obtener los archivos modificados en el commit, excluyendo los archivos especificados
    modified_files=$(git diff-tree --no-commit-id --name-only -r "$commit" | grep -Ev "$EXCLUDE_PATTERN")

    for file in $modified_files; do
        total_changes=$((total_changes + 1))

        # Contar líneas agregadas y modificadas
        lines_changed=$(git diff --numstat "$commit^" "$commit" -- "$file" | awk '{sum += $1 + $2} END {print sum}')
        total_lines=$((total_lines + lines_changed))

        # Obtener las líneas específicas modificadas con el commit correspondiente
        modified_lines=$(git diff "$commit^" "$commit" -- "$file" | grep -E "^\-" | grep -Ev "^\+\+\+" | grep -Ev "^---" | sed "s/^/Commit $commit: /")

        # Incrementar el contador de cambios por archivo
        file_change_count["$file"]=$((file_change_count["$file"] + 1))
        file_modified_lines["$file"]+=$'\n'"$modified_lines"

        # Registrar cambios específicos de rework si el archivo ya ha sido modificado más de dos veces
        if [ ${file_change_count["$file"]} -ge 2 ]; then
            echo "Rework specific detected: Commit $commit on file $file" >> "$OUTPUT_SPECIFIC"
            echo "File: $file" >> "$OUTPUT_CHANGES"
            echo "Lines Modified More Than Twice:" >> "$OUTPUT_CHANGES"
            echo "$modified_lines" >> "$OUTPUT_CHANGES"
            echo "-------------------------------------" >> "$OUTPUT_CHANGES"
            rework_changes=$((rework_changes + 1))
            rework_lines=$((rework_lines + $(echo "$modified_lines" | wc -l)))
        fi
    done
done

# Calcular el porcentaje de rework
if [ $total_lines -eq 0 ]; then
    rework_percentage=0
else
    rework_percentage=$(awk "BEGIN {printf \"%.2f\", ($rework_lines/$total_lines)*100}")
fi

# Guardar el porcentaje de rework en el archivo
echo "Resumen del análisis de Rework:" >> "$OUTPUT_PERCENTAGE"
echo "---------------------------------" >> "$OUTPUT_PERCENTAGE"
echo "REWORK %$rework_percentage" >> "$OUTPUT_PERCENTAGE"
echo "Total de commits procesados: $total_commits" >> "$OUTPUT_PERCENTAGE"
echo "Total de líneas modificadas: $total_lines" >> "$OUTPUT_PERCENTAGE"
echo "Total de líneas de rework (modificadas más de dos veces): $rework_lines" >> "$OUTPUT_PERCENTAGE"

echo "Cálculo completado."
echo "Detalles generales escritos en: $OUTPUT_CHANGES"
echo "Cambios específicos escritos en: $OUTPUT_SPECIFIC"
echo "Porcentaje de rework escrito en: $OUTPUT_PERCENTAGE"

# Obtener información del repositorio y PR
REPO_URL=$(git config --get remote.origin.url)

# Obtener información del PR actual
MESSAGE=$(git log -1 --pretty=%B)
if [[ "$MESSAGE" =~ Merged\ PR\ ([0-9]+) ]]; then
    PR_NUMBER="${BASH_REMATCH[1]}"
else
    echo "No merged PR found."
    PR_NUMBER="N/A"
fi

AUTHOR=$(git log -1 --pretty=%an || echo "N/A")
APPROVER=$(git log -1 --pretty=%cn || echo "N/A")

# Hacer la llamada a la API
echo "Enviando datos a la API..."

# Escapar caracteres especiales en las variables
AUTHOR=$(echo "$AUTHOR" | sed 's/\\/\\\\/g')
REPO_URL=$(echo "$REPO_URL" | sed 's/\\/\\\\/g')

# Construcción del payload GraphQL
graphql_query=$(cat <<EOF
{
  "query": "mutation CreateReworkData(\$data: ReworkDataInput!) { createReworkData(data: \$data) { id repoUrl prNumber author } }",
  "variables": {
    "data": {
      "repoUrl": "$REPO_URL",
      "prNumber": "$PR_NUMBER",
      "author": "$AUTHOR",
      "prApprover": "$APPROVER",
      "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
      "totalCommits": $total_commits,
      "periodStart": "$START_DATE",
      "periodEnd": "$END_DATE",
      "modifiedLines": $total_lines,
      "reworkLines": $rework_lines,
      "reworkPercentage": $rework_percentage
    }
  }
}
EOF
)

# Mostrar el JSON para verificación
echo "Enviando a GraphQL:"
echo "$graphql_query"

# Enviar la petición al endpoint GraphQL
curl -X POST https://api.rework-rate.scisa.com.mx/graphql \
    -H "Content-Type: application/json" \
    --data-raw "$graphql_query"
