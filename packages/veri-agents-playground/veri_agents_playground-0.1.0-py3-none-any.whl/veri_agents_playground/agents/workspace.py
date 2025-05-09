"""Workspace definitions. Workspaces organize workflows and knowledgebases. """

import logging

from veri_agents_playground.schema.schema import WorkspaceMetadata

log = logging.getLogger(__name__)

class Workspace:
    """A workspace is a collection of workflows and knowledgebases.
    """

    def __init__(
        self,
        name: str,
        description: str,
    ):
        self._metadata = WorkspaceMetadata(name=name, description=description)

    @property
    def metadata(self):
        """Get the metadata for the workspace."""
        return self._metadata
