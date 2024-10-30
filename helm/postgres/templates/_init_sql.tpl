{{/* Generate script to init database */}}
{{- define "init_sql" -}}
{{- $uniqueDatabases := dict -}}
{{- range .Values.users }}
  {{- range .databases }}
    {{- $_ := set $uniqueDatabases . true -}}
  {{- end }}
{{- end }}

{{- range $db, $_ := $uniqueDatabases }}
\c {{ $db }};
CREATE EXTENSION IF NOT EXISTS vector SCHEMA public;
{{- end }}

{{- end -}}
