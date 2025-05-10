from typing import Optional, Literal
from pydantic import BaseModel, Field

class FileObject(BaseModel):
    """
    Model representing file configuration for imports in the Naxai People API.
    
    This class defines settings for how to parse the import file, such as
    the delimiter used to separate values in CSV files.
    
    Attributes:
        separator (Literal[",", ";"]): The character used to separate values in the import file.
            Must be either a comma (",") or semicolon (";"). Defaults to semicolon (";").
    
    Example:
        >>> file_config = FileObject(separator=",")
        >>> print(f"Using '{file_config.separator}' as the CSV separator")
        Using ',' as the CSV separator
    
    Note:
        - The separator is crucial for correctly parsing CSV files
        - Most spreadsheet applications can export CSV files with either separator
        - Use comma for standard CSV files and semicolon for files where data may contain commas
    """
    separator: Literal[",", ";"] = Field(default=";")

class SegmentObject(BaseModel):
    """
    Model representing a segment reference for imports in the Naxai People API.
    
    This class is used to specify which segment should be associated with an import,
    allowing imported contacts to be automatically added to a segment.
    
    Attributes:
        segment_id (str): The unique identifier of the segment to associate with the import.
            Mapped from JSON key 'segmentId'.
    
    Example:
        >>> segment = SegmentObject(segmentId="seg_123abc")
        >>> print(f"Importing contacts to segment: {segment.segment_id}")
        Importing contacts to segment: seg_123abc
        >>> 
        >>> # Can also use snake_case
        >>> segment = SegmentObject(segment_id="seg_123abc")
        >>> print(f"Importing contacts to segment: {segment.segment_id}")
        Importing contacts to segment: seg_123abc
    
    Note:
        - This model supports both snake_case and camelCase field access through populate_by_name
        - The segment must exist before it can be used in an import
        - Only manual segments can be used for imports
        - All imported contacts will be added to the specified segment
    """
    segment_id: str = Field(alias="segmentId")

    model_config = {"populate_by_name": True}

class MappingObject(BaseModel):
    """
    Model representing a field mapping for imports in the Naxai People API.
    
    This class defines how columns in the import file map to attributes in the Naxai system.
    Each mapping object represents one column in the import file and specifies whether to
    skip it or which attribute it should be mapped to.
    
    Attributes:
        header (Optional[str]): The column header name from the import file.
            Defaults to None.
        skip (Optional[bool]): Whether to skip this column during import.
            If True, the column will be ignored. Defaults to None.
        attribute (Optional[str]): The name of the attribute in Naxai to map this column to.
            Defaults to None.
    
    Example:
        >>> # Map a column named "Email Address" to the "email" attribute
        >>> email_mapping = MappingObject(
        ...     header="Email Address",
        ...     skip=False,
        ...     attribute="email"
        ... )
        >>> 
        >>> # Skip a column named "Internal ID"
        >>> skip_mapping = MappingObject(
        ...     header="Internal ID",
        ...     skip=True
        ... )
        >>> 
        >>> # Map a column to a custom attribute
        >>> custom_mapping = MappingObject(
        ...     header="Loyalty Points",
        ...     attribute="loyalty_points"
        ... )
    
    Note:
        - The header should match exactly the column name in the import file
        - Standard attributes include: email, phone, externalId, firstName, lastName, etc.
        - Custom attributes must exist in your account before they can be used in mappings
        - Setting skip=True will cause the column to be ignored during import
        - If attribute is not specified, the system will try to match the header to a known attribute
    """
    header: Optional[str] = Field(default=None)
    skip: Optional[bool] = Field(default=None)
    attribute: Optional[str] = Field(default=None)

