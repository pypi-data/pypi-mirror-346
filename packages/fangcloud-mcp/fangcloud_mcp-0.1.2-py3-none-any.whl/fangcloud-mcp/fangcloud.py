"""
#!/usr/bin/env python3
FangCloud MCP Main Module

This is the main entry point for the FangCloud MCP server.
"""

import logging
import argparse
import asyncio
import sys
import os
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from .fangcloud_api import FangcloudAPI


# Configure logging
DEFAULT_LOG_FILE = "fangcloud_mcp.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(DEFAULT_LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("FangCloud.Main")


# Initialize MCP server
mcp = FastMCP("fangcloud")
api = FangcloudAPI()

@mcp.tool()
async def get_file_info(file_id: str) -> Dict[str, Any]:
    """
    Get file information
    
    Args:
        file_id: File ID
        
    Returns:
        File information (JSON format) or error message
    """
    
    if not file_id:
        return {"status": "error", "message": "file_id is required"}
    
    try:
        result = await api.get_file_info(file_id)
        if result:
            return {"status": "success", "data": result}
        else:
            return {"status": "error", "message": f"Failed to get file info for file ID {file_id}"}
    except Exception as e:
        error_msg = f"Get file info operation failed - {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"status": "error", "message": error_msg}

@mcp.tool()
async def get_folder_info(folder_id: str) -> Dict[str, Any]:
    """
    Get folder information
    
    Args:
        folder_id: Folder ID
        
    Returns:
        Folder information (JSON format) or error message
    """
    if not folder_id:
        return {"status": "error", "message": "folder_id is required"}
    
    try:
        result = await api.get_folder_info(folder_id)
        if result:
            return {"status": "success", "data": result}
        else:
            return {"status": "error", "message": f"Failed to get folder info for folder ID {folder_id}"}
    except Exception as e:
        error_msg = f"Get folder info operation failed - {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"status": "error", "message": error_msg}

