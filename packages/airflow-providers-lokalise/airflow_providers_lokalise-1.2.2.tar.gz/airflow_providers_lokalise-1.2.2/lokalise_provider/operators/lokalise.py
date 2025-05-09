from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from lokalise.errors import ClientError, ServerError

from lokalise_provider.hooks.lokalise import LokaliseHook

if TYPE_CHECKING:
    from airflow.utils.context import Context


class LokaliseOperator(BaseOperator):
    """
    Interact and perform actions on Lokalise API.

    This operator is designed to use Lokalise's Python Library: https://github.com/lokalise/python-lokalise-api

    :param lokalise_conn_id: Reference to a pre-defined Lokalise Connection
    :param lokalise_method: Method name from Lokalise Library to be called
    :param lokalise_method_args: Method parameters for the lokalise_method
    :param result_processor: Function to further process the response from the Lokalise API
    """

    def __init__(
        self,
        *,
        lokalise_method: str,
        lokalise_conn_id: str = "lokalise_default",
        lokalise_method_args: dict | None = None,
        result_processor: Callable | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.lokalise_conn_id = lokalise_conn_id
        self.method_name = lokalise_method
        self.lokalise_method_args = lokalise_method_args or {}
        self.result_processor = result_processor

    def execute(self, context: Context) -> Any:
        try:
            hook = LokaliseHook(lokalise_conn_id=self.lokalise_conn_id)
            resource = hook.client

            lokalise_result = getattr(resource, self.method_name)(
                **self.lokalise_method_args
            )
            if self.result_processor:
                return self.result_processor(lokalise_result)

            return lokalise_result

        except (ClientError, ServerError) as lokalise_error:
            raise AirflowException(
                f"Failed to execute LokaliseOperator, error: {lokalise_error}"
            )
        except Exception as exc:
            raise AirflowException(f"LokaliseOperator error: {exc}")
