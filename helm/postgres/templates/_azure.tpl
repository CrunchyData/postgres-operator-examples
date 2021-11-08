{{/* Allow for Azure secret information to be stored in a Secret */}}
{{- define "postgres.azure" }}
[global]
{{- if .azure }}
  {{- if .azure.account }}
repo{{ add .index 1 }}-azure-account={{ .azure.account }}
  {{- end }}
  {{- if .azure.key }}
repo{{ add .index 1 }}-azure-key={{ .azure.key }}
  {{- end }}
{{- end }}
{{ end }}
