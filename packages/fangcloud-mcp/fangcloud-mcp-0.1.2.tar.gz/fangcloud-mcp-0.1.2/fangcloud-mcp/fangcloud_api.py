"""
FangCloud API Module

This module provides API client functionality for interacting with FangCloud.
"""

import logging
import uuid
import os
import aiohttp
from typing import Dict, Any, Optional

# Constants
TOKEN_EXPIRY_SECONDS = 59
HTTP_OK = 200
REQUEST_TIMEOUT = 60
OPEN_HOST = "https://open.fangcloud.com"
API_UPLOAD_PATH = "/api/v2/file/upload_by_path"
API_FILE_UPLOAD_PATH = "/api/v2/file/upload"
API_FILE_INFO_PATH = "/api/v2/file/{id}/info"
API_FILE_UPDATE_PATH = "/api/v2/file/{id}/update"
API_FILE_DOWNLOAD_PATH = "/api/v2/file/{id}/download"
API_FOLDER_INFO_PATH = "/api/v2/folder/{id}/info"
API_FOLDER_CHILDREN_PATH = "/api/v2/folder/{id}/children"
API_PERSONAL_ITEMS_PATH = "/api/v2/folder/personal_items"
API_SEARCH_PATH = "/api/v2/item/search"
API_FOLDER_CREATE_PATH = "/api/v2/folder/create"
OAUTH_TOKEN_PATH = "/oauth/token"
GRANT_TYPE = "jwt_simple"
UPLOAD_TYPE = "api"

logger = logging.getLogger("FangCloud.API")


