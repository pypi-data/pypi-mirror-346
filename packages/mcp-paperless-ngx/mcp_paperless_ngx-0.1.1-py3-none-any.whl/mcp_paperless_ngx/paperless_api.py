import asyncio
from typing import Dict, Any

from pypaperless import Paperless

from mcp_paperless_ngx.env import PAPERLESS_NGX_URI, PAPERLESS_NGX_TOKEN


class PaperlessAPI:
    def __init__(self):
        """Initialize the PaperlessAPI with URI and token from environment variables."""
        self.paperless = Paperless(PAPERLESS_NGX_URI, PAPERLESS_NGX_TOKEN)
        self._initialized = False

    async def __aenter__(self):
        """Async context manager entry point."""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit point."""
        await self.close()
    
    async def initialize(self):
        """Initialize the Paperless connection."""
        if not self._initialized:
            await self.paperless.initialize()
            self._initialized = True
        return self
        
    async def close(self):
        """Close the Paperless connection."""
        if self._initialized:
            await self.paperless.close()
            self._initialized = False
    
    async def get_document_ids(self):
        """Get all document IDs."""
        return await self.paperless.documents.all()
    
    async def get_document(self, doc_id):
        """Get a specific document by ID."""
        return await self.paperless.documents(doc_id)

    async def search_documents(self, query):
        """Search documents with a query string."""
        documents = []
        async for document in self.paperless.documents.search(query):
            documents.append(document)
        return documents
    
    def get_documents_pages(self):
        """Get a page iterator for documents.
        
        Use as:
        page_iter = aiter(api.get_documents_pages())
        page = await anext(page_iter)
        """
        return self.paperless.documents.pages()
        
    async def get_tag(self, tag_id):
        """Get a specific tag by ID."""
        return await self.paperless.tags(tag_id)
        
    async def get_correspondent(self, correspondent_id):
        """Get a specific correspondent by ID."""
        return await self.paperless.correspondents(correspondent_id)
        
    async def get_document_type(self, doc_type_id):
        """Get a specific document type by ID."""
        return await self.paperless.document_types(doc_type_id)
        
    async def get_all_tags(self) -> Dict[int, Any]:
        """Get all tags as a dictionary with tag ID as key."""
        tags = {}
        # Get all tags by iterating through the collection
        tag_list = []
        async for tag in self.paperless.tags:
            tag_list.append(tag)
        
        # Convert to dictionary with ID as key
        for tag in tag_list:
            tags[tag.id] = tag
        return tags
    
    async def get_all_correspondents(self) -> Dict[int, Any]:
        """Get all correspondents as a dictionary with correspondent ID as key."""
        correspondents = {}
        # Get all correspondents by iterating through the collection
        correspondent_list = []
        async for correspondent in self.paperless.correspondents:
            correspondent_list.append(correspondent)
        
        # Convert to dictionary with ID as key
        for correspondent in correspondent_list:
            correspondents[correspondent.id] = correspondent
        return correspondents
    
    async def get_all_document_types(self) -> Dict[int, Any]:
        """Get all document types as a dictionary with document type ID as key."""
        doc_types = {}
        # Get all document types by iterating through the collection
        doc_type_list = []
        async for doc_type in self.paperless.document_types:
            doc_type_list.append(doc_type)
        
        # Convert to dictionary with ID as key
        for doc_type in doc_type_list:
            doc_types[doc_type.id] = doc_type
        return doc_types
