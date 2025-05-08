from naxai.models.email.send_transactional_email_model import SendTransactionalEmailModel

class TransactionalResource:
    """ transactional resource for email resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.headers = {"Content-Type": "application/json"}
            
    async def send(self, data: SendTransactionalEmailModel):
          """Send a transactional email"""
          return await self._client._request("POST", self.root_path + "/send", json=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)

            
