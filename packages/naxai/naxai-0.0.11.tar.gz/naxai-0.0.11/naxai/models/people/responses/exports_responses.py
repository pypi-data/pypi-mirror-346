from typing import Optional, Literal
from pydantic import BaseModel, Field
from naxai.models.base.pagination import Pagination

class ContactBaseModel(BaseModel):
    """
    Base model for contact information in the Naxai People API.
    
    This class defines the common structure for contact objects returned by various
    contact-related API endpoints. It contains essential contact information and
    communication preferences.
    
    Attributes:
        nx_id (str): The unique Naxai identifier for the contact.
            Mapped from JSON key 'nxId'.
        email (Optional[str]): The contact's email address.
            Defaults to None if not provided.
        phone (Optional[str]): The contact's phone number.
            Defaults to None if not provided.
        sms_capable (Optional[bool]): Whether the contact's phone can receive SMS messages.
            Mapped from JSON key 'smsCapable'. Defaults to None if not provided.
        external_id (Optional[str]): An external identifier for the contact, typically
            from your own system. Mapped from JSON key 'externalId'.
            Defaults to None if not provided.
        unsubscribed (Optional[bool]): Whether the contact has unsubscribed from communications.
            Defaults to None if not provided.
        language (Optional[str]): The contact's preferred language code (e.g., "en", "fr").
            Defaults to None if not provided.
        created_at (Optional[int]): Timestamp when the contact was created in your system.
            Mapped from JSON key 'createdAt'. Defaults to None if not provided.
        created_at_naxai (Optional[int]): Timestamp when the contact was created in Naxai.
            Mapped from JSON key 'createdAtNaxai'. Defaults to None if not provided.
    
    Example:
        >>> contact = ContactBaseModel(
        ...     nxId="cnt_123abc",
        ...     email="john.doe@example.com",
        ...     phone="+15551234567",
        ...     smsCapable=True,
        ...     externalId="cust_456def",
        ...     unsubscribed=False,
        ...     language="en",
        ...     createdAt=1703066400000,
        ...     createdAtNaxai=1703066400000
        ... )
        >>> print(f"Contact: {contact.email} (ID: {contact.nx_id})")
        Contact: john.doe@example.com (ID: cnt_123abc)
    
    Note:
        - This model supports both snake_case and camelCase field access through populate_by_name
        - The model allows extra fields beyond those explicitly defined, which can
          include custom attributes specific to the contact
        - Custom attributes will be accessible as dynamic properties on the model instance
    """
    nx_id: str = Field(alias="nxId")
    email: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    sms_capable: Optional[bool] = Field(default=None, alias="smsCapable")
    external_id: Optional[str] = Field(default=None, alias="externalId")
    unsubscribed: Optional[bool] = Field(default=None)
    language: Optional[str] = Field(default=None)
    created_at: Optional[int] = Field(default=None, alias="createdAt")
    created_at_naxai: Optional[int] = Field(default=None, alias="createdAtNaxai")

    model_config = {"populate_by_name": True,
                    "extra": "allow"}

class Export(BaseModel):
    """
    Model representing an export job in the Naxai People API.
    
    This class defines the structure for export jobs, which are used to export data
    from your Naxai account, such as contacts or other entities. Export jobs are
    processed asynchronously and can be monitored for completion.
    
    Attributes:
        id (str): The unique identifier of the export job.
        user_id (str): The ID of the user who created the export job.
            Mapped from JSON key 'userId'.
        email (Optional[str]): The email address where export notifications will be sent.
            Defaults to None.
        export (Optional[Literal["Contacts"]]): The type of data being exported.
            Currently only "Contacts" is supported. Defaults to None.
        state (Optional[Literal["pending", "done", "failed"]]): The current state of the export job.
            - "pending": The export is being processed
            - "done": The export has completed successfully
            - "failed": The export encountered an error
            Defaults to None.
        failed (Optional[bool]): Whether the export job has failed.
            Defaults to None.
        rows (Optional[int]): The number of rows/records in the export.
            Only available when the export is complete. Defaults to None.
        created_at (Optional[int]): Timestamp when the export job was created.
            Defaults to None.
            Mapped from JSON key 'createdAt'.
    
    Example:
        >>> export = Export(
        ...     id="exp_123abc",
        ...     userId="usr_456def",
        ...     email="user@example.com",
        ...     export="Contacts",
        ...     state="done",
        ...     failed=False,
        ...     rows=1250,
        ...     createdAt=1703066400000
        ... )
        >>> print(f"Export job {export.id} is in state: {export.state}")
        >>> print(f"Contains {export.rows} records")
    
    Note:
        - This model supports both snake_case and camelCase field access through populate_by_name
        - Export jobs are processed asynchronously and may take time to complete
        - Once an export job is complete, the file can be downloaded using the download URL
        - Export files are typically available for a limited time after completion
    """
    id: str
    user_id: str = Field(alias="userId")
    email: Optional[str] = Field(default=None)
    export: Optional[Literal["Contacts"]] = Field(default=None)
    state: Optional[Literal["pending", "done", "failed"]] = Field(default=None)
    failed: Optional[bool] = Field(default=None)
    rows: Optional[int] = Field(default=None)
    created_at: Optional[int] = Field(default=None, alias="createdAt")

    model_config = {"populate_by_name": True}

