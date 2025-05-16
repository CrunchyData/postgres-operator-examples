{{/* Generate script to init database */}}
{{- define "init_sql" -}}
{{- $dbUserMap := dict -}}
{{- range .Values.users }}
  {{- $user := .name }}
  {{- range .databases }}
    {{- $db := . }}
    {{- if not (hasKey $dbUserMap $db) }}
      {{- $_ := set $dbUserMap $db (list $user) }}
    {{- else }}
      {{- $_ := set $dbUserMap $db (append (get $dbUserMap $db) $user) }}
    {{- end }}
  {{- end }}
{{- end }}

{{- range $db, $users := $dbUserMap }}
\c {{ $db }};
CREATE EXTENSION IF NOT EXISTS vector SCHEMA public;
{{- range $users }}
GRANT USAGE, CREATE ON SCHEMA public TO {{ . }};
CREATE SCHEMA IF NOT EXISTS {{ . }};
GRANT ALL ON SCHEMA {{ . }} TO {{ . }};
{{- end }}
{{- end }}

{{- end -}}
