# FangCloud MCP

FangCloud MCP 是一个 Model Context Protocol (MCP) 服务器实现，提供与 FangCloud 云存储服务的集成。通过该服务，AI 助手可以直接与 FangCloud 进行交互，实现文件和文件夹的管理操作。

## 功能特点

FangCloud MCP 提供以下功能：

- 文件操作
  - 获取文件信息
  - 上传文件
  - 下载文件
  - 更新文件名称和描述
- 文件夹操作
  - 获取文件夹信息
  - 创建文件夹
  - 列出文件夹内容
  - 列出个人空间项目
- 搜索功能
  - 按关键词搜索文件和文件夹
  - 支持多种过滤和排序选项

## 安装要求

- Python 3.12 或更高版本
- 依赖项:
  - aiohttp >= 3.8.6
  - mcp[cli] >= 1.7.1

## 安装方法

### 从 PyPI 安装（推荐）

```bash
pip install fangcloud-mcp
```

## 使用方法

### 启动服务器

服务器需要 FangCloud API 访问令牌才能运行：

```bash
fangcloud --access_token <your-access-token>
```

或者使用简短参数形式：

```bash
fangcloud -c <your-access-token>
```

### 日志

服务器日志保存在`fangcloud-mcp.log`文件中，同时也会输出到控制台。

## API 参考

### 文件操作

#### 获取文件信息

```python
get_file_info(file_id: str)
```

获取指定文件 ID 的详细信息。

#### 上传文件

```python
upload_file(parent_folder_id: str, local_file_path: str)
```

将本地文件上传到指定的 FangCloud 文件夹。

#### 下载文件

```python
download_file(file_id: str, local_path: str)
```

下载指定 ID 的文件到本地路径。

#### 更新文件

```python
update_file(file_id: str, name: Optional[str] = None, description: Optional[str] = None)
```

更新文件的名称和/或描述。

### 文件夹操作

#### 获取文件夹信息

```python
get_folder_info(folder_id: str)
```

获取指定文件夹 ID 的详细信息。

#### 创建文件夹

```python
create_folder(name: str, parent_id: str, target_space_type: Optional[str] = None, target_space_id: Optional[str] = None)
```

在指定的父文件夹中创建新文件夹。

#### 列出文件夹内容

```python
list_folder_contents(folder_id: str, page_id: Optional[int] = 0, page_capacity: Optional[int] = 20, type_filter: Optional[str] = "all", sort_by: Optional[str] = "date", sort_direction: Optional[str] = "desc")
```

列出指定文件夹中的文件和子文件夹。

#### 列出个人空间项目

```python
list_personal_items(page_id: Optional[int] = 0, page_capacity: Optional[int] = 20, type_filter: Optional[str] = "all", sort_by: Optional[str] = "date", sort_direction: Optional[str] = "desc")
```

列出个人空间中的文件和文件夹。

### 搜索功能

```python
search_items(query_words: str, search_type: Optional[str] = "all", page_id: Optional[int] = 0, search_in_folder: Optional[str] = None, query_filter: Optional[str] = "all", updated_time_range: Optional[str] = None)
```

搜索文件和文件夹，支持多种过滤选项。

## 开发

### 项目结构

- `fangcloud.py` - 主入口点，包含 MCP 服务器实现和工具函数
- `fangcloud_api.py` - FangCloud API 客户端实现
- `pyproject.toml` - 项目配置和依赖声明

### 日志记录

项目使用 Python 的标准 logging 模块记录日志，配置为同时输出到控制台和文件。

## 许可证

MIT License

Copyright (c) 2025 FangCloud Developer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