@mcp.tool()
async def create_folder(name: str, parent_id: str, 
                        target_space_type: Optional[str] = None, 
                        target_space_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new folder
    
    Args:
        name: Folder name (1-222 characters, cannot contain / ? : * " > <)
        parent_id: Parent folder ID
        target_space_type: Space type - "department" or "personal" (optional, effective when parent_id is 0)
        target_space_id: Space ID (required when target_space_type is "department")
        
    Returns:
        Folder creation result (JSON format) or error message
    """  
    if not name:
        return {"status": "error", "message": "name is required"}
        
    if not parent_id:
        return {"status": "error", "message": "parent_id is required"}
    
    try:
        # Validate folder name length
        if len(name) < 1 or len(name) > 222:
            return {"status": "error", "message": "Folder name must be between 1 and 222 characters"}
            
        # Check for invalid characters in folder name
        invalid_chars = ['/', '?', ':', '*', '"', '>', '<']
        if any(char in name for char in invalid_chars):
            return {"status": "error", "message": "Folder name contains invalid characters (/ ? : * \" > <)"}
        
        # Check if target_space_id is provided when needed
        if parent_id == "0" or parent_id == 0:
            if target_space_type == "department" and not target_space_id:
                return {"status": "error", "message": "target_space_id is required when target_space_type is department"}
        
        result = await api.create_folder(
            name, parent_id, target_space_type, target_space_id
        )
        if result:
            return {"status": "success", "data": result}
        else:
            return {"status": "error", "message": f"Failed to create folder '{name}' in parent folder {parent_id}"}
    except Exception as e:
        error_msg = f"Create folder operation failed - {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"status": "error", "message": error_msg}

@mcp.tool()
async def upload_file(parent_folder_id: str, local_file_path: str) -> Dict[str, Any]:
    """
    Upload file to FangCloud
    
    Args:
        parent_folder_id: Target folder ID in FangCloud
        local_file_path: Local file path to upload
        
    Returns:
        Upload result message
    """
    if not parent_folder_id:
        return {"status": "error", "message": "parent_folder_id is required"}
        
    if not local_file_path:
        return {"status": "error", "message": "local_file_path is required"}
    
    try:
        # 获取文件名
        file_name = os.path.basename(local_file_path)
        
        # 获取上传URL
        upload_url = await api.get_file_upload_url(parent_folder_id, file_name)
        if not upload_url:
            return {"status": "error", "message": f"Failed to get upload URL for {file_name}"}
        
        # 上传文件
        result = await api.upload_file(upload_url, local_file_path)
        
        if result:
            return {
                "status": "success", 
                "message": f"File uploaded successfully - {local_file_path} -> Folder ID {parent_folder_id}",
                "file_name": file_name,
                "parent_folder_id": parent_folder_id
            }
        else:
            return {"status": "error", "message": f"File upload failed - {local_file_path}"}
    except Exception as e:
        error_msg = f"Upload operation failed - {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"status": "error", "message": error_msg}

@mcp.tool()
async def update_file(file_id: str, name: Optional[str] = None, 
                        description: Optional[str] = None) -> Dict[str, Any]:
    """
    Update file name and/or description
    
    Args:
        file_id: File ID
        name: New file name (optional)
        description: New file description (optional)
        
    Returns:
        Update result message
        
    Note:
        At least one of name or description must be provided
    """    
    if not file_id:
        return {"status": "error", "message": "file_id is required"}
        
    if not name and not description:
        return {"status": "error", "message": "At least one of name or description must be provided"}
    
    try:
        result = await api.update_file(file_id, name, description)
        if result:
            updated_fields = []
            if name:
                updated_fields.append("name")
            if description:
                updated_fields.append("description")
                
            fields_str = " and ".join(updated_fields)
            return {
                "status": "success", 
                "message": f"File {file_id} {fields_str} updated successfully",
                "file_id": file_id,
                "updated_fields": updated_fields
            }
        else:
            return {"status": "error", "message": f"Failed to update file ID {file_id}"}
    except Exception as e:
        error_msg = f"Update operation failed - {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"status": "error", "message": error_msg}

@mcp.tool()
async def download_file(file_id: str, local_path: str) -> Dict[str, Any]:
    """
    Download file from FangCloud
    
    Args:
        file_id: File ID
        local_path: Local path to save the file
        
    Returns:
        local file path or error message
    """
    if not file_id:
        return {"status": "error", "message": "file_id is required"}
    
    try:
        # Download file to local path
        result = await api.download_file_to_local(file_id, local_path)
        if result:
            return {
                "status": "success", 
                "message": f"File downloaded to {result}",
                "file_path": result
            }
        else:
            return {"status": "error", "message": f"Failed to download file ID {file_id} to {local_path}"}
    except Exception as e:
        error_msg = f"Download operation failed - {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"status": "error", "message": error_msg}

@mcp.tool()
async def list_folder_contents(folder_id: str, page_id: Optional[int] = 0,
                                page_capacity: Optional[int] = 20, type_filter: Optional[str] = "all",
                                sort_by: Optional[str] = "date", 
                                sort_direction: Optional[str] = "desc") -> Dict[str, Any]:
    """
    List folder contents (files and subfolders)
    
    Args:
        folder_id: Folder ID
        page_id: Page number (optional, default 0)
        page_capacity: Page capacity (optional, default 20)
        type_filter: Filter by type - "file", "folder", or "all" (optional, default "all")
        sort_by: Sort by - "name", "date", or "size" (optional, default "date")
        sort_direction: Sort direction - "desc" or "asc" (optional, default "desc")
        
    Returns:
        Folder contents (JSON format) or error message
    """ 
    if not folder_id:
        return {"status": "error", "message": "folder_id is required"}
    
    try:
        result = await api.get_folder_children(
            folder_id, page_id, page_capacity, type_filter, sort_by, sort_direction
        )
        if result:
            return {"status": "success", "data": result}
        else:
            return {"status": "error", "message": f"Failed to get contents for folder ID {folder_id}"}
    except Exception as e:
        error_msg = f"List folder contents operation failed - {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"status": "error", "message": error_msg}

@mcp.tool()
async def list_personal_items(page_id: Optional[int] = 0,
                                page_capacity: Optional[int] = 20, type_filter: Optional[str] = "all",
                                sort_by: Optional[str] = "date", 
                                sort_direction: Optional[str] = "desc") -> Dict[str, Any]:
    """
    List personal items (files and folders in personal space)
    
    Args:
        page_id: Page number (optional, default 0)
        page_capacity: Page capacity (optional, default 20)
        type_filter: Filter by type - "file", "folder", or "all" (optional, default "all")
        sort_by: Sort by - "name", "date", or "size" (optional, default "date")
        sort_direction: Sort direction - "desc" or "asc" (optional, default "desc")
        
    Returns:
        Personal items (JSON format) or error message
    """
    try:
        result = await api.get_personal_items(
            page_id, page_capacity, type_filter, sort_by, sort_direction
        )
        if result:
            return {"status": "success", "data": result}
        else:
            return {"status": "error", "message": "Failed to get personal items"}
    except Exception as e:
        error_msg = f"List personal items operation failed - {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"status": "error", "message": error_msg}

@mcp.tool()
async def search_items(query_words: str, search_type: Optional[str] = "all",
                        page_id: Optional[int] = 0, search_in_folder: Optional[str] = None,
                        query_filter: Optional[str] = "all", 
                        updated_time_range: Optional[str] = None) -> Dict[str, Any]:
    """
    Search for files and folders
    
    Args:
        query_words: Search keywords (required)
        search_type: Search type - "file", "folder", or "all" (optional, default "all")
        page_id: Page number (optional, default 0)
        search_in_folder: Parent folder ID to search within (optional)
        query_filter: Search filter - "file_name", "content", "creator", or "all" (optional, default "all")
        updated_time_range: Updated time range in format "start_timestamp,end_timestamp" (optional)
                            Both timestamps can be empty, but comma is required
        
    Returns:
        Search results (JSON format) or error message
    """  
    if not query_words:
        return {"status": "error", "message": "query_words is required"}
    
    try:
        result = await api.search_items(
            query_words, search_type, page_id, search_in_folder, query_filter, updated_time_range
        )
        if result:
            return {"status": "success", "data": result}
        else:
            return {"status": "error", "message": f"Failed to search for items with query: {query_words}"}
    except Exception as e:
        error_msg = f"Search operation failed - {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"status": "error", "message": error_msg}


def main():
    """Main entry point for the FangCloud MCP server"""
    try:
        logger.info("=== Starting FangCloud MCP ===")
        
        # Parse command line arguments
        parser = argparse.ArgumentParser(description='FangCloud MCP')
        parser.add_argument('--access_token', '-c', type=str, required=True, help='FangCloud API access token is required')
        args = parser.parse_args()
        
        # Validate access_token
        if not args.access_token:
            logger.error("Access token is required")
            sys.exit(1)
            
        logger.info(f"access_token: {args.access_token}")
        
        # set access_token
        api.set_access_token(args.access_token)
        
        # Run MCP server
        logger.info("Starting MCP server")
        mcp.run(transport='stdio')
        
    except Exception as e:
        logger.error(f"Initialization failed: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        if 'api' in locals():
            asyncio.run(api.cleanup())

if __name__ == "__main__":
    main()