class Import(BaseModel):
    """
    Model representing an import job in the Naxai People API.
    
    This class defines the structure for import jobs, which are used to import contacts
    or events into your Naxai account from external files. Import jobs are processed
    asynchronously and can be monitored for completion.
    
    Attributes:
        id (str): The unique identifier of the import job.
        name (str): The name of the import job.
        description (Optional[str]): A description of the import job. Defaults to None.
        user_id (Optional[str]): The ID of the user who created the import job. Defaults to None.
        type_ (Optional[Literal["manual", "ftp-template"]]): The type of import.
            - "manual": A one-time manual import
            - "ftp-template": An import based on an FTP template
            Mapped from JSON key 'type'. Defaults to None.
        state (Optional[Literal["preparing", "importing", "imported", "failed", "canceled"]]):
            The current state of the import job.
            - "preparing": The import is being prepared
            - "importing": The import is in progress
            - "imported": The import has completed successfully
            - "failed": The import encountered an error
            - "canceled": The import was canceled
            Defaults to None.
        file (Optional[FileObject]): Configuration for parsing the import file.
            Defaults to None.
        import_mode (Optional[Literal["contacts", "events"]]): The type of data being imported.
            - "contacts": Importing contact records
            - "events": Importing event data
            Defaults to None.
        event_name (Optional[str]): The name of the event when import_mode is "events".
            Mapped from JSON key 'eventName'. Defaults to None.
        segment (Optional[SegmentObject]): The segment to add imported contacts to.
            Defaults to None.
        mapping (Optional[list[MappingObject]]): The field mappings for the import.
            Defines how columns in the import file map to attributes in Naxai.
            Defaults to None.
        rows_to_import (Optional[int]): The total number of rows to be imported.
            Mapped from JSON key 'rowToImport'. Defaults to None.
        rows_imported (Optional[int]): The number of rows successfully imported so far.
            Mapped from JSON key 'rowsImported'. Defaults to None.
        failed_reason (Optional[int]): The reason code if the import failed.
            Mapped from JSON key 'failedReason'. Defaults to None.
        created_at (Optional[int]): Timestamp when the import job was created.
            Mapped from JSON key 'createdAt'. Defaults to None.
        modified_at (Optional[int]): Timestamp when the import job was last modified.
            Mapped from JSON key 'modifiedAt'. Defaults to None.
    
    Example:
        >>> import_job = Import(
        ...     id="imp_123abc",
        ...     name="Monthly Customer Import",
        ...     description="Import of new customers from January 2023",
        ...     user_id="usr_456def",
        ...     type="manual",
        ...     state="imported",
        ...     file=FileObject(separator=","),
        ...     import_mode="contacts",
        ...     segment=SegmentObject(segment_id="seg_789ghi"),
        ...     mapping=[
        ...         MappingObject(header="Email", attribute="email"),
        ...         MappingObject(header="First Name", attribute="firstName"),
        ...         MappingObject(header="Last Name", attribute="lastName")
        ...     ],
        ...     rows_to_import=1250,
        ...     rows_imported=1250,
        ...     created_at=1703066400000,
        ...     modified_at=1703067000000
        ... )
        >>> 
        >>> print(f"Import job: {import_job.name} (ID: {import_job.id})")
        >>> print(f"Status: {import_job.state}")
        >>> print(f"Imported {import_job.rows_imported} of {import_job.rows_to_import} rows")
        Import job: Monthly Customer Import (ID: imp_123abc)
        Status: imported
        Imported 1250 of 1250 rows
    
    Note:
        - This model supports both snake_case and camelCase field access through populate_by_name
        - Import jobs are processed asynchronously and may take time to complete
        - The state field indicates the current status of the import
        - For large imports, monitor the rows_imported field to track progress
        - If an import fails, check the failed_reason field for more information
        - The mapping field is crucial for correctly mapping import data to Naxai attributes
    """
    id: str
    name: str
    description: Optional[str] = Field(default=None)
    user_id: Optional[str] = Field(default=None)
    type_: Optional[Literal["manual", "ftp-template"]] = Field(alias="type", default=None)
    state: Optional[Literal["preparing", "importing", "imported", "failed", "canceled"]] = Field(default=None)
    file: Optional[FileObject] = Field(default=None)
    import_mode: Optional[Literal["contacts", "events"]] = Field(default=None)
    event_name: Optional[str] = Field(alias="eventName", default=None)
    segment: Optional[SegmentObject] = Field(default=None)
    mapping: Optional[list[MappingObject]] = Field(default=None)
    rows_to_import: Optional[int] = Field(default=None, alias="rowToImport")
    rows_imported: Optional[int] = Field(default=None, alias="rowsImported")
    failed_reason: Optional[int] = Field(default=None, alias="failedReason")
    created_at: Optional[int] = Field(default=None, alias="createdAt")
    modified_at: Optional[int] = Field(default=None, alias="modifiedAt")

    model_config = {"populate_by_name": True}

