{{/* Allow for S3 secret information to be stored in a Secret */}}
{{- define "postgres.s3" }}
[global]
{{- if .s3 }}
  {{- if .s3.key }}
repo{{ add .index 1 }}-s3-key={{ .s3.key }}
  {{- end }}
  {{- if .s3.keySecret }}
repo{{ add .index 1 }}-s3-key-secret={{ .s3.keySecret }}
  {{- end }}
  {{- if .s3.encryptionPassphrase }}
repo{{ add .index 1 }}-cipher-pass={{ .s3.encryptionPassphrase }}
  {{- end }}
{{- end }}
{{ end }}
