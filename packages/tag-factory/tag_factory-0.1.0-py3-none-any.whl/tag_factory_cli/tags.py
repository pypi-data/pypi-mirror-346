"""
Tag-related functionality for Tag Factory CLI.
"""
from tag_factory_cli.utils.api import APIClient
from tag_factory_cli.utils.config import Config


class TagManager:
    """Manager for tag operations."""

    def __init__(self, api_client=None):
        """Initialize tag manager.
        
        Args:
            api_client: API client instance. If None, creates new client.
        """
        self.api_client = api_client or APIClient()

    def list_tags(self, workspace_id):
        """List tags in workspace.
        
        Args:
            workspace_id: Workspace ID
            
        Returns:
            List of tags
        """
        path = f"/workspaces/{workspace_id}/tags"
        return self.api_client.get(path)

    def get_tag(self, tag_id):
        """Get tag details.
        
        Args:
            tag_id: Tag ID
            
        Returns:
            Tag details
        """
        path = f"/tags/{tag_id}"
        return self.api_client.get(path)

    def create_tag(self, workspace_id, name, description=None):
        """Create new tag.
        
        Args:
            workspace_id: Workspace ID
            name: Tag name
            description: Tag description
            
        Returns:
            Created tag
        """
        path = f"/workspaces/{workspace_id}/tags"
        data = {
            "name": name,
            "description": description,
        }
        return self.api_client.post(path, data)
