import logging
from functools import lru_cache

from omegaconf import DictConfig

log = logging.getLogger(__name__)

class AuthorizationError(Exception):
    """Exception raised for authorization errors."""
    pass


class AccessControl:
    """Base class for access control."""

    def is_admin(self, user: str | None) -> bool:
        """Check if a user is an admin."""
        raise NotImplementedError

    def has_workspace_access(self, user: str | None, workspace: str) -> bool:
        """Validate if a user has access to a workspace."""
        raise NotImplementedError


class AccessControlNone(AccessControl):
    """No access control. All users have access to all workspaces."""

    def is_admin(self, user: str | None) -> bool:
        """Check if a user is an admin."""
        return True

    def has_workspace_access(self, user: str | None, workspace: str) -> bool:
        """Validate if a user has access to a workspace."""
        return True


class AccessControlConfigured(AccessControl):
    """Access control using user names defined in the configuration."""

    def __init__(self, config: DictConfig):
        self.config = config

    def is_admin(self, user: str | None) -> bool:
        """Check if a user is an admin."""
        return user is not None and is_admin(user)

    def has_workspace_access(self, user: str | None, workspace: str) -> bool:
        """Validate if a user has access to a workspace."""
        return user is not None and has_workspace_access(user, workspace, self.config)


# class AccessControlAiWARE:
#    """Access control for the system using aiWARE ACLs."""
#    TODO


def is_admin(user: str) -> bool:
    """Check if a user is an admin."""
    # TODO: here we can hook in aiWare permissions later on
    return user in [
        "mtoman@veritone.com",
        "dschabus@veritone.com",
        "tboley@veritone.com",
    ]


@lru_cache(maxsize=128)
def has_workspace_access(user: str, workspace: str, config: DictConfig) -> bool:
    """Validate if a user has access to a workspace."""
    # TODO: here we can hook in aiWare ACLs later on
    log.info("Checking workspace access for %s in %s", user, workspace)
    if workspace == "public":
        return True
    if is_admin(user):
        return True
    if workspace == "veritone" and user.endswith("@veritone.com"):
        return True
    if workspace in config.workspaces:
        return user in config.workspaces[workspace].users
    return False