class ListExportsResponse(BaseModel):
    """
    Response model for listing export jobs in the Naxai People API.
    
    This class represents the response returned by the API when retrieving a list of
    export jobs. It implements list-like behavior, allowing the response to be used
    as an iterable collection of export objects.
    
    Attributes:
        root (list[Export]): The list of export job objects returned by the API.
            Defaults to an empty list if no exports are found.
    
    Example:
        >>> # Creating a response with export objects
        >>> exports = [
        ...     Export(id="exp_123", userId="usr_456", state="done", rows=1250),
        ...     Export(id="exp_789", userId="usr_456", state="pending")
        ... ]
        >>> response = ListExportsResponse(root=exports)
        >>> 
        >>> # Using list-like operations
        >>> len(response)  # Returns 2
        >>> response[0]    # Returns the first export
        >>> for export in response:  # Iterating through exports
        ...     print(f"Export {export.id} is in state: {export.state}")
        Export exp_123 is in state: done
        Export exp_789 is in state: pending
        >>> 
        >>> # Parsing from JSON
        >>> json_data = '[{"id": "exp_123", "userId": "usr_456", "state": "done"}, {"id": "exp_789", "userId": "usr_456", "state": "pending"}]'
        >>> response = ListExportsResponse.model_validate_json(json_data)
        >>> len(response)  # Returns 2
    
    Note:
        - This class implements __len__, __getitem__, and __iter__ methods to provide
          list-like behavior
        - The model_validate_json method handles both array-style JSON and object-style
          JSON with a root field
        - When a JSON array is provided, it's automatically wrapped in a 'root' field
        - The class uses Pydantic's default_factory to initialize the root as an empty
          list when no data is provided
        - Export jobs are typically listed in reverse chronological order (newest first)
    """
    root: list[Export] = Field(default_factory=list)

    def __len__(self) -> int:
        """Return the number of exports in the list."""
        return len(self.root)

    def __getitem__(self, index):
        """Access export by index."""
        return self.root[index]

    def __iter__(self):
        """Iterate through exports."""
        return iter(self.root)

    @classmethod
    def model_validate_json(cls, json_data: str, **kwargs):
        """Parse JSON data into the model.
        
        This method handles both array-style JSON and object-style JSON with a root field.
        
        Args:
            json_data (str): The JSON string to parse
            **kwargs: Additional arguments to pass to the standard model_validate_json method
            
        Returns:
            ListAttributesResponse: A validated instance of the class
        """
        import json
        data = json.loads(json_data)
        
        # If the data is a list, wrap it in a dict with the root field
        if isinstance(data, list):
            return cls(root=data)
        
        # Otherwise, use the standard Pydantic validation
        return super().model_validate_json(json_data, **kwargs)

