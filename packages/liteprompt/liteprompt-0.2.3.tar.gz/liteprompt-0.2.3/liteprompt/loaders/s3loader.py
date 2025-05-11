import os
import logging
import boto3
from .base import LiteTemplateLoader, LiteCacheLoader
from jinja2 import Environment, TemplateNotFound
from typing import Optional

logger = logging.getLogger(__name__)

S3_TEMPLATE_LOADER_PREFIX = "s3://"


class LiteS3TemplateLoader(LiteTemplateLoader):
    """Template loader for loading templates from Amazon S3."""

    def __init__(
        self,
        bucket_name: str,
        template_path: str,
        s3_client: Optional[boto3.client] = None,
    ):
        self._bucket_name = bucket_name
        self._template_dir, self._template_name = self._parse_template_path(
            template_path
        )

        self._s3_client = s3_client or boto3.client("s3")

        self._mapping = {}
        self._generation_data = {}

    @staticmethod
    def _parse_template_path(template_path: str) -> tuple:
        """Helper function to parse the template path."""
        template_dir, template_name = os.path.split(template_path)
        if not template_dir:
            template_dir = "."
        return template_dir, template_name

    def _is_stale(self, key: str) -> bool:
        """Check if the template needs to be downloaded."""
        local_generation = self._generation_data.get(key)
        head_object = self._s3_client.head_object(Bucket=self._bucket_name, Key=key)
        return local_generation != head_object["VersionId"]

    def _download(self):
        """Download templates from S3 to local memory."""
        logger.info(f"Downloading templates from S3 bucket: {self._bucket_name}")

        objects = self._s3_client.list_objects_v2(
            Bucket=self._bucket_name, Prefix=self._template_dir
        )

        for obj in objects.get("Contents", []):
            key = obj["Key"]
            if key.endswith("/"):
                continue

            if not key.endswith((".yml.j2", ".yaml.j2", ".yml.jinja2", ".yaml.jinja2")):
                logger.warning(f"Skipping non-YAML Jinja2 file: {key}")
                continue

            if self._is_stale(key):
                logger.info(f"Downloading {key} from S3")
                response = self._s3_client.get_object(Bucket=self._bucket_name, Key=key)
                self._mapping[key] = response["Body"].read().decode("utf-8")
                self._generation_data[key] = obj["VersionId"]

    def load(self) -> Environment:
        """Load the template from the S3 bucket."""
        try:
            self._download()
            loader = LiteCacheLoader(mapping=self._mapping)
            env = Environment(loader=loader, auto_reload=False)
            template = env.get_template(self._template_name)
            return template
        except TemplateNotFound as ex:
            raise TemplateNotFound(
                f"Template not found: {ex} {self._template_name=} {self._template_dir=}"
            )
        except Exception as ex:
            logger.error(f"Error loading template from S3: {ex}")
            raise Exception(f"Error while loading template: {ex}")

    def id(self) -> str:
        """Generate a unique identifier for the S3 template loader."""
        return f"{S3_TEMPLATE_LOADER_PREFIX}{self._bucket_name}/{self._template_dir}/{self._template_name}"
