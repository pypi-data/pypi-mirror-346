import logging

logger = logging.getLogger(__name__)

from prompt_poet.template_loaders import (
    TemplateLoader,
    LocalFSTemplateLoader,
    LocalPackageTemplateLoader,
    CacheLoader,
)


class LiteTemplateLoader(TemplateLoader):
    """Renamed TemplateLoader from prompt_poet with no modifications."""

    pass


class LiteLocalFSTemplateLoader(LiteTemplateLoader, LocalFSTemplateLoader):
    """Renamed LocalFSTemplateLoader from prompt_poet with no modifications."""

    pass


class LiteLocalPackageTemplateLoader(LiteTemplateLoader, LocalPackageTemplateLoader):
    """Renamed LocalPackageTemplateLoader from prompt_poet with no modifications."""

    pass


class LiteCacheLoader(LiteTemplateLoader, CacheLoader):
    """Renamed CacheLoader from prompt_poet with no modifications."""

    pass
