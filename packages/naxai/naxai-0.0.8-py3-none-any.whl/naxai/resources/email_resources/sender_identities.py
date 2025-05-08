from typing import Optional

class SenderIdentitiesResource:
    """ sender_identities resource for email resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/senders"
        self.headers = {"Content-Type": "application/json"}
            
    #TODO: email validation
    def update(self, sender_id: str, name: str, email: str):
        """
        Updates the name of a sender identity.

        Args:
            sender_id (str): The ID of the sender identity to update.
            name (str): The new name for the sender identity.

        Returns:
            dict: The API response indicating the update status.

        Example:
            >>> response = client.email.sender_identities.update("sender123", "Johnny Tuch")
        """
        payload = {
            "name": name,
            "email": email
        }

        return self._client._request("PUT", self.root_path + "/" + sender_id, json=payload, headers=self.headers)


    def delete(self, sender_id: str):
        """
        Deletes a sender identity.

        Args:
            sender_id (str): The ID of the sender identity to delete.

        Returns:
            dict: The API response indicating the deletion status.

        Example:
            >>> response = client.email.sender_identities.delete("sender123")
        """
        return self._client._request("DELETE", self.root_path + "/" + sender_id, headers=self.headers)
            
    def get(self, sender_id: str):
        """
        Retrieves a specific sender identity.

        Args:
            sender_id (str): The ID of the sender identity to retrieve.

        Returns:
            dict: The API response containing the sender identity.

        Example:
            >>> response = client.email.sender_identities.get("sender123")
        """
        self._client.logger.debug("sender_id url: %s", self.root_path + "/" + sender_id)
        return self._client._request("GET", self.root_path + "/" + sender_id, headers=self.headers)
    
    #TODO: email validation
    def create(self, domain_id: str, email: str, name: str):
        """
        Creates a new sender identity.

        Args:
            domain_id (str): The domain ID for the sender identity.
            email (str): The email address of the sender identity.
            name (str): The name of the sender identity.

        Returns:
            dict: The API response containing the created sender identity.

        Example:
            >>> response = client.email.sender_identities.create("domain123", "sender@example.com", "Johnny Tuch")
        """
        payload = {
            "domainId": domain_id,
            "email": email,
            "name": name
        }

        return self._client._request("POST", self.root_path, json=payload, headers=self.headers)


    def list(self,
            domain_id: Optional[str] = None,
            verified: Optional[bool] = None,
            shared: Optional[bool] = None):
        """
        Retrieves a list of sender identities.

        Args:
            domain_id (str, optional): The domain ID to filter on.
            verified (bool, optional): Whether to filter on verified sender identities.
            shard (bool, optional): Whether to filter on shared sender identities.

        Returns:
            dict: The API response containing the list of sender identities.

        Example:
            >>> response = client.email.sender_identities.list()
        """
        params = {}

        if domain_id:
             params["domainId"] = domain_id
        if verified:
             params["verified"] = verified
        if shared:
             params["shared"] = shared

        return self._client._request("GET", self.root_path, params=params, headers=self.headers)
