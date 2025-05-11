import os
import sys
import types


def raise_install_error(lib, item=None):
    target = f"{lib}.{item}" if item else lib
    raise ImportError(
        f"'{target}' is required but not installed. Please run:\n    pip install {lib}"
    )


try:
    from cachetools import LRUCache
except ImportError:

    def fake_LRUCache(*args, **kwargs):
        raise_install_error("cachetools", "LRUCache")

    sys.modules["cachetools"] = types.SimpleNamespace(LRUCache=fake_LRUCache)

try:
    from tiktoken import get_encoding, Encoding
except ImportError:

    class FakeEncoding:
        def __getattr__(self, name):
            raise_install_error("tiktoken", "Encoding")

    def fake_get_encoding(name):
        raise_install_error("tiktoken", "get_encoding")

    sys.modules["tiktoken"] = types.SimpleNamespace(
        get_encoding=fake_get_encoding, Encoding=FakeEncoding()
    )

try:
    from google.cloud import storage
except ImportError:

    class FakeStorage:
        class Client:
            def __init__(self):
                pass

            def some_method(self):
                pass

        class Blob:
            def __init__(self):
                pass

            def some_method(self):
                pass

        def __getattr__(self, name):
            raise_install_error("google-cloud-storage", f"google.cloud.storage.{name}")

    fake_storage = FakeStorage()
    google_ns = types.SimpleNamespace()
    cloud_ns = types.SimpleNamespace(storage=fake_storage)
    google_ns.cloud = cloud_ns

    sys.modules["google"] = google_ns
    sys.modules["google.cloud"] = cloud_ns
    sys.modules["google.cloud.storage"] = fake_storage

package_path = os.path.abspath(os.path.dirname(__file__))
if package_path not in sys.path:
    sys.path.insert(0, package_path)

from liteprompt.prompt import (
    LitePrompt,
    LitePromptPart,
    LiteTruncationBlock,
    LiteTemplate,
)
from liteprompt.exceptions import LitePromptError, LiteTruncationError
from liteprompt.registry import LiteTemplateRegistry

__all__ = [
    "LitePrompt",
    "LitePromptPart",
    "LiteTruncationBlock",
    "LiteTruncationBlock",
    "LitePromptError",
    "LiteTemplate",
    "LiteTruncationError",
    "LiteTemplateRegistry",
    "LiteTruncationError",
]
