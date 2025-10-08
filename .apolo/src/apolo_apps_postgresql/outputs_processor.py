import asyncio
import base64
import logging
import typing as t

from apolo_app_types import (
    CrunchyPostgresUserCredentials,
)
from apolo_app_types.clients.kube import get_crd_objects, get_secret
from apolo_app_types.outputs.base import BaseAppOutputsProcessor
from apolo_app_types.protocols.postgres import PostgresURI

from .types import PostgresAdminUser, PostgresOutputs, PostgresUsers


logger = logging.getLogger()

MAX_SLEEP_SEC = 10
POSTGRES_ADMIN_USERNAME = "postgres"


def get_postgres_cluster_users(app_instance_id: str) -> dict[str, t.Any]:
    pg_clusters = get_crd_objects(
        api_group="postgres-operator.crunchydata.com",
        api_version="v1beta1",
        crd_plural_name="postgresclusters",
        label_selector=f"argocd.argoproj.io/instance={app_instance_id}",
    )
    assert len(pg_clusters["items"]) == 1, "Expected exactly one Postgres cluster"
    pg_cluster = pg_clusters["items"][0]
    users = pg_cluster["spec"].get("users", [])
    return {user["name"]: user for user in users}


def postgres_creds_from_kube_secret_data(
    secret_data: dict[str, str],
) -> CrunchyPostgresUserCredentials:
    T = t.TypeVar("T", str, str | None)

    def _b64decode(s: T) -> T:
        if not isinstance(s, str):
            return s
        return base64.b64decode(s).decode()

    user = _b64decode(secret_data["user"])
    password = _b64decode(secret_data["password"])
    host = _b64decode(secret_data["host"])
    port = _b64decode(secret_data["port"])
    pgbouncer_host = _b64decode(secret_data["pgbouncer-host"])
    pgbouncer_port = _b64decode(secret_data["pgbouncer-port"])
    dbname = _b64decode(secret_data.get("dbname"))

    postgres_conn_string = (
        f"postgresql://{user}:{password}@{pgbouncer_host}:{pgbouncer_port}/{dbname}"
    )

    return CrunchyPostgresUserCredentials(
        user=user,
        password=password,
        host=host,
        port=int(port),
        pgbouncer_host=pgbouncer_host,
        pgbouncer_port=int(pgbouncer_port),
        dbname=dbname,
        jdbc_uri=_b64decode(secret_data.get("jdbc-uri")),
        pgbouncer_jdbc_uri=_b64decode(secret_data.get("pgbouncer-jdbc-uri")),
        pgbouncer_uri=_b64decode(secret_data.get("pgbouncer-uri")),
        uri=_b64decode(secret_data.get("uri")),
        postgres_uri=PostgresURI(uri=postgres_conn_string),
    )


async def get_postgres_outputs(
    helm_values: dict[str, t.Any],
    app_instance_id: str,
) -> dict[str, t.Any]:
    for trial in range(1, MAX_SLEEP_SEC):
        logger.info("Trying to get postgres outputs")  # noqa: T201
        secrets = await get_secret(
            label="postgres-operator.crunchydata.com/role=pguser"
        )
        if secrets:
            logger.info("Secrets found")  # noqa: T201
            break
        logger.info(  # noqa: T201
            "Failed to get postgres outputs, retrying in %s seconds", trial
        )
        await asyncio.sleep(trial)
    else:
        msg = "Failed to get postgres outputs"
        raise Exception(msg)

    requested_users = get_postgres_cluster_users(
        app_instance_id=app_instance_id,
    )
    users = []
    admin_user = None

    for item in secrets.items:
        user = postgres_creds_from_kube_secret_data(item.data)
        if user.user == POSTGRES_ADMIN_USERNAME:
            admin_user = user
            continue
        users.append(user)
        # currently, postgres operator does not create all combinations of
        # user <> database accesses, we need to expand this
        requested_dbs = requested_users.get(user.user, {}).get("databases", [])
        for db in requested_dbs:
            if user.dbname == db:
                continue
            users.append(user.with_database(db))
    if admin_user:
        admin = PostgresAdminUser(
            **{**admin_user.model_dump(exclude={"dbname"}), "user_type": "admin"}
        )
    else:
        admin = None
    return PostgresOutputs(
        postgres_users=PostgresUsers(
            users=users,
            postgres_admin_user=admin,
        ),
    ).model_dump()


class PostgresOutputsProcessor(BaseAppOutputsProcessor[PostgresOutputs]):
    async def _generate_outputs(
        self,
        helm_values: dict[str, t.Any],
        app_instance_id: str,
    ) -> PostgresOutputs:
        psql_outputs = await get_postgres_outputs(helm_values, app_instance_id)
        return PostgresOutputs.model_validate(psql_outputs)
