from __future__ import annotations

import enum
import typing as t

from pydantic import ConfigDict, Field

from apolo_app_types.protocols.common import (
    AbstractAppFieldType,
    AppInputs,
    AppOutputs,
    Preset,
    SchemaExtraMetadata,
    SchemaMetaType,
)
from apolo_app_types.protocols.postgres import (
    BasePostgresUserCredentials,
    CrunchyPostgresUserCredentials,
    PGBackupConfig,
    PGBouncer,
    PostgresConfig,
)


POSTGRES_ADMIN_DEFAULT_USER_NAME = "postgres"


class PostgresSupportedVersions(enum.StrEnum):
    v12 = "12"
    v13 = "13"
    v14 = "14"
    v15 = "15"
    v16 = "16"


POSTGRES_RESOURCES_PATTERN = r"^[a-z0-9]([-a-z0-9]*[a-z0-9])?$"


class PostgresInputs(AppInputs):
    preset: Preset
    postgres_config: PostgresConfig
    pg_bouncer: PGBouncer
    backup: PGBackupConfig | None = None


class PostgresAdminUser(BasePostgresUserCredentials):
    model_config = ConfigDict(
        protected_namespaces=(),
        json_schema_extra=SchemaExtraMetadata(
            title="Postgres Admin User",
            description="Configuration for the Postgres admin user.",
            meta_type=SchemaMetaType.INTEGRATION,
        ).as_json_schema_extra(),
    )
    user_type: t.Literal["admin"] = "admin"


class PostgresUsers(AbstractAppFieldType):
    postgres_admin_user: PostgresAdminUser | None = Field(
        default=None,
        json_schema_extra=SchemaExtraMetadata(
            title="Postgres Admin User",
            description="Admin user for the Postgres instance.",
        ).as_json_schema_extra(),
    )
    users: list[CrunchyPostgresUserCredentials] = Field(
        default_factory=list,
        json_schema_extra=SchemaExtraMetadata(
            title="Postgres Users",
            description="List of Postgres users with their credentials.",
        ).as_json_schema_extra(),
    )


class PostgresOutputs(AppOutputs):
    postgres_users: PostgresUsers | None = None