class GetExportResponse(Export):
    """
    Response model for retrieving a specific export job in the Naxai People API.
    
    This class represents the response returned by the API when retrieving details
    about a single export job. It inherits all fields from the Export model.
    
    Example:
        >>> response = GetExportResponse(
        ...     id="exp_123abc",
        ...     userId="usr_456def",
        ...     email="user@example.com",
        ...     export="Contacts",
        ...     state="done",
        ...     failed=False,
        ...     rows=1250,
        ...     createdAt=1703066400000
        ... )
        >>> 
        >>> # Check if the export is ready for download
        >>> if response.state == "done" and not response.failed:
        ...     print(f"Export is ready for download. Contains {response.rows} records.")
        ... elif response.state == "pending":
        ...     print("Export is still being processed.")
        ... elif response.failed or response.state == "failed":
        ...     print("Export failed.")
        Export is ready for download. Contains 1250 records.
        >>> 
        >>> # Convert timestamp to readable date
        >>> from datetime import datetime
        >>> created_date = datetime.fromtimestamp(response.created_at / 1000)
        >>> print(f"Export was created on: {created_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    Note:
        - This class inherits all fields and behavior from the Export model
        - Use this model to check the status of an export job before attempting to download it
        - Export jobs may take time to complete, especially for large datasets
        - Once an export job is in the "done" state, you can retrieve its download URL
          using the appropriate API endpoint
    """

class GetExportDownloadUrlResponse(BaseModel):
    """
    Response model for retrieving the download URL of a completed export in the Naxai People API.
    
    This class represents the response returned by the API when requesting a download URL
    for a completed export job. The URL can be used to download the exported data file.
    
    Attributes:
        url (str): The temporary URL where the export file can be downloaded from.
    
    Example:
        >>> response = GetExportDownloadUrlResponse(
        ...     url="https://download.naxai.com/exports/exp_123abc.csv?token=abc123"
        ... )
        >>> 
        >>> # The URL can be used to download the file
        >>> download_url = response.url
        >>> print(f"Download URL: {download_url}")
        >>> 
        >>> # In a real application, you might download the file using requests or similar
        >>> import requests
        >>> # r = requests.get(download_url)
        >>> # with open("exported_contacts.csv", "wb") as f:
        >>> #     f.write(r.content)
        >>> # print("File downloaded successfully")
    
    Note:
        - The download URL is temporary and will expire after a certain period
        - Only exports in the "done" state can be downloaded
        - Before requesting a download URL, check that the export job is complete
          using the GetExportResponse model
        - The exported file format is typically CSV for contacts exports
        - Large exports may take significant time to download depending on your connection
    """
    url: str

class CreateExportResponse(BaseModel):
    """
    Response model for creating a new export job in the Naxai People API.
    
    This class represents the response returned by the API when a new export job is
    successfully created. Unlike other export responses, this model contains pagination
    information and a list of contacts that will be included in the export.
    
    Attributes:
        pagination (Pagination): Pagination information about the contacts being exported,
            including the total number of contacts and page information.
        contacts (list[ContactBaseModel]): A preview list of contacts that will be included
            in the export. This typically includes a sample of the first few contacts.
    
    Example:
        >>> response = CreateExportResponse(
        ...     pagination=Pagination(
        ...         page=1,
        ...         page_size=25,
        ...         total_pages=40,
        ...         total_items=1000
        ...     ),
        ...     contacts=[
        ...         ContactBaseModel(nx_id="cnt_123", email="john@example.com"),
        ...         ContactBaseModel(nx_id="cnt_456", email="jane@example.com")
        ...     ]
        ... )
        >>> 
        >>> print(f"Export job created for {response.pagination.total_items} contacts")
        >>> print(f"Sample contacts ({len(response.contacts)}):")
        >>> for contact in response.contacts:
        ...     print(f"- {contact.email} (ID: {contact.nx_id})")
        Export job created for 1000 contacts
        Sample contacts (2):
        - john@example.com (ID: cnt_123)
        - jane@example.com (ID: cnt_456)
        >>> 
        >>> # In a real application, you would store the export ID from the response
        >>> # and use it to check the status later
        >>> # export_id = response.id  # Note: This example assumes the ID is in the response
        >>> # Later: await client.people.exports.get(export_id=export_id)
    
    Note:
        - This response provides a preview of the contacts that will be exported
        - The pagination information indicates the total number of contacts in the export
        - Unlike GetExportResponse, this doesn't contain the export job ID directly
        - You may need to extract the export ID from headers or other response metadata
        - Export jobs are processed asynchronously and may take time to complete
        - After creating an export, you should periodically check its status using the get method
        - Once the export is complete, you can retrieve the download URL
    """
    pagination: Pagination
    contacts: list[ContactBaseModel]