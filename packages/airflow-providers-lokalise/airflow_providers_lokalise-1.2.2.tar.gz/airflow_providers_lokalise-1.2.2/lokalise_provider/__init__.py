__version__ = "1.2.2"

## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features.
def get_provider_info():
    return {
        "package-name": "airflow-providers-lokalise",  # Required
        "name": "Lokalise",  # Required
        "description": "Lokalise hook and operator for Airflow based on the Lokalise Python SDK.",  # Required
        "connection-types": [
            {
                "connection-type": "lokalise",
                "hook-class-name": "lokalise_provider.hooks.lokalise.LokaliseHook",
            }
        ],
        "versions": [__version__],  # Required
    }
