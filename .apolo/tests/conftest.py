import base64
from unittest.mock import MagicMock, patch

import pytest


pytest_plugins = [
    "apolo_app_types_fixtures.apolo_clients",
]


def encode_b64(value: str) -> str:
    """Helper function to encode a string in Base64."""
    return base64.b64encode(value.encode()).decode()


@pytest.fixture
def mock_kubernetes_client():
    with (
        patch("kubernetes.config.load_config") as mock_load_config,
        patch("kubernetes.config.load_incluster_config") as mock_load_incluster_config,
        patch("kubernetes.client.CoreV1Api") as mock_core_v1_api,
        patch("kubernetes.client.NetworkingV1Api") as mock_networking_v1_api,
        patch("kubernetes.client.CustomObjectsApi") as mock_custom_objects_api,
        patch(
            "apolo_app_types.clients.kube.get_current_namespace"
        ) as mock_get_curr_namespace,
    ):
        # Mock CoreV1Api instance for services
        mock_v1_instance = MagicMock()
        mock_core_v1_api.return_value = mock_v1_instance

        # Mock NetworkingV1Api instance for ingresses
        mock_networking_instance = MagicMock()
        mock_networking_v1_api.return_value = mock_networking_instance
        namespace = "default-namespace"
        mock_get_curr_namespace.return_value = namespace

        def get_services_by_label(namespace, label_selector):
            return {
                "items": [
                    {
                        "metadata": {
                            "name": "app",
                            "namespace": "default-namespace",
                        },
                        "spec": {"ports": [{"port": 80}]},
                    },
                ]
            }

        mock_v1_instance.list_namespaced_service.side_effect = get_services_by_label
        user_params = {
            "password": encode_b64("supersecret"),
            "host": encode_b64("db.example.com"),
            "port": encode_b64("5432"),
            "pgbouncer-host": encode_b64("pgbouncer.example.com"),
            "pgbouncer-port": encode_b64("6432"),
            "dbname": encode_b64("mydatabase"),
            "jdbc-uri": encode_b64("jdbc:postgresql://db.example.com:5432/mydatabase"),
            "pgbouncer-jdbc-uri": encode_b64(
                "jdbc:postgresql://pgbouncer.example.com:6432/mydatabase"
            ),
            "pgbouncer-uri": encode_b64(
                "postgres://pgbouncer.example.com:6432/mydatabase"
            ),
            "uri": encode_b64("postgres://db.example.com:5432/mydatabase"),
        }
        mock_secret = MagicMock()
        mock_secret.metadata.name = "llm-inference"
        mock_secret.metadata.namespace = "default"
        mock_secret.data = {
            "user": encode_b64("admin"),
            **user_params,
        }
        mock_postgres_secret = MagicMock()
        mock_postgres_secret.metadata.name = "llm-inference"
        mock_postgres_secret.metadata.namespace = "default"
        mock_postgres_secret.data = {
            "user": encode_b64("postgres"),
            **user_params,
        }

        # Set .items to a list containing the mocked secret
        mock_v1_instance.list_namespaced_secret.return_value.items = [
            mock_secret,
            mock_postgres_secret,
        ]

        def mock_list_namespaced_custom_object(
            group, version, namespace, plural, **kwargs
        ):
            if (
                group == "postgres-operator.crunchydata.com"
                and version == "v1beta1"
                and plural == "postgresclusters"
            ):
                return {
                    "items": [
                        {
                            "metadata": {
                                "name": "pg-test",
                            },
                            "spec": {
                                "users": [
                                    {
                                        "name": "admin",
                                        "databases": ["mydatabase", "otherdatabase"],
                                    },
                                    {
                                        "name": "postgres",
                                        "databases": ["postgres"],
                                    },
                                ]
                            },
                        }
                    ]
                }
            raise Exception("Unknown custom object")  # noqa: EM101

        mock_custom_objects_instance = MagicMock()
        mock_custom_objects_api.return_value = mock_custom_objects_instance
        mock_custom_objects_instance.list_namespaced_custom_object.side_effect = (
            mock_list_namespaced_custom_object
        )

        yield {
            "mock_load_config": mock_load_config,
            "mock_load_incluster_config": mock_load_incluster_config,
            "mock_core_v1_api": mock_core_v1_api,
            "mock_networking_v1_api": mock_networking_v1_api,
            "mock_v1_instance": mock_v1_instance,
            "mock_networking_instance": mock_networking_instance,
            "mock_custom_objects": mock_custom_objects_instance,
        }