class FangcloudAPI:
    def __init__(self):
        self.access_token = ""
        self.open_host = OPEN_HOST

    def set_access_token(self, access_token:str):
        self.access_token = access_token

    def _validate_file(self, file_path: str) -> bool:
        logger.info(f"Starting file upload: {file_path}")
        
        if not os.path.exists(file_path):
            logger.error(f"File does not exist: {file_path}")
            return False
        
        file_size = os.path.getsize(file_path)
        logger.info(f"File size: {file_size} bytes")
        return True

    async def _send_request(self, url: str, method: str = "POST", headers: Dict[str, str] = None, 
                           data: Any = None, json_data: Any = None, 
                           is_json_response: bool = True) -> Optional[Any]:
        async with aiohttp.ClientSession() as session:
            try:
                request_method = getattr(session, method.lower())
                async with request_method(url, headers=headers, data=data, json=json_data) as response:
                    if response.status != HTTP_OK:
                        error_text = await response.text()
                        logger.error(f"Request failed, status: {response.status}, error: {error_text}")
                        return None
                    
                    if is_json_response:
                        return await response.json()
                    else:
                        return await response.text()
            except Exception as e:
                logger.error(f"Request error: {str(e)}", exc_info=True)
                return None
    
    async def _api_request(self, operation_name: str, url: str, method: str = "POST", 
                          headers: Dict[str, str] = None, data: Any = None, json_data: Any = None,
                          is_json_response: bool = True, check_token: bool = True,
                          success_key: str = None, success_msg: str = None, 
                          error_msg: str = None) -> Optional[Any]:
        try:
            # 检查访问令牌（如果需要）
            if check_token and not self.access_token:
                logger.error(f"Failed to {operation_name}: access_token is empty")
                return None
            
            # 添加认证头（如果需要且未提供）
            if check_token and headers is None:
                headers = {
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                }
            elif check_token and "Authorization" not in headers:
                headers["Authorization"] = f"Bearer {self.access_token}"
            
            # 发送请求
            logger.info(f"Sending {operation_name} request")
            result = await self._send_request(
                url=url, 
                method=method,
                headers=headers,
                data=data,
                json_data=json_data,
                is_json_response=is_json_response
            )
            
            if not result:
                return None
            
            # 检查成功响应中的关键字段
            if success_key is not None:
                if isinstance(result, dict) and success_key in result:
                    if success_msg:
                        logger.info(success_msg)
                    return result[success_key]
                else:
                    if error_msg:
                        logger.error(f"{error_msg}: {result}")
                    else:
                        logger.error(f"Failed to {operation_name}, response missing {success_key}: {result}")
                    return None
            
            # 如果没有指定关键字段，直接返回结果
            if success_msg:
                logger.info(success_msg)
            return result
                
        except Exception as e:
            logger.error(f"Error in {operation_name}: {str(e)}", exc_info=True)
            return None
    
    async def get_upload_url_by_path(self, target_folder_path: str, file_name: str) -> Optional[str]:
        logger.info(f"Getting file upload URL for {file_name}")
        url = f"{self.open_host}{API_UPLOAD_PATH}"
        
        params = {
            "target_folder_path": target_folder_path,
            "name": file_name,
            "upload_type": UPLOAD_TYPE
        }
        
        return await self._api_request(
            operation_name="get upload URL",
            url=url,
            json_data=params,
            success_key="presign_url",
            success_msg="Successfully obtained upload URL",
            error_msg="Failed to get upload URL, response missing presign_url"
        )

    async def get_file_upload_url(self, parent_id: str, name: str, is_covered: Optional[bool] = None) -> Optional[str]:
        try:
            if not self.access_token:
                logger.error("Failed to get file upload URL: access_token is empty")
                return None
                
            logger.info(f"Getting file upload URL for {name} in folder {parent_id}")
            url = f"{self.open_host}{API_FILE_UPLOAD_PATH}"
            
            # Prepare request body
            params = {
                "parent_id": parent_id,
                "name": name,
                "upload_type": UPLOAD_TYPE
            }
            
            # Add optional parameters if provided
            if is_covered is not None:
                params["is_covered"] = is_covered
            
            return await self._api_request(
                operation_name="get file upload URL",
                url=url,
                json_data=params,
                success_key="presign_url",
                success_msg="Successfully obtained file upload URL",
                error_msg="Failed to get file upload URL, response missing presign_url"
            )
                
        except Exception as e:
            logger.error(f"Error getting file upload URL: {str(e)}", exc_info=True)
            return None
    
    async def upload_file(self, url: str, file_path: str) -> Optional[str]:
        try:
            if not url:
                logger.error("Failed to upload file: upload URL is empty")
                return None
                
            if not file_path:
                logger.error("Failed to upload file: file_path is empty")
                return None
            
            # 验证文件
            if not self._validate_file(file_path):
                return None
            
            # 发送文件上传请求
            try:
                with open(file_path, 'rb') as f:
                    form_data = aiohttp.FormData()
                    form_data.add_field('file', f, filename=os.path.basename(file_path))
                    
                    logger.info("Sending file upload request")
                    result = await self._send_request(
                        url=url, 
                        data=form_data, 
                        is_json_response=False
                    )
                    
                    if result:
                        logger.info("File upload successful")
                    return result
            except FileNotFoundError:
                logger.error(f"File not found or cannot be opened: {file_path}")
                return None
            except PermissionError:
                logger.error(f"Permission denied when accessing file: {file_path}")
                return None
                
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}", exc_info=True)
            return None
    
    async def get_file_info(self, file_id: str) -> Optional[Dict[str, Any]]:
        try:
            if not self.access_token:
                logger.error("Failed to get file info: access_token is empty")
                return None
                
            logger.info(f"Getting file info for file ID {file_id}")
            url = f"{self.open_host}{API_FILE_INFO_PATH.replace('{id}', file_id)}"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # Send request to get file information
            result = await self._send_request(url=url, method="GET", headers=headers)
            if not result:
                return None
            
            logger.info(f"Successfully obtained file info for file ID {file_id}")
            return result
                
        except Exception as e:
            logger.error(f"Error getting file info: {str(e)}", exc_info=True)
            return None
    
    async def update_file(self, file_id: str, name: Optional[str] = None, 
                         description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        try:
            if not self.access_token:
                logger.error("Failed to update file: access_token is empty")
                return None
                
            if not name and not description:
                logger.error("Failed to update file: both name and description are empty")
                return None
                
            logger.info(f"Updating file ID {file_id}")
            url = f"{self.open_host}{API_FILE_UPDATE_PATH.replace('{id}', file_id)}"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # Prepare request body
            params = {}
            if name:
                params["name"] = name
            if description:
                params["description"] = description
            
            # Send request to update file
            result = await self._send_request(url=url, headers=headers, json_data=params)
            if not result:
                return None
            
            logger.info(f"Successfully updated file ID {file_id}")
            return result
                
        except Exception as e:
            logger.error(f"Error updating file: {str(e)}", exc_info=True)
            return None
    
    async def get_download_url(self, file_id: str) -> Optional[str]:
        """
        Get file download URL
        
        Args:
            file_id: File ID
        Returns:
            Download URL or None (if request fails)
        """
        try:
            if not self.access_token:
                logger.error("Failed to get download URL: access_token is empty")
                return None
                
            logger.info(f"Getting download URL for file ID {file_id}")
            url = f"{self.open_host}{API_FILE_DOWNLOAD_PATH.replace('{id}', file_id)}"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # Prepare query parameters
            params = {}
            # Add query parameters to URL if any
            if params:
                query_string = "&".join([f"{k}={v}" for k, v in params.items()])
                url = f"{url}?{query_string}"
            
            # Send request to get download URL
            result = await self._send_request(url=url, method="GET", headers=headers)
            if not result:
                return None
            
            if "download_url" in result:
                logger.info(f"Successfully obtained download URL for file ID {file_id}")
                return result["download_url"]
            else:
                logger.error(f"Failed to get download URL, response missing download_url: {result}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting download URL: {str(e)}", exc_info=True)
            return None
    
    async def download_file_to_local(self, file_id: str, local_path: str) -> Optional[str]:
        try:
            # Get file info
            file_info = await self.get_file_info(file_id)
            if not file_info:
                logger.error(f"Failed to download file: could not get file info for file ID {file_id}")
                return None
            file_name = file_info["name"]
            file_path = os.path.join(local_path, file_name)

            # Get download URL
            download_url = await self.get_download_url(file_id)
            if not download_url:
                logger.error(f"Failed to download file: could not get download URL for file ID {file_id}")
                return None
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            # Generate temporary file path with UUID
            temp_dir = os.path.dirname(os.path.abspath(file_path))
            temp_filename = str(uuid.uuid4())
            temp_path = os.path.join(temp_dir, temp_filename)
            
            # Download file to temporary path first
            logger.info(f"Downloading file ID {file_id} to temporary file {temp_path}")
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(download_url) as response:
                        if response.status != HTTP_OK:
                            error_text = await response.text()
                            logger.error(f"File download failed, status: {response.status}, error: {error_text}")
                            return None
                        
                        # Save file to temporary path
                        with open(temp_path, 'wb') as f:
                            while True:
                                chunk = await response.content.read(8192)  # Read in 8kb chunks
                                if not chunk:
                                    break
                                f.write(chunk)
                
                # If download successful, rename to the correct file name
                os.replace(temp_path, file_path)
                logger.info(f"File successfully downloaded and moved to {file_path}")
                return file_path
                
            except Exception as e:
                # If any error occurs during download, delete the temporary file if it exists
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                        logger.info(f"Deleted temporary file {temp_path} after download failure")
                    except Exception as del_err:
                        logger.error(f"Failed to delete temporary file {temp_path}: {str(del_err)}")
                raise  # Re-raise the original exception
                
        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}", exc_info=True)
            return None
    
    async def get_folder_children(self, folder_id: str, page_id: Optional[int] = 0,
                                 page_capacity: Optional[int] = 20, type_filter: Optional[str] = "all",
                                 sort_by: Optional[str] = "date", 
                                 sort_direction: Optional[str] = "desc") -> Optional[Dict[str, Any]]:
        try:
            if not self.access_token:
                logger.error("Failed to get folder children: access_token is empty")
                return None
                
            logger.info(f"Getting children for folder ID {folder_id}")
            url = f"{self.open_host}{API_FOLDER_CHILDREN_PATH.replace('{id}', folder_id)}"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # Prepare query parameters
            params = {
                "page_id": page_id,
                "page_capacity": page_capacity,
                "type": type_filter,
                "sort_by": sort_by,
                "sort_direction": sort_direction
            }
                
            # Add query parameters to URL
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            url = f"{url}?{query_string}"
            
            # Send request to get folder children
            result = await self._send_request(url=url, method="GET", headers=headers)
            if not result:
                return None
            
            logger.info(f"Successfully obtained children for folder ID {folder_id}")
            return result
                
        except Exception as e:
            logger.error(f"Error getting folder children: {str(e)}", exc_info=True)
            return None
    
    async def get_personal_items(self, page_id: Optional[int] = 0,
                               page_capacity: Optional[int] = 20, type_filter: Optional[str] = "all",
                               sort_by: Optional[str] = "date", 
                               sort_direction: Optional[str] = "desc") -> Optional[Dict[str, Any]]:
        try:
            if not self.access_token:
                logger.error("Failed to get personal items: access_token is empty")
                return None
                
            logger.info("Getting personal items")
            url = f"{self.open_host}{API_PERSONAL_ITEMS_PATH}"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # Prepare query parameters
            params = {
                "page_id": page_id,
                "page_capacity": page_capacity,
                "type": type_filter,
                "sort_by": sort_by,
                "sort_direction": sort_direction
            }
                
            # Add query parameters to URL
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            url = f"{url}?{query_string}"
            
            # Send request to get personal items
            result = await self._send_request(url=url, method="GET", headers=headers)
            if not result:
                return None
            
            logger.info("Successfully obtained personal items")
            return result
                
        except Exception as e:
            logger.error(f"Error getting personal items: {str(e)}", exc_info=True)
            return None
    
    async def get_folder_info(self, folder_id: str) -> Optional[Dict[str, Any]]:
        """
        Get folder information
        
        Args:
            folder_id: Folder ID (if 0, represents personal space directory)
            
        Returns:
            Folder information or None (if request fails)
        """
        try:
            if not self.access_token:
                logger.error("Failed to get folder info: access_token is empty")
                return None
                
            logger.info(f"Getting folder info for folder ID {folder_id}")
            url = f"{self.open_host}{API_FOLDER_INFO_PATH.replace('{id}', folder_id)}"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # Send request to get folder information
            result = await self._send_request(url=url, method="GET", headers=headers)
            if not result:
                return None
            
            logger.info(f"Successfully obtained folder info for folder ID {folder_id}")
            return result
                
        except Exception as e:
            logger.error(f"Error getting folder info: {str(e)}", exc_info=True)
            return None
    
    async def search_items(self, query_words: str, search_type: Optional[str] = "all",
                         page_id: Optional[int] = 0, search_in_folder: Optional[str] = None,
                         query_filter: Optional[str] = "all", 
                         updated_time_range: Optional[str] = None) -> Optional[Dict[str, Any]]:
        try:
            if not self.access_token:
                logger.error("Failed to search items: access_token is empty")
                return None
                
            if not query_words:
                logger.error("Failed to search items: query_words is empty")
                return None
                
            logger.info(f"Searching for items with query: {query_words}")
            url = f"{self.open_host}{API_SEARCH_PATH}"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # Prepare query parameters
            params = {
                "query_words": query_words,
                "type": search_type,
                "page_id": page_id,
                "query_filter": query_filter
            }
            
            # Add optional parameters if provided
            if search_in_folder:
                params["search_in_folder"] = search_in_folder
            if updated_time_range:
                params["updated_time_range"] = updated_time_range
                
            # Add query parameters to URL
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            url = f"{url}?{query_string}"
            
            # Send request to search items
            result = await self._send_request(url=url, method="GET", headers=headers)
            if not result:
                return None
            
            logger.info(f"Successfully completed search for query: {query_words}, result:{result}")
            return result
                
        except Exception as e:
            logger.error(f"Error searching items: {str(e)}", exc_info=True)
            return None
    
    async def create_folder(self, name: str, parent_id: str, 
                           target_space_type: Optional[str] = None, 
                           target_space_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        try:
            if not self.access_token:
                logger.error("Failed to create folder: access_token is empty")
                return None
                
            if not name:
                logger.error("Failed to create folder: name is empty")
                return None
                
            if not parent_id and parent_id != "0":
                logger.error("Failed to create folder: parent_id is empty")
                return None
                
            # Validate folder name length
            if len(name) < 1 or len(name) > 222:
                logger.error(f"Failed to create folder: name length must be between 1 and 222 characters")
                return None
                
            # Check for invalid characters in folder name
            invalid_chars = ['/', '?', ':', '*', '"', '>', '<']
            if any(char in name for char in invalid_chars):
                logger.error(f"Failed to create folder: name contains invalid characters")
                return None
                
            logger.info(f"Creating folder '{name}' in parent folder {parent_id}")
            url = f"{self.open_host}{API_FOLDER_CREATE_PATH}"
            
            # Prepare request body
            params = {
                "name": name,
                "parent_id": parent_id
            }
            
            # Add target_space if parent_id is 0
            if parent_id == "0" or parent_id == 0:
                if target_space_type:
                    target_space = {"type": target_space_type}
                    
                    # Add target_space_id if type is department
                    if target_space_type == "department":
                        if not target_space_id:
                            logger.error("Failed to create folder: target_space_id is required when target_space_type is department")
                            return None
                        target_space["id"] = target_space_id
                        
                    params["target_space"] = target_space
            
            # Send request to create folder
            result = await self._api_request(
                operation_name="create folder",
                url=url,
                json_data=params,
                success_msg=f"Successfully created folder '{name}' in parent folder {parent_id}"
            )
            
            return result
                
        except Exception as e:
            logger.error(f"Error creating folder: {str(e)}", exc_info=True)
            return None
    
    async def cleanup(self) -> None:
        logger.info("Cleaning up FangCloud client resources")
        pass
