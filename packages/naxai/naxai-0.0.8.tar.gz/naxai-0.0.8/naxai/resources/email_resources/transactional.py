from naxai.models.email.send_transactional_email_model import SendTransactionalEmailModel

class TransactionalResource:
    """ transactional resource for email resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.headers = {"Content-Type": "application/json"}
            
    def send(self, data: SendTransactionalEmailModel):
        """
        Send a transactional email.

        Args:
            data (SendTransactionalEmailModel): The email data containing recipient, 
                sender, subject, content and other optional parameters

        Returns:
            dict: The API response containing the sent email details

        Example:
            >>> email_data = SendTransactionalEmailModel(
            ...     sender={},
            ...     to=[{}],
            ...     subject="Your Order Confirmation",
            ...     html="<html>Your order has been confirmed.</html>"
            ... )
            >>> response = client.email.transactional.send(data=email_data)

        Note:
            The email content can be provided in HTML format using html_content
            or in plain text using text_content. At least one content type must be provided.
        """
        return self._client._request("POST", self.root_path + "/send", json=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)

            
