"""This module allows to connect to Lokalise."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook
from lokalise import Client as LokaliseClient


class LokaliseHook(BaseHook):
    """
    Interact with Lokalise.

    Performs a connection to Lokalise and retrieves client.

    :param lokalise_conn_id: Reference to :ref:`Lokalise connection id <howto/connection: lokalise>`.
    """

    conn_name_attr = "lokalise_conn_id"
    default_conn_name = "lokalise_default"
    conn_type = "lokalise"
    hook_name = "Lokalise"

    def __init__(
        self, lokalise_conn_id: str = default_conn_name, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.lokalise_conn_id = lokalise_conn_id
        self.client: LokaliseClient | None = None
        self.get_conn()

    def get_conn(self) -> LokaliseClient:
        """Initiate a new Github connection with API key"""
        if self.client is not None:
            return self.client

        conn = self.get_connection(self.lokalise_conn_id)
        api_key = conn.password

        if not api_key:
            raise AirflowException("An API Key is mandatory to access Lokalise")

        self.client = LokaliseClient(token=api_key)

        return self.client

    def test_connection(self) -> tuple[bool, str]:
        """Test Lokalise connection"""
        conn = self.get_connection(self.lokalise_conn_id)
        project = conn.host

        try:
            if TYPE_CHECKING:
                assert self.client
            self.client.project(project)
            return True, "Successfully connected to Lokalise."
        except Exception as exc:
            return False, str(exc)

    @staticmethod
    def get_ui_field_behaviour() -> dict[str, Any]:
        """Returns custom field behaviour"""

        return {
            "hidden_fields": ["schema", "login", "port", "extra"],
            "relabeling": {
                "host": "Lokalise Project ID",
                "password": "Lokalise API Key",
            },
        }
