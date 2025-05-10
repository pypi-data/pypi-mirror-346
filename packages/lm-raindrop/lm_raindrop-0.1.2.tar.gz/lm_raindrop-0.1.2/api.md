# Search

Types:

```python
from lm_raindrop.types import SearchResponse, TextResult
```

Methods:

- <code title="get /v1/search">client.search.<a href="./src/lm_raindrop/resources/search.py">retrieve</a>(\*\*<a href="src/lm_raindrop/types/search_retrieve_params.py">params</a>) -> <a href="./src/lm_raindrop/types/text_result.py">SyncSearchPage[TextResult]</a></code>
- <code title="post /v1/search">client.search.<a href="./src/lm_raindrop/resources/search.py">find</a>(\*\*<a href="src/lm_raindrop/types/search_find_params.py">params</a>) -> <a href="./src/lm_raindrop/types/search_response.py">SearchResponse</a></code>

# DocumentQuery

Types:

```python
from lm_raindrop.types import DocumentQueryAskResponse
```

Methods:

- <code title="post /v1/document_query">client.document_query.<a href="./src/lm_raindrop/resources/document_query.py">ask</a>(\*\*<a href="src/lm_raindrop/types/document_query_ask_params.py">params</a>) -> <a href="./src/lm_raindrop/types/document_query_ask_response.py">DocumentQueryAskResponse</a></code>

# ChunkSearch

Types:

```python
from lm_raindrop.types import ChunkSearchFindResponse
```

Methods:

- <code title="post /v1/chunk_search">client.chunk_search.<a href="./src/lm_raindrop/resources/chunk_search.py">find</a>(\*\*<a href="src/lm_raindrop/types/chunk_search_find_params.py">params</a>) -> <a href="./src/lm_raindrop/types/chunk_search_find_response.py">ChunkSearchFindResponse</a></code>

# SummarizePage

Types:

```python
from lm_raindrop.types import SummarizePageCreateResponse
```

Methods:

- <code title="post /v1/summarize_page">client.summarize_page.<a href="./src/lm_raindrop/resources/summarize_page.py">create</a>(\*\*<a href="src/lm_raindrop/types/summarize_page_create_params.py">params</a>) -> <a href="./src/lm_raindrop/types/summarize_page_create_response.py">SummarizePageCreateResponse</a></code>

# StorageObject

Types:

```python
from lm_raindrop.types import (
    StorageObjectListResponse,
    StorageObjectDeleteResponse,
    StorageObjectUploadResponse,
)
```

Methods:

- <code title="get /v1/object/{bucket}">client.storage_object.<a href="./src/lm_raindrop/resources/storage_object.py">list</a>(bucket) -> <a href="./src/lm_raindrop/types/storage_object_list_response.py">StorageObjectListResponse</a></code>
- <code title="delete /v1/object/{bucket}/{key}">client.storage_object.<a href="./src/lm_raindrop/resources/storage_object.py">delete</a>(key, \*, bucket) -> <a href="./src/lm_raindrop/types/storage_object_delete_response.py">StorageObjectDeleteResponse</a></code>
- <code title="get /v1/object/{bucket}/{key}">client.storage_object.<a href="./src/lm_raindrop/resources/storage_object.py">download</a>(key, \*, bucket) -> BinaryAPIResponse</code>
- <code title="put /v1/object/{bucket}/{key}">client.storage_object.<a href="./src/lm_raindrop/resources/storage_object.py">upload</a>(key, \*, bucket, \*\*<a href="src/lm_raindrop/types/storage_object_upload_params.py">params</a>) -> <a href="./src/lm_raindrop/types/storage_object_upload_response.py">StorageObjectUploadResponse</a></code>
