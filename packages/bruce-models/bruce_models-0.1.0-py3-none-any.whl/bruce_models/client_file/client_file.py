from typing import Optional, TypedDict, List, Any
from bruce_models import BruceApi

class ClientFile:
    """
    Represents a Client File in Nextspace.
    You will find the JClientFile data-model and all related API communication here.
    """

    class JClientFile(TypedDict):
        # The ID of the file.
        ID: str
        # The file's original name. This includes the extension.
        OriginalFileName: str
        # The file's size in bytes.
        OriginalLength: int
        # The file's mime type.
        MIMEType: str
        # The file's extension.
        # Currently a mess with conflicting records with and without the dot.
        FileExt: str
        # Date/time when the file was uploaded.
        Created: str
        # The user's ID who uploaded the file.
        UploadedByUser_ID: str
        # An optional category for the file.
        # Some Nextspace default purposes have additional meaning.
        Purpose: Optional[str]

    @staticmethod
    def get_url(api: BruceApi, id: str) -> str:
        """
        Get the URL to download a Client File by its ID.
        """
        if not id:
            raise ValueError("ID is required to get the download URL.")
        return f"{api.base_url}file/{id}"

    @staticmethod
    def get_url(api: BruceApi, file: JClientFile) -> str:
        """
        Get the URL to download a Client File by its JClientFile data-model.
        """
        if not file:
            raise ValueError("File is required to get the download URL.")
        
        ext = file.get("FileExt")
        if not ext and file.get("OriginalFileName"):
            ext = file.get("OriginalFileName").split(".")[-1]
        if not ext:
            ext = ""
        if len(ext) > 0 and ext[0] != ".":
            ext = f".{ext}"

        return f"{api.base_url}file/{file.get('ID')}{ext}"

    @staticmethod
    def get(api: BruceApi, id: str) -> JClientFile:
        """
        Get Client File details by its ID.
        """
        if not id:
            raise ValueError("ID is required to get Client File details.")
        return api.GET(f"file/{id}/details")
    
    @staticmethod
    def delete(api: BruceApi, ids: List[str]) -> None:
        """
        Delete a list of Client Files by IDs
        """
        if not ids:
            raise ValueError("IDs are required to delete Client Files.")
        
        body = {
            "Items": ids
        }
        api.POST("deleteFiles", body)

    @staticmethod
    def update_purpose(api: BruceApi, file_id: str, purpose: str) -> None:
        """
        Update the purpose of a Client File.
        """
        if not file_id:
            raise ValueError("File ID is required to update the purpose.")
        
        params = {
            "Purpose": purpose
        }
        api.POST(f"file/updatepurpose/{file_id}", {}, params)