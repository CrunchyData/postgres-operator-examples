{{/* Allow for GCS secret information to be stored in a Secret */}}
{{- define "postgres.gcs" }}
[global]
{{- if .gcs }}
repo{{ add .index 1 }}-gcs-key=/etc/pgbackrest/conf.d/gcs-key.json
{{- end }}
{{ end }}
