import json
from naxai.models.people.responses.imports_responses import (GetImportResponse,
                                                             ListImportsResponse)

class ImportsResource:
    """ imports resource for people resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/imports"
        self.headers = {"Content-Type": "application/json"}

    def list(self):
        """
        Retrieve a list of import jobs from the Naxai People API.
        
        This method fetches all import jobs in your account, allowing you to view
        and track the status of current and past imports.
        
        Returns:
            ListImportsResponse: A response object containing the list of import jobs.
                The response behaves like a list and can be iterated over.
        
        Raises:
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access imports.
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                try:
                    # List all import jobs
                    imports = client.people.imports.list()
                    
                    print(f"Found {len(imports)} import jobs")
                    
                    # Group imports by state
                    imports_by_state = {}
                    for import_job in imports:
                        state = import_job.state or "unknown"
                        if state not in imports_by_state:
                            imports_by_state[state] = []
                        imports_by_state[state].append(import_job)
                    
                    # Display import statistics by state
                    for state, jobs in imports_by_state.items():
                        print(f"{state.capitalize()} imports: {len(jobs)}")
                    
                    # Display details of the most recent imports
                    if imports:
                        print("\nRecent imports:")
                        for i, import_job in enumerate(imports[:5]):  # Show up to 5 most recent imports
                            # Create a status indicator
                            if import_job.state == "imported":
                                status = f"✅ Complete ({import_job.rows_imported} rows)"
                            elif import_job.state == "importing":
                                progress = 0
                                if import_job.rows_to_import and import_job.rows_imported:
                                    progress = (import_job.rows_imported / import_job.rows_to_import) * 100
                                status = f"⏳ In progress ({progress:.1f}%)"
                            elif import_job.state == "failed":
                                status = f"❌ Failed (Reason: {import_job.failed_reason or 'Unknown'})"
                            elif import_job.state == "preparing":
                                status = "🔄 Preparing"
                            elif import_job.state == "canceled":
                                status = "⏹️ Canceled"
                            else:
                                status = "❓ Unknown state"
                            
                            # Display import information
                            print(f"{i+1}. {import_job.name} (ID: {import_job.id})")
                            print(f"   Status: {status}")
                            print(f"   Type: {import_job.type_ or 'Unknown'}, Mode: {import_job.import_mode or 'Unknown'}")
                            
                            # For imports in progress, show how to check status
                            if import_job.state in ["preparing", "importing"]:
                                print(f"   To check status: client.people.imports.get('{import_job.id}')")
                    
                except Exception as e:
                    print(f"Error listing imports: {str(e)}")
            ```
        
        Note:
            - Import jobs are typically listed in reverse chronological order (newest first)
            - The response is list-like and supports operations like len(), indexing, and iteration
            - Import jobs can be in various states: "preparing", "importing", "imported", "failed", or "canceled"
            - For imports in progress, you can track their status using the get method
            - The rows_imported and rows_to_import fields can be used to calculate progress
            - Import jobs remain in the list even after completion for historical reference
        """
        return ListImportsResponse.model_validate_json(json.dumps(self._client._request("GET", self.root_path, headers=self.headers)))

    def get(self, import_id: str):
        """
        Retrieve information about a specific import job in the Naxai People API.
        
        This method fetches the current status and details of an import job, allowing you
        to check its progress or results.
        
        Args:
            import_id (str): The unique identifier of the import job to retrieve.
        
        Returns:
            GetImportResponse: A response object containing detailed information about the import job.
        
        Raises:
            ValueError: If import_id is empty.
            NaxaiAPIRequestError: If there is an error response from the API.
            NaxaiAuthenticationError: If authentication fails.
            NaxaiAuthorizationError: If the account lacks permission to access import information.
            NaxaiResourceNotFound: If the specified import job does not exist.
        
        Example:
            ```python
            with NaxaiClient(api_client_id="your_id", api_client_secret="your_secret") as client:
                try:
                    # Get information about a specific import job
                    import_id = "imp_123abc"
                    import_job = client.people.imports.get(import_id=import_id)
                    
                    # Display basic import information
                    print(f"Import job: {import_job.name} (ID: {import_job.id})")
                    print(f"Type: {import_job.type_ or 'Unknown'}")
                    print(f"Mode: {import_job.import_mode or 'Unknown'}")
                    
                    # Check the import state and display appropriate information
                    if import_job.state == "imported":
                        print(f"Status: Complete ✅")
                        print(f"Imported {import_job.rows_imported} rows successfully")
                        
                        # If the import added contacts to a segment, display segment info
                        if import_job.segment:
                            print(f"Contacts were added to segment: {import_job.segment.segment_id}")
                        
                    elif import_job.state == "importing":
                        # Calculate and display progress
                        progress = 0
                        if import_job.rows_to_import and import_job.rows_imported:
                            progress = (import_job.rows_imported / import_job.rows_to_import) * 100
                        
                        print(f"Status: In progress ⏳ ({progress:.1f}%)")
                        print(f"Imported {import_job.rows_imported} of {import_job.rows_to_import} rows")
                        
                        # In a real application, you might implement polling
                        # import asyncio
                        # print("Waiting 10 seconds to check progress again...")
                        # await asyncio.sleep(10)
                        # updated_import = client.people.imports.get(import_id=import_id)
                        # updated_progress = (updated_import.rows_imported / updated_import.rows_to_import) * 100
                        # print(f"Updated progress: {updated_progress:.1f}%")
                        
                    elif import_job.state == "failed":
                        print(f"Status: Failed ❌")
                        print(f"Reason: {import_job.failed_reason or 'Unknown error'}")
                        
                    elif import_job.state == "preparing":
                        print(f"Status: Preparing 🔄")
                        print("The import is being prepared. Check again later.")
                        
                    elif import_job.state == "canceled":
                        print(f"Status: Canceled ⏹️")
                        
                    else:
                        print(f"Status: {import_job.state or 'Unknown'}")
                    
                    # Display file and mapping information if available
                    if import_job.file:
                        print(f"\nFile configuration:")
                        print(f"Separator: '{import_job.file.separator}'")
                    
                    if import_job.mapping:
                        print(f"\nColumn mappings:")
                        for mapping in import_job.mapping:
                            if mapping.skip:
                                print(f"- {mapping.header}: Skipped")
                            else:
                                print(f"- {mapping.header} → {mapping.attribute}")
                    
                except Exception as e:
                    print(f"Error retrieving import: {str(e)}")
            ```
        
        Note:
            - Use this method to check the status and progress of an import job
            - Import jobs may take time to complete, especially for large datasets
            - The state field indicates the current status: "preparing", "importing", "imported", "failed", or "canceled"
            - For imports in the "importing" state, the rows_imported and rows_to_import fields
            can be used to calculate progress
            - The mapping field provides information about how columns in the import file
            were mapped to attributes in Naxai
            - For failed imports, check the failed_reason field for more information
            - Import jobs remain accessible even after completion for historical reference
        """
        return GetImportResponse.model_validate_json(json.dumps(self._client._request("GET", self.root_path + "/" + import_id, headers=self.headers)))