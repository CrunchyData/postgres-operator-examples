import base64
import logging
import typing as t

import apolo_sdk

from apolo_app_types.helm.apps.base import BaseChartValueProcessor
from apolo_app_types.helm.apps.common import (
    get_preset,
    preset_to_affinity,
    preset_to_resources,
    preset_to_tolerations,
)
from apolo_app_types.helm.utils.buckets import get_or_create_bucket_credentials
from apolo_app_types.helm.utils.deep_merging import merge_list_of_dicts
from apolo_app_types.protocols.postgres import PostgresDBUser, PostgresInputs


logger = logging.getLogger(__name__)

POSTGRESQL_CRD_NAME_MAX_LENGTH = 37


class PostgresInputsChartValueProcessor(BaseChartValueProcessor[PostgresInputs]):
    def __init__(self, *args: t.Any, **kwargs: t.Any):
        super().__init__(*args, **kwargs)

    async def gen_extra_helm_args(self, *_: t.Any) -> list[str]:
        return ["--timeout", "30m"]

    async def _gen_instances_config(
        self,
        instance_preset_name: str,
        instance_replicas: int,
        instances_size: int,
    ) -> list[dict[str, t.Any]]:
        preset = get_preset(self.client, instance_preset_name)
        resources = preset_to_resources(preset)
        tolerations = await preset_to_tolerations(preset)
        affinity = preset_to_affinity(preset)

        pod_anti_afinity = {
            "preferredDuringSchedulingIgnoredDuringExecution": [
                {
                    "weight": 100,
                    "podAffinityTerm": {
                        "topologyKey": "kubernetes.io/hostname",
                        "labelSelector": {
                            "matchExpressions": [
                                {
                                    "key": "platform.apolo.us/component",
                                    "operator": "In",
                                    "values": ["app"],
                                },
                                {
                                    "key": "platform.apolo.us/app",
                                    "operator": "In",
                                    "values": ["crunchypostgresql"],
                                },
                            ]
                        },
                    },
                }
            ]
        }
        affinity["podAntiAffinity"] = pod_anti_afinity

        instance = {
            "name": "instance1",
            "metadata": {
                "labels": {
                    "platform.apolo.us/component": "app",
                    "platform.apolo.us/app": "crunchypostgresql",
                    "platform.apolo.us/preset": instance_preset_name,
                },
            },
            "replicas": int(instance_replicas),
            "dataVolumeClaimSpec": {
                "accessModes": ["ReadWriteOnce"],
                "resources": {"requests": {"storage": f"{instances_size}Gi"}},
            },
            "resources": resources,
            "tolerations": tolerations,
            "affinity": affinity,
        }
        return [instance]

    def _create_users_config(
        self, db_users: list[PostgresDBUser]
    ) -> list[dict[str, t.Any]]:
        # Set user[].password to "AlphaNumeric" since often non-alphanumberic
        # characters break client libs :(
        users_config: list[dict[str, t.Any]] = [{"name": "postgres"}]
        for db_user in db_users:
            users_config.append(
                {
                    "name": db_user.name,
                    "password": {"type": "AlphaNumeric"},
                    "databases": db_user.db_names,
                }
            )
        return users_config

    async def _get_bouncer_config(
        self,
        bouncer_preset_name: str,
        bouncer_repicas: int,
    ) -> dict[str, t.Any]:
        preset = get_preset(self.client, bouncer_preset_name)
        resources = preset_to_resources(preset)
        tolerations = await preset_to_tolerations(preset)
        affinity = preset_to_affinity(preset)
        pod_anti_afinity = {
            "preferredDuringSchedulingIgnoredDuringExecution": [
                {
                    "weight": 100,
                    "podAffinityTerm": {
                        "topologyKey": "kubernetes.io/hostname",
                        "labelSelector": {
                            "matchExpressions": [
                                {
                                    "key": "platform.apolo.us/component",
                                    "operator": "In",
                                    "values": ["app"],
                                },
                                {
                                    "key": "platform.apolo.us/app",
                                    "operator": "In",
                                    "values": ["crunchypostgresql"],
                                },
                            ]
                        },
                    },
                }
            ]
        }

        affinity["podAntiAffinity"] = pod_anti_afinity

        return {
            "affinity": affinity,
            "metadata": {
                "labels": {
                    "platform.apolo.us/component": "app",
                    "platform.apolo.us/app": "crunchypostgresql",
                    "platform.apolo.us/preset": bouncer_preset_name,
                },
            },
            "replicas": bouncer_repicas,
            "resources": resources,
            "tolerations": tolerations,
        }

    async def _get_backup_config(
        self, input_: PostgresInputs, app_name: str
    ) -> dict[str, t.Any]:
        if not input_.backup or not input_.backup.enable:
            return {}

        name = f"app-pg-backup-{app_name}"

        bucket_credentials = await get_or_create_bucket_credentials(
            client=self.client,
            bucket_name=name,
            credentials_name=name,
            supported_providers=[
                apolo_sdk.Bucket.Provider.AWS,
                apolo_sdk.Bucket.Provider.MINIO,
                apolo_sdk.Bucket.Provider.GCP,
            ],
        )

        provider = bucket_credentials.credentials[0].provider
        credentials = bucket_credentials.credentials[0].credentials

        values = {}
        if provider in (apolo_sdk.Bucket.Provider.AWS, apolo_sdk.Bucket.Provider.MINIO):
            values["s3"] = {
                "bucket": credentials["bucket_name"],
                "endpoint": credentials["endpoint_url"],
                "region": credentials["region_name"],
                "key": credentials["access_key_id"],
                "keySecret": credentials["secret_access_key"],
            }
        elif provider == apolo_sdk.Bucket.Provider.GCP:
            values["gcs"] = {
                "bucket": credentials["bucket_name"],
                "key": base64.b64decode(credentials["key_data"]).decode("utf-8"),
            }
        # For Azure, we need to return a bit more data from API
        else:
            # For Azure, we need to return a bit more data from API
            # OpenStack is not supported in PGO yet
            error = "Unsupported bucket provider, unable configure backups"
            raise ValueError(error)
        return values

    async def gen_extra_values(
        self,
        input_: PostgresInputs,
        app_name: str,
        namespace: str,
        app_id: str,
        app_secrets_name: str,
        *_: t.Any,
        **kwargs: t.Any,
    ) -> dict[str, t.Any]:
        """
        Generate extra Helm values for postgres configuration.
        """
        instances = await self._gen_instances_config(
            instance_preset_name=input_.preset.name,
            instance_replicas=input_.postgres_config.instance_replicas,
            instances_size=input_.postgres_config.instance_size,
        )

        bouncer_preset_name = input_.pg_bouncer.preset.name
        pgbouncer_config = {}
        if bouncer_preset_name:
            pgbouncer_config = await self._get_bouncer_config(
                bouncer_preset_name=bouncer_preset_name,
                bouncer_repicas=int(input_.pg_bouncer.replicas),
            )

        postgrescluster_crd_name = f"pg-{app_id}"
        if len(postgrescluster_crd_name) > POSTGRESQL_CRD_NAME_MAX_LENGTH:
            postgrescluster_crd_name = postgrescluster_crd_name[
                :POSTGRESQL_CRD_NAME_MAX_LENGTH
            ]

        values: dict[str, t.Any] = {
            "metadata": {"labels": {"platform.apolo.us/component": "app"}},
            "features": {
                "AutoCreateUserSchema": "true",
            },
            # empirically measured, postgrescluster crd name is limited to 37 chars
            # otherwise it will fail to create STSs and other resources
            "name": postgrescluster_crd_name,
            "postgresVersion": input_.postgres_config.postgres_version.value,
            "databaseInitSQL": {
                "name": f"{postgrescluster_crd_name}-init-sql",
                "key": "bootstrap.sql",
            },
        }
        users_config = self._create_users_config(input_.postgres_config.db_users)

        if instances:
            values["instances"] = instances
        if pgbouncer_config:
            values["pgBouncerConfig"] = pgbouncer_config
        if users_config:
            values["users"] = users_config

        backup_values = await self._get_backup_config(input_, app_name)

        return merge_list_of_dicts([backup_values, values])
