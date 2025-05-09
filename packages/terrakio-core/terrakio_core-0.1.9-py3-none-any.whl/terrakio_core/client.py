import requests
import xarray as xr
from io import BytesIO
from typing import Dict, Any, Optional, Union
import json
from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry as ShapelyGeometry
from .exceptions import APIError, ConfigurationError

class BaseClient:
    def __init__(self, url: Optional[str] = None, key: Optional[str] = None, 
                auth_url: Optional[str] = "https://dev-au.terrak.io",
                quiet: bool = False, config_file: Optional[str] = None,
                verify: bool = True, timeout: int = 60):
        self.quiet = quiet
        self.verify = verify
        self.timeout = timeout
        self.auth_client = None
        if auth_url:
            from terrakio_core.auth import AuthClient
            self.auth_client = AuthClient(
                base_url=auth_url,
                verify=verify,
                timeout=timeout
            )
        self.url = url
        self.key = key
        if self.url is None or self.key is None:
            from terrakio_core.config import read_config_file, DEFAULT_CONFIG_FILE
            if config_file is None:
                config_file = DEFAULT_CONFIG_FILE
            try:
                config = read_config_file(config_file)
                if self.url is None:
                    self.url = config.get('url')
                if self.key is None:
                    self.key = config.get('key')
            except Exception as e:
                raise ConfigurationError(
                    f"Failed to read configuration: {e}\n\n"
                    "To fix this issue:\n"
                    "1. Create a file at ~/.terrakioapirc with:\n"
                    "url: https://api.terrak.io\n"
                    "key: your-api-key\n\n"
                    "OR\n\n"
                    "2. Initialize the client with explicit parameters:\n"
                    "client = terrakio_api.Client(\n"
                    "    url='https://api.terrak.io',\n"
                    "    key='your-api-key'\n"
                    ")"
                )
        if not self.url:
            raise ConfigurationError("Missing API URL in configuration")
        if not self.key:
            raise ConfigurationError("Missing API key in configuration")
        self.url = self.url.rstrip('/')
        if not self.quiet:
            print(f"Using Terrakio API at: {self.url}")
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'x-api-key': self.key
        })
        self.user_management = None
        self.dataset_management = None

    def validate_feature(self, feature: Dict[str, Any]) -> None:
        if hasattr(feature, 'is_valid'):
            from shapely.geometry import mapping
            feature = {
                "type": "Feature",
                "geometry": mapping(feature),
                "properties": {}
            }
        if not isinstance(feature, dict):
            raise ValueError("Feature must be a dictionary or a Shapely geometry")
        if feature.get("type") != "Feature":
            raise ValueError("GeoJSON object must be of type 'Feature'")
        if "geometry" not in feature:
            raise ValueError("Feature must contain a 'geometry' field")
        if "properties" not in feature:
            raise ValueError("Feature must contain a 'properties' field")
        try:
            geometry = shape(feature["geometry"])
        except Exception as e:
            raise ValueError(f"Invalid geometry format: {str(e)}")
        if not geometry.is_valid:
            raise ValueError(f"Invalid geometry: {geometry.is_valid_reason}")
        geom_type = feature["geometry"]["type"]
        if geom_type == "Point":
            if len(feature["geometry"]["coordinates"]) != 2:
                raise ValueError("Point must have exactly 2 coordinates")
        elif geom_type == "Polygon":
            if not geometry.is_simple:
                raise ValueError("Polygon must be simple (not self-intersecting)")
            if geometry.area == 0:
                raise ValueError("Polygon must have non-zero area")
            coords = feature["geometry"]["coordinates"][0]
            if coords[0] != coords[-1]:
                raise ValueError("Polygon must be closed (first and last points must match)")

    def signup(self, email: str, password: str) -> Dict[str, Any]:
        if not self.auth_client:
            raise ConfigurationError("Authentication client not initialized. Please provide auth_url during client initialization.")
        return self.auth_client.signup(email, password)

    def login(self, email: str, password: str) -> str:
        if not self.auth_client:
            raise ConfigurationError("Authentication client not initialized. Please provide auth_url during client initialization.")
        token = self.auth_client.login(email, password)
        if not self.quiet:
            print(f"Successfully authenticated as: {email}")
        return token

    def refresh_api_key(self) -> str:
        if not self.auth_client:
            raise ConfigurationError("Authentication client not initialized. Please provide auth_url during client initialization.")
        if not self.auth_client.token:
            raise ConfigurationError("Not authenticated. Call login() first.")
        self.key = self.auth_client.refresh_api_key()
        self.session.headers.update({'x-api-key': self.key})
        import os
        config_path = os.path.join(os.environ.get("HOME", ""), ".tkio_config.json")
        try:
            config = {"EMAIL": "", "TERRAKIO_API_KEY": ""}
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
            config["TERRAKIO_API_KEY"] = self.key
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            if not self.quiet:
                print(f"API key generated successfully and updated in {config_path}")
        except Exception as e:
            if not self.quiet:
                print(f"Warning: Failed to update config file: {e}")
        return self.key

    def view_api_key(self) -> str:
        if not self.auth_client:
            raise ConfigurationError("Authentication client not initialized. Please provide auth_url during client initialization.")
        if not self.auth_client.token:
            raise ConfigurationError("Not authenticated. Call login() first.")
        self.key = self.auth_client.view_api_key()
        self.session.headers.update({'x-api-key': self.key})
        return self.key

    def get_user_info(self) -> Dict[str, Any]:
        if not self.auth_client:
            raise ConfigurationError("Authentication client not initialized. Please provide auth_url during client initialization.")
        if not self.auth_client.token:
            raise ConfigurationError("Not authenticated. Call login() first.")
        return self.auth_client.get_user_info()

    def wcs(self, expr: str, feature: Union[Dict[str, Any], ShapelyGeometry], in_crs: str = "epsg:4326",
            out_crs: str = "epsg:4326", output: str = "csv", resolution: int = -1,
            **kwargs):
        if hasattr(feature, 'is_valid'):
            from shapely.geometry import mapping
            feature = {
                "type": "Feature",
                "geometry": mapping(feature),
                "properties": {}
            }
        self.validate_feature(feature)
        payload = {
            "feature": feature,
            "in_crs": in_crs,
            "out_crs": out_crs,
            "output": output,
            "resolution": resolution,
            "expr": expr,
            **kwargs
        }
        if not self.quiet:
            print(f"Requesting data with expression: {expr}")
        request_url = f"{self.url}/wcs"
        try:
            response = self.session.post(request_url, json=payload, timeout=self.timeout, verify=self.verify)
            if not response.ok:
                error_msg = f"API request failed: {response.status_code} {response.reason}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg += f" - {error_data['detail']}"
                except:
                    pass
                raise APIError(error_msg)
            if output.lower() == "csv":
                import pandas as pd
                return pd.read_csv(BytesIO(response.content))
            elif output.lower() == "netcdf":
                return xr.open_dataset(BytesIO(response.content))
            else:
                try:
                    return xr.open_dataset(BytesIO(response.content))
                except ValueError:
                    import pandas as pd
                    try:
                        return pd.read_csv(BytesIO(response.content))
                    except:
                        return response.content
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    # Admin/protected methods
    def _get_user_by_id(self, user_id: str):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.get_user_by_id(user_id)

    def _get_user_by_email(self, email: str):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.get_user_by_email(email)

    def _list_users(self, substring: str = None, uid: bool = False):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.list_users(substring=substring, uid=uid)

    def _edit_user(self, user_id: str, uid: str = None, email: str = None, role: str = None, apiKey: str = None, groups: list = None, quota: int = None):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.edit_user(
            user_id=user_id,
            uid=uid,
            email=email,
            role=role,
            apiKey=apiKey,
            groups=groups,
            quota=quota
        )

    def _reset_quota(self, email: str, quota: int = None):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.reset_quota(email=email, quota=quota)

    def _delete_user(self, uid: str):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.delete_user(uid=uid)

    # Dataset management protected methods
    def _get_dataset(self, name: str, collection: str = "terrakio-datasets"):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.get_dataset(name=name, collection=collection)

    def _list_datasets(self, substring: str = None, collection: str = "terrakio-datasets"):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.list_datasets(substring=substring, collection=collection)

    def _create_dataset(self, name: str, collection: str = "terrakio-datasets", **kwargs):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.create_dataset(name=name, collection=collection, **kwargs)

    def _update_dataset(self, name: str, append: bool = True, collection: str = "terrakio-datasets", **kwargs):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.update_dataset(name=name, append=append, collection=collection, **kwargs)

    def _overwrite_dataset(self, name: str, collection: str = "terrakio-datasets", **kwargs):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.overwrite_dataset(name=name, collection=collection, **kwargs)

    def _delete_dataset(self, name: str, collection: str = "terrakio-datasets"):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.delete_dataset(name=name, collection=collection)

    def close(self):
        self.session.close()
        if self.auth_client:
            self.auth_client.session.close()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
