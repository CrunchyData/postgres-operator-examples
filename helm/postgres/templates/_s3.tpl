{{/* Allow for S3 secret information to be stored in a Secret */}}
{{- define "postgres.s3" }}
[global]
{{- if .Values.s3 }}
{{- if .Values.s3.key }}
repo1-s3-key={{ .Values.s3.key }}
{{- end }}
{{- if .Values.s3.keySecret }}
repo1-s3-key-secret={{ .Values.s3.keySecret }}
{{- end }}
{{- if .Values.s3.encryptionPassphrase }}
repo1-cipher-pass={{ .Values.s3.encryptionPassphrase }}
{{- end }}
{{- end }}
{{ end }}
