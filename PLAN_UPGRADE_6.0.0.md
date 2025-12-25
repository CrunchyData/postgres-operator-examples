# Plan aktualizacji PGO do wersji 6.0.0

Poniższy plan opisuje kroki niezbędne do aktualizacji operatora Crunchy Data Postgres Operator (PGO) z wersji 5.8.3 do 6.0.0.

## 1. Przygotowanie i Backup
*   **Backup danych**: Upewnij się, że wszystkie klastry Postgres mają aktualne backupy (pgBackRest).
*   **Backup manifestów**: Zrób kopię obecnego katalogu `postgres-operator`.
    ```bash
    cp -r postgres-operator postgres-operator-backup
    ```

## 2. Pobranie nowych manifestów (Installer 6.0.0)
Ponieważ dokładne tagi obrazów (np. suffixy buildów) zmieniają się z każdą wersją, najlepiej pobrać oficjalny pakiet instalacyjny dla wersji 6.0.0 z portalu Crunchy Data lub repozytorium GitHub (jeśli dostępne publicznie).

*   Pobierz archiwum lub sklonuj repozytorium dla wersji 6.0.0.
*   Zlokalizuj katalog `kustomize/install`.

## 3. Aktualizacja CRD (Custom Resource Definitions)
Aktualizacja definicji zasobów jest krytyczna przed aktualizacją samego operatora.

1.  Podmień pliki w katalogu `kustomize/install/crd` na te z wersji 6.0.0.
2.  Zastosuj nowe CRD (użyj `--server-side` aby uniknąć problemów z wielkością obiektów):
    ```bash
    kubectl apply --server-side -k kustomize/install/crd
    ```

## 4. Aktualizacja obrazów i konfiguracji Managera
1.  **Obrazy**: Zaktualizuj plik `kustomize/install/components/images-by-tag/kustomization.yaml`.
    *   Znajdź sekcję `images`.
    *   Podmień tagi na te odpowiadające wersji 6.0.0 (z pobranego installera).
    *   Przykład (wartości orientacyjne, sprawdź dokładne tagi!):
        *   `postgres-operator`: `ubi9-6.0.0-0`
        *   `crunchy-pgbackrest`: `ubi9-2.56.0-<suffix>`
        *   `crunchy-postgres-17`: `ubi9-17.x-<suffix>`
2.  **Manager**: Sprawdź czy plik `kustomize/install/manager/manager.yaml` wymaga zmian w zmiennych środowiskowych (np. nowe flagi feature gates).

## 5. Aplikacja zmian (Upgrade Operatora)
Po zaktualizowaniu plików lokalnych, wdróż zmiany na klaster.

```bash
# Jeśli używasz domyślnej ścieżki instalacji
kubectl apply -k kustomize/install/default
```

## 6. Weryfikacja
1.  Sprawdź czy pod PGO zrestartował się i działa poprawnie:
    ```bash
    kubectl -n postgres-operator get pods
    kubectl -n postgres-operator logs -l postgres-operator.crunchydata.com/control-plane=postgres-operator
    ```
2.  Operator 6.0.0 powinien automatycznie przejąć kontrolę nad istniejącymi klastrami.
3.  Jeśli planujesz upgrade wersji samego Postgresa (np. 16 -> 17), wykonaj to dopiero po upewnieniu się, że PGO 6.0.0 działa stabilnie.

## Uwagi
*   Upewnij się, że masz odpowiednie uprawnienia do klastra.
*   Wersja 6.0.0 może wprowadzać zmiany w CRD, które są niekompatybilne wstecz (breaking changes), dlatego krok 3 jest kluczowy.
