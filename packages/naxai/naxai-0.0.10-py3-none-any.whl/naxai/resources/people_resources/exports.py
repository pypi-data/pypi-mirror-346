import json
from naxai.models.people.helper_models.search_condition import SearchCondition
from naxai.models.people.responses.exports_responses import (ListExportsResponse,
                                                             GetExportResponse,
                                                             GetExportDownloadUrlResponse,
                                                             CreateExportResponse)

class ExportsResource:
    """ exports resource for people resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/exports"
        self.headers = {"Content-Type": "application/json"}

    def list(self):
        """
        Retrieve a list of export jobs from the Naxai People API.
        
        This method fetches all export jobs in your account, allowing you to view
        and track the status of current and past exports.
        
        Returns:
            ListExportsResponse: A response object containing the list of export jobs.
                The response behaves like a list and can be iterated over.
        
        Raises:
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access exports.
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                try:
                    # List all export jobs
                    exports = client.people.exports.list()
                    
                    print(f"Found {len(exports)} export jobs")
                    
                    # Group exports by state
                    pending_exports = []
                    completed_exports = []
                    failed_exports = []
                    
                    for export in exports:
                        if export.state == "pending":
                            pending_exports.append(export)
                        elif export.state == "done":
                            completed_exports.append(export)
                        elif export.state == "failed":
                            failed_exports.append(export)
                    
                    # Display export statistics
                    print(f"Pending exports: {len(pending_exports)}")
                    print(f"Completed exports: {len(completed_exports)}")
                    print(f"Failed exports: {len(failed_exports)}")
                    
                    # Display details of the most recent exports
                    if exports:
                        print("\nRecent exports:")
                        for i, export in enumerate(exports[:5]):  # Show up to 5 most recent exports
                            state_emoji = "⏳" if export.state == "pending" else "✅" if export.state == "done" else "❌"
                            rows_info = f", {export.rows} rows" if export.rows else ""
                            print(f"{i+1}. {state_emoji} {export.export} export ({export.id}): {export.state}{rows_info}")
                            
                            # For completed exports, show how to get the download URL
                            if export.state == "done":
                                print(f"   To download: client.people.exports.get_download_url('{export.id}')")
                    
                except Exception as e:
                    print(f"Error listing exports: {str(e)}")
            ```
        
        Note:
            - Export jobs are typically listed in reverse chronological order (newest first)
            - The response is list-like and supports operations like len(), indexing, and iteration
            - Export jobs can be in one of three states: "pending", "done", or "failed"
            - For exports in the "done" state, you can retrieve the download URL using the
            get_download_url method
            - Export files are typically available for a limited time after completion
        """
        return ListExportsResponse.model_validate_json(json.dumps(self._client._request("GET", self.root_path, headers=self.headers)))

    def create(self, condition: SearchCondition):
        """
        Create a new export job in the Naxai People API.
        
        This method initiates an export of contacts that match the specified search condition.
        The export is processed asynchronously, and the response provides a preview of the
        contacts that will be included.
        
        Args:
            condition (SearchCondition): The search condition that defines which contacts
                to include in the export. This should be a SearchCondition object with
                the appropriate filters.
        
        Returns:
            CreateExportResponse: A response object containing pagination information and
                a preview of contacts that will be included in the export.
        
        Raises:
            ValueError: If condition is invalid.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to create exports.
            NaxaiInvalidRequestError: If the request contains invalid data.
        
        Example:
            ```python
            from naxai.models.people.helper_models.search_condition import SearchCondition
            
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                try:
                    # Create a search condition for active US customers
                    condition = SearchCondition(
                        all=[
                            {"attribute": {"field": "country", "operator": "eq", "value": "US"}},
                            {"attribute": {"field": "status", "operator": "eq", "value": "active"}}
                        ]
                    )
                    
                    # Create an export job
                    response = client.people.exports.create(condition=condition)
                    
                    # Display information about the export
                    print(f"Export job created for {response.pagination.total_items} contacts")
                    print(f"Preview of first {len(response.contacts)} contacts:")
                    
                    for contact in response.contacts:
                        print(f"- {contact.email or 'No email'} (ID: {contact.nx_id})")
                    
                    # In a real application, you would need to get the export ID
                    # from headers or other response metadata
                    # Then poll for status until the export is complete
                    
                    # Example of checking export status (assuming you have the export ID)
                    # export_id = "exp_123abc"  # This would come from the response headers
                    # export_status = client.people.exports.get(export_id=export_id)
                    # print(f"Export status: {export_status.state}")
                    
                except Exception as e:
                    print(f"Error creating export: {str(e)}")
            ```
        
        Note:
            - Export jobs are processed asynchronously and may take time to complete
            - The response provides a preview of contacts and pagination information
            - The export ID may need to be extracted from response headers or metadata
            - After creating an export, you should periodically check its status using the get method
            - Once the export is complete (state="done"), you can retrieve the download URL
            - Large exports may take significant time to process depending on the amount of data
            - The exported file format is typically CSV for contacts exports
        """
        return CreateExportResponse.model_validate_json(json.dumps(self._client._request("POST", self.root_path, json=condition.model_dump(by_alias=True, exclude_none=True), headers=self.headers)))

    def get(self, export_id: str):
        """
        Retrieve information about a specific export job in the Naxai People API.
        
        This method fetches the current status and details of an export job, allowing you
        to check if it's complete and ready for download.
        
        Args:
            export_id (str): The unique identifier of the export job to retrieve.
        
        Returns:
            GetExportResponse: A response object containing detailed information about the export job.
        
        Raises:
            ValueError: If export_id is empty.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access export information.
            NaxaiResourceNotFound: If the specified export job does not exist.
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                try:
                    # Get information about a specific export job
                    export_id = "exp_123abc"
                    export = client.people.exports.get(export_id=export_id)
                    
                    # Display export information
                    print(f"Export job: {export.id}")
                    print(f"Type: {export.export}")
                    print(f"State: {export.state}")
                    
                    # Check if the export is ready for download
                    if export.state == "done" and not export.failed:
                        print(f"Export is complete with {export.rows} rows")
                        print("Getting download URL...")
                        
                        # Get the download URL
                        download_response = client.people.exports.get_download_url(export_id=export_id)
                        print(f"Download URL: {download_response.url}")
                        
                        # In a real application, you might download the file
                        # import requests
                        # r = requests.get(download_response.url)
                        # with open("exported_contacts.csv", "wb") as f:
                        #     f.write(r.content)
                        # print("File downloaded successfully")
                        
                    elif export.state == "pending":
                        print("Export is still being processed. Check again later.")
                        
                        # In a real application, you might implement polling
                        # import asyncio
                        # print("Waiting 10 seconds...")
                        # await asyncio.sleep(10)
                        # export = client.people.exports.get(export_id=export_id)
                        # print(f"Updated state: {export.state}")
                        
                    elif export.failed or export.state == "failed":
                        print("Export failed.")
                    
                except Exception as e:
                    print(f"Error retrieving export: {str(e)}")
            ```
        
        Note:
            - Use this method to check the status of an export job before attempting to download it
            - Export jobs may take time to complete, especially for large datasets
            - The state field indicates the current status: "pending", "done", or "failed"
            - For exports in the "done" state, the rows field indicates the number of records
            - Once an export job is in the "done" state, you can retrieve its download URL
            using the get_download_url method
            - Export files are typically available for a limited time after completion
        """
        return GetExportResponse.model_validate_json(json.dumps(self._client._request("GET", self.root_path + "/" + export_id, headers=self.headers)))

    def get_download_url(self, export_id: str):
        """
        Retrieve the download URL for a completed export job in the Naxai People API.
        
        This method fetches a temporary URL that can be used to download the exported data file.
        The export job must be in the "done" state for this method to succeed.
        
        Args:
            export_id (str): The unique identifier of the completed export job.
        
        Returns:
            GetExportDownloadUrlResponse: A response object containing the temporary download URL.
        
        Raises:
            ValueError: If export_id is empty.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access export information.
            NaxaiResourceNotFound: If the specified export job does not exist.
            NaxaiInvalidRequestError: If the export job is not in the "done" state.
        
        Example:
            ```python
            import aiohttp
            import aiofiles
            
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                try:
                    # First, check if the export is complete
                    export_id = "exp_123abc"
                    export = client.people.exports.get(export_id=export_id)
                    
                    if export.state != "done" or export.failed:
                        print(f"Export is not ready for download. Current state: {export.state}")
                        if export.failed:
                            print("Export failed.")
                        else:
                            print("Export is still being processed. Try again later.")
                    else:
                        # Get the download URL
                        download_response = client.people.exports.get_download_url(export_id=export_id)
                        print(f"Download URL obtained: {download_response.url}")
                        
                        # Download the file asynchronously
                        print(f"Downloading export with {export.rows} contacts...")
                        
                        # Using aiohttp for asynchronous download
                        async with aiohttp.ClientSession() as session:
                            async with session.get(download_response.url) as response:
                                if response.status == 200:
                                    # Save the file
                                    filename = f"contacts_export_{export_id}.csv"
                                    async with aiofiles.open(filename, 'wb') as f:
                                        await f.write(await response.read())
                                    print(f"File downloaded successfully as {filename}")
                                else:
                                    print(f"Download failed with status {response.status}")
                    
                except Exception as e:
                    print(f"Error getting download URL: {str(e)}")
            ```
        
        Note:
            - This method should only be called for exports in the "done" state
            - Always check the export's state using the get method before requesting the download URL
            - The download URL is temporary and will expire after a certain period
            - The exported file format is typically CSV for contacts exports
            - Large exports may take significant time to download depending on your connection
            - For very large files, consider implementing chunked downloading or streaming
            - In production applications, you might want to implement retry logic for downloads
        """
        return GetExportDownloadUrlResponse.model_validate_json(json.dumps(self._client._request("GET", self.root_path + "/" + export_id + "/download", headers=self.headers)))