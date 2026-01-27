{{- define "certmanager.prefix" -}}
{{- default .Release.Name .Values.name -}}
{{- end -}}
