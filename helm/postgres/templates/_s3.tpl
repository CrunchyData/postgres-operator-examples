{{/* Allow for S3 secret information to be stored in a Secret */}}
{{- define "postgres.s3" }}
[global]
{{- if .s3 }}
  {{- if .s3.key }}
{{- $resolvedKey := include "mychart.resolveAwsS3Key" }}
repo{{ add .index 1 }}-s3-key={{ $$resolvedKey | b64dec}}
  {{- end }}
  {{- /* Use the helper for resolving keySecret */}}
  {{- $resolvedKeySecret := include "mychart.resolveAwsS3KeySecret" }}
repo{{ add .index 1 }}-s3-key-secret={{ $resolvedKeySecret | b64dec }}
  {{- end }}
  {{- if .s3.keyType }}
repo{{ add .index 1 }}-s3-key-type={{ .s3.keyType }}
  {{- end }}
  {{- if .s3.encryptionPassphrase }}
repo{{ add .index 1 }}-cipher-pass={{ .s3.encryptionPassphrase }}
  {{- end }}
{{- end }}
{{ end }}
