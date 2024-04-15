import typing as t
import base64
import yaml
import asyncio
from pathlib import Path
from dataclasses import dataclass, asdict

import neuro_sdk
import click


@dataclass(frozen=True)
class S3:
    bucket: str
    endpoint: str
    region: str
    key: str
    keySecret: str
    keyType: str | None = None
    encryptionPassphrase: str | None = None


@dataclass(frozen=True)
class GCS:
    bucket: str
    key: t.Mapping[str, t.Any]


@dataclass(frozen=True)
class Azure:
    account: str
    key: str
    container: str


BackupConfig = t.Union[S3, GCS, Azure]


@click.command()
@click.argument("helm_release_name")
@click.argument(
    "base_config_path", required=True, type=click.Path(exists=True, path_type=Path)
)
@click.argument("output_config_path", type=click.Path(path_type=Path))
@click.option("--cluster_name", type=str, default=None)
@click.option("--project_name", type=str, default=None)
@click.option("--org_name")
def generate(
    helm_release_name: str,
    base_config_path: Path,
    output_config_path: Path,
    cluster_name: str | None,
    project_name: str | None,
    org_name: str | None,
) -> None:

    assert base_config_path.exists()

    base_config = yaml.safe_load(base_config_path.read_text())
    click.echo("Generating backup config")
    config = asyncio.run(
        gen_backup_config(helm_release_name, cluster_name, project_name, org_name)
    )
    updated_config = {**base_config, **config}
    with output_config_path.open("w") as f:
        yaml.dump(updated_config, f)
    click.echo("Backup config generated")


async def gen_backup_config(
    helm_release_name: str,
    cluster_name: str | None = None,
    project_name: str | None = None,
    org_name: str | None = None,
) -> BackupConfig:
    bucket_name = f"{helm_release_name}-pgo-backups"
    client = await neuro_sdk.get()
    async with client:
        try:
            bucket = await client.buckets.get(
                bucket_id_or_name=bucket_name,
                cluster_name=cluster_name,
                project_name=project_name,
                org_name=org_name,
            )
            click.echo(f"Found existing bucket {bucket.name=} ({bucket.id=})")
        except neuro_sdk.ResourceNotFound:
            bucket = await client.buckets.create(
                name=bucket_name,
                cluster_name=cluster_name,
                org_name=org_name,
                project_name=project_name,
            )
            click.echo(f"Created bucket {bucket.name=} ({bucket.id=})")

        credentials_name = bucket.name
        assert credentials_name
        try:
            p_credentials = await client.buckets.persistent_credentials_get(
                credentials_name, cluster_name
            )
            click.echo(
                f"Found existing bucket credentials {p_credentials.name=} ({p_credentials.id=})"
            )
        except neuro_sdk.ResourceNotFound:
            p_credentials = await client.buckets.persistent_credentials_create(
                bucket_ids=[bucket.id],
                name=credentials_name,
                cluster_name=cluster_name,
                read_only=False,
            )

        backup_config = _parse_backup_config(bucket, p_credentials)
        config_dict = asdict(
            backup_config,
            dict_factory=lambda x: {k: v for (k, v) in x if v is not None},
        )

        if isinstance(backup_config, S3):
            return {"s3": config_dict}
        elif isinstance(backup_config, GCS):
            return {"gcs": config_dict}
        elif isinstance(backup_config, Azure):
            return {"azure": config_dict}
        else:
            raise ValueError("Unexpected backup config")


def _parse_backup_config(
    bucket: neuro_sdk.Bucket, p_credentials: neuro_sdk.PersistentBucketCredentials
) -> BackupConfig:
    if len(p_credentials.credentials) != 1:
        raise RuntimeError("Unexpected number of credentials, should be one")

    provider = p_credentials.credentials[0].provider
    credentials = p_credentials.credentials[0].credentials

    if provider in (
        neuro_sdk.Bucket.Provider.MINIO,
        neuro_sdk.Bucket.Provider.AWS,
    ):
        return S3(
            bucket=credentials["bucket_name"],
            endpoint=credentials["endpoint_url"],
            region=credentials["region_name"],
            key=credentials["access_key_id"],
            keySecret=credentials["secret_access_key"],
        )
    elif provider == neuro_sdk.Bucket.Provider.GCP:
        return GCS(
            bucket=credentials["bucket_name"],
            key=base64.b64decode(credentials["key_data"]),
        )
    else:
        # For Azure, we need to return a bit more data from API
        # OpenStack is not supported in PGO yet
        raise ValueError(f"Unsupported bucket provider: {bucket.provider}")


if __name__ == "__main__":
    generate()