class ListImportsResponse(BaseModel):
    """
    Response model for listing import jobs in the Naxai People API.
    
    This class represents the response returned by the API when retrieving a list of
    import jobs. It implements list-like behavior, allowing the response to be used
    as an iterable collection of import objects.
    
    Attributes:
        root (list[Import]): The list of import job objects returned by the API.
            Defaults to an empty list if no imports are found.
    
    Example:
        >>> # Creating a response with import objects
        >>> imports = [
        ...     Import(id="imp_123", name="January Import", state="imported", rows_imported=1250),
        ...     Import(id="imp_456", name="February Import", state="importing", rows_imported=500)
        ... ]
        >>> response = ListImportsResponse(root=imports)
        >>> 
        >>> # Using list-like operations
        >>> len(response)  # Returns 2
        >>> response[0]    # Returns the first import
        >>> for import_job in response:  # Iterating through imports
        ...     print(f"Import {import_job.name} is in state: {import_job.state}")
        Import January Import is in state: imported
        Import February Import is in state: importing
        >>> 
        >>> # Parsing from JSON
        >>> json_data = '[{"id": "imp_123", "name": "January Import", "state": "imported"}, {"id": "imp_456", "name": "February Import", "state": "importing"}]'
        >>> response = ListImportsResponse.model_validate_json(json_data)
        >>> len(response)  # Returns 2
        >>> 
        >>> # Filter imports by state
        >>> completed_imports = [imp for imp in response if imp.state == "imported"]
        >>> print(f"Found {len(completed_imports)} completed imports")
        Found 1 completed imports
    
    Note:
        - This class implements __len__, __getitem__, and __iter__ methods to provide
          list-like behavior
        - The model_validate_json method handles both array-style JSON and object-style
          JSON with a root field
        - When a JSON array is provided, it's automatically wrapped in a 'root' field
        - The class uses Pydantic's default_factory to initialize the root as an empty
          list when no data is provided
        - Import jobs are typically listed in reverse chronological order (newest first)
        - You can filter or sort the imports based on their attributes after retrieval
    """
    root: list[Import] = Field(default_factory=list)

    def __len__(self) -> int:
        """Return the number of imports in the list."""
        return len(self.root)

    def __getitem__(self, index):
        """Access import by index."""
        return self.root[index]

    def __iter__(self):
        """Iterate through imports."""
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

class GetImportResponse(Import):
    """
    Response model for retrieving a specific import job in the Naxai People API.
    
    This class represents the response returned by the API when retrieving details
    about a single import job. It inherits all fields from the Import model.
    
    Example:
        >>> response = GetImportResponse(
        ...     id="imp_123abc",
        ...     name="Monthly Customer Import",
        ...     description="Import of new customers from January 2023",
        ...     user_id="usr_456def",
        ...     type="manual",
        ...     state="importing",
        ...     import_mode="contacts",
        ...     rows_to_import=1250,
        ...     rows_imported=750,
        ...     created_at=1703066400000,
        ...     modified_at=1703067000000
        ... )
        >>> 
        >>> # Check the import status
        >>> if response.state == "imported":
        ...     print(f"Import complete! {response.rows_imported} contacts imported.")
        ... elif response.state == "importing":
        ...     progress = (response.rows_imported / response.rows_to_import) * 100 if response.rows_to_import else 0
        ...     print(f"Import in progress: {progress:.1f}% complete ({response.rows_imported}/{response.rows_to_import})")
        ... elif response.state == "failed":
        ...     print(f"Import failed. Reason code: {response.failed_reason}")
        ... elif response.state == "preparing":
        ...     print("Import is being prepared.")
        ... elif response.state == "canceled":
        ...     print("Import was canceled.")
        Import in progress: 60.0% complete (750/1250)
        >>> 
        >>> # Convert timestamp to readable date
        >>> from datetime import datetime
        >>> created_date = datetime.fromtimestamp(response.created_at / 1000)
        >>> print(f"Import was created on: {created_date.strftime('%Y-%m-%d %H:%M:%S')}")
        Import was created on: 2023-12-20 12:00:00
    
    Note:
        - This class inherits all fields and behavior from the Import model
        - Use this model to check the status and progress of an import job
        - Import jobs may take time to complete, especially for large datasets
        - The rows_imported field can be used to track progress during the import
        - If an import fails, the failed_reason field may provide more information
        - Once an import is complete (state="imported"), the contacts or events
          have been successfully added to your account
    """