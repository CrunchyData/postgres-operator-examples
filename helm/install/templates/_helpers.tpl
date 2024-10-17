{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "install.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Crunchy labels
*/}}
{{- define "install.clusterLabels" -}}
postgres-operator.crunchydata.com/control-plane: {{ .Chart.Name }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "install.labels" -}}
helm.sh/chart: {{ include "install.chart" . }}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Custom Labels
*/}}
{{- define "install.customPodLabels" -}}
{{- if .Values.customPodLabels -}}
{{ toYaml .Values.customPodLabels }}
{{- end}}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "install.serviceAccountName" -}}
{{ .Chart.Name }}
{{- end }}

{{/*
Create the name of the Role/ClusterRole to use
*/}}
{{- define "install.roleName" -}}
{{ .Chart.Name }}
{{- end }}

{{/*
Create the name of the RoleBinding/ClusterRoleBinding to use
*/}}
{{- define "install.roleBindingName" -}}
{{ .Chart.Name }}
{{- end }}

{{/*
Create the kind for rolebindings. Will be RoleBinding in single
namespace mode or ClusterRoleBinding by default.
*/}}
{{- define "install.roleBindingKind" -}}
{{- if .Values.singleNamespace -}}
RoleBinding
{{- else -}}
ClusterRoleBinding
{{- end }}
{{- end }}

{{/*
Create the kind for role. Will be Role in single
namespace mode or ClusterRole by default.
*/}}
{{- define "install.roleKind" -}}
{{- if .Values.singleNamespace -}}
Role
{{- else -}}
ClusterRole
{{- end }}
{{- end }}

{{- define "install.imagePullSecrets" -}}
{{/* Earlier versions required the full structure of PodSpec.ImagePullSecrets */}}
{{- if .Values.imagePullSecrets }}
imagePullSecrets:
{{ toYaml .Values.imagePullSecrets }}
{{- else if .Values.imagePullSecretNames }}
imagePullSecrets:
{{- range .Values.imagePullSecretNames }}
- name: {{ . | quote }}
{{- end }}{{/* range */}}
{{- end }}{{/* if */}}
{{- end }}{{/* define */}}

{{- define "install.relatedImages" -}}
{{- range $id, $object := .Values.relatedImages }}
- name: RELATED_IMAGE_{{ $id | upper }}
  value: {{ $object.image | quote }}
{{- end }}
{{- end }}


{{- define "install.defaultEnv" -}}
- name: CRUNCHY_DEBUG
  value: {{ .Values.debug | ne false | quote }}
- name: PGO_NAMESPACE
  valueFrom: { fieldRef: { apiVersion: v1, fieldPath: metadata.namespace } }
{{- if .Values.singleNamespace }}
- name: PGO_TARGET_NAMESPACE
  valueFrom: { fieldRef: { apiVersion: v1, fieldPath: metadata.namespace } }
{{- end }}
{{- if .Values.workers }}
- name: PGO_WORKERS
  value: {{ .Values.workers | quote }}
{{- end }}
{{- include "install.relatedImages" . }}
{{- if .Values.disable_check_for_upgrades }}
- name: CHECK_FOR_UPGRADES
  value: "false"
{{- end }}
{{- if .Values.features }}
{{- $value := .Values.features }}
- name: PGO_FEATURE_GATES
{{- $out := "" -}}
{{- if eq (kindOf $value) "map" -}}
{{- range $key, $val := $value -}}
  {{- $out = (print $out $key "=" $val ",") -}}
{{- end }}
{{- end }}
  value: "{{ trimSuffix "," $out }}"
{{- end }}
{{- end }}{{/* define */}}

