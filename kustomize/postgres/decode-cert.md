# Decoding TLS Certificates from Kubernetes Secret

This document provides step-by-step instructions to extract and decode the contents of certificates and private keys from a Kubernetes secret.

## Secret Overview
The Kubernetes secret `hippo-tls` in the namespace `postgres-operator` contains the following data:

- **ca.crt**: Certificate Authority's certificate
- **tls.crt**: Server's certificate
- **tls.key**: Server's private key

### Steps to Decode the Certificate and Key

### 1. Get the Secret Data
Run the following command to view the raw Base64-encoded data:
```bash
kubectl get secret hippo-tls -n postgres-operator -o jsonpath='{.data}'
```

Output example:
```json
{"ca.crt":"<Base64_String>","tls.crt":"<Base64_String>","tls.key":"<Base64_String>"}
```

### 2. Extract and Decode the Data
Use the following commands to decode each part of the secret:

#### Decode `ca.crt` (CA Certificate):
```bash
kubectl get secret hippo-tls -n postgres-operator -o jsonpath='{.data.ca\.crt}' | base64 -d > ca.crt
```

#### Decode `tls.crt` (Server Certificate):
```bash
kubectl get secret hippo-tls -n postgres-operator -o jsonpath='{.data.tls\.crt}' | base64 -d > tls.crt
```

#### Decode `tls.key` (Server Private Key):
```bash
kubectl get secret hippo-tls -n postgres-operator -o jsonpath='{.data.tls\.key}' | base64 -d > tls.key
```

### 3. View the Decoded Contents
After decoding, you can view the contents of the files using the following commands:

#### View `ca.crt`:
```bash
cat ca.crt
```

#### View `tls.crt`:
```bash
cat tls.crt
```

#### View `tls.key`:
```bash
cat tls.key
```

### Example Outputs

#### `ca.crt` (Certificate Authority Certificate):
```
-----BEGIN CERTIFICATE-----
[Base64 encoded certificate]
-----END CERTIFICATE-----
```

#### `tls.crt` (Server Certificate):
```
-----BEGIN CERTIFICATE-----
[Base64 encoded certificate]
-----END CERTIFICATE-----
```

#### `tls.key` (Server Private Key):
```
-----BEGIN PRIVATE KEY-----
[Base64 encoded private key]
-----END PRIVATE KEY-----
```

### 4. Verify the Decoded Files
You can use the `openssl` tool to verify the decoded files:

#### Verify the Certificate:
```bash
openssl x509 -in tls.crt -text -noout
```

#### Verify the Private Key:
```bash
openssl rsa -in tls.key -check
```

### Use Cases
- The decoded files (`ca.crt`, `tls.crt`, and `tls.key`) can now be used for:
  - Configuring TLS for `pgBouncer` or `PostgreSQL`.
  - Testing and debugging certificate and key configurations.

By following these steps, you can successfully decode and retrieve the contents of your certificates and private key from the Kubernetes secret.