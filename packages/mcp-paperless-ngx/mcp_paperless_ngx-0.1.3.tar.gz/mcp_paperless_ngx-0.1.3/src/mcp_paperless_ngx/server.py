import asyncio
import logging
from typing import List, Optional

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

from mcp_paperless_ngx.paperless_api import PaperlessAPI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server = Server("mcp-paperless-ngx")

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    List available resources from Paperless-ngx including:
    - Documents (with paperless://document/ID URI scheme)
    - Tags (with paperless://tag/ID URI scheme)
    - Correspondents (with paperless://correspondent/ID URI scheme)
    - Document Types (with paperless://document_type/ID URI scheme)
    
    Uses pagination for documents and caching for other entities.
    """
    resources = []
    
    try:
        async with PaperlessAPI() as api:
            # Fetch all entity data at once to populate cache
            await api.fetch_all_entities()
            
            # Get data from cache
            tags_cache = api._cache["tags"]
            correspondents = api._cache["correspondents"]
            doc_types = api._cache["document_types"]
            
            # Process tags
            try:
                if tags_cache:
                    for tag_id, tag in tags_cache.items():
                        resources.append(
                            types.Resource(
                                uri=AnyUrl(f"paperless://tag/{tag_id}"),
                                name=f"Tag: {tag.name}",
                                description=f"Tag ID: {tag_id}",
                                mimeType="text/plain",
                            )
                        )
            except Exception as e:
                logger.error(f"Error processing tags: {e}")
            
            # Process correspondents
            try:
                if correspondents:
                    for corr_id, corr in correspondents.items():
                        resources.append(
                            types.Resource(
                                uri=AnyUrl(f"paperless://correspondent/{corr_id}"),
                                name=f"Correspondent: {corr.name}",
                                description=f"Correspondent ID: {corr_id}",
                                mimeType="text/plain",
                            )
                        )
            except Exception as e:
                logger.error(f"Error processing correspondents: {e}")
            
            # Process document types
            try:
                if doc_types:
                    for type_id, doc_type in doc_types.items():
                        resources.append(
                            types.Resource(
                                uri=AnyUrl(f"paperless://document_type/{type_id}"),
                                name=f"Document Type: {doc_type.name}",
                                description=f"Document Type ID: {type_id}",
                                mimeType="text/plain",
                            )
                        )
            except Exception as e:
                logger.error(f"Error processing document types: {e}")
            
            # Use the pagination feature to get documents page by page
            page_iter = aiter(api.get_documents_pages())
            
            try:
                while True:
                    page = await anext(page_iter)
                    
                    # Process all documents in this page
                    for document in page.items:
                        try:
                            # Get the document name (title or filename or ID as fallback)
                            doc_name = document.title or document.filename
                            if not doc_name:
                                doc_name = f"Document #{document.id}"
                            
                            # Create description based on available metadata
                            description_parts = []
                            
                            # Always include created date if available
                            if hasattr(document, 'created') and document.created:
                                description_parts.append(f"Created: {document.created}")
                            
                            # Get tag names from cache instead of just counting them
                            if hasattr(document, 'tags') and document.tags:
                                tag_names = []
                                for tag_id in document.tags:
                                    tag = tags_cache.get(tag_id)
                                    if tag:
                                        tag_names.append(tag.name)
                                if tag_names:
                                    description_parts.append(f"Tags: {', '.join(tag_names)}")
                            
                            # Add first 50 characters of content if available
                            if hasattr(document, 'content') and document.content:
                                content_preview = document.content[:50]
                                if len(document.content) > 50:
                                    content_preview += "..."
                                description_parts.append(f"Preview: {content_preview}")
                            
                            description = ", ".join(description_parts) if description_parts else "No additional metadata"
                            
                            # Determine the MIME type
                            mime_type = "application/pdf"  # Default
                            if hasattr(document, 'original_mime_type') and document.original_mime_type:
                                mime_type = document.original_mime_type
                            
                            resources.append(
                                types.Resource(
                                    uri=AnyUrl(f"paperless://document/{document.id}"),
                                    name=f"Document #{document.id}: {doc_name}",
                                    description=description,
                                    mimeType=mime_type,
                                )
                            )
                        except Exception as e:
                            # Log the error but continue with other documents
                            logger.error(f"Error processing document {getattr(document, 'id', 'unknown')}: {e}")
            except StopAsyncIteration:
                # No more pages
                pass
    except Exception as e:
        logger.error(f"Error listing Paperless resources: {e}")
        # Return empty list if Paperless API is unavailable
        return []
                
    return resources

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    Read a specific resource's content by its URI.
    Supports various paperless resource types:
    - paperless://document/ID - Document details
    - paperless://tag/ID - Tag details
    - paperless://correspondent/ID - Correspondent details
    - paperless://document_type/ID - Document type details
    """
    # Handle paperless URIs
    if uri.scheme == "paperless":
        path = uri.path
        logger.info(f"Processing paperless URI with path: {path}")
        
        # Extract the ID by removing slashes
        resource_id = path.replace("/", "")
        
        if uri.host == "document":
            try:
                async with PaperlessAPI() as api:
                    # Fetch all entity data at once to populate cache
                    await api.fetch_all_entities()
                    
                    # Get data from cache
                    tags_cache = api._cache["tags"]
                    correspondents_cache = api._cache["correspondents"]
                    doc_types_cache = api._cache["document_types"]
                    
                    document = await api.get_document(resource_id)
                    
                    # Build a formatted text representation of the document
                    details = [
                        f"**Document ID:** {document.id}",
                        f"**Archive serial number:** {document.archive_serial_number or 'N/A'}",
                        f"**Title:** {document.title or 'N/A'}",
                        f"**Original filename:** {document.original_file_name or 'N/A'}",
                        f"**Archived filename:** {document.archived_file_name or 'N/A'}",
                    ]
                    
                    # Add additional details if available
                    if hasattr(document, 'created') and document.created:
                        details.append(f"**Created:** {document.created}")
                    if hasattr(document, 'modified') and document.modified:
                        details.append(f"**Modified:** {document.modified}")
                    if hasattr(document, 'added') and document.added:
                        details.append(f"**Added:** {document.added}")
                    
                    # Add correspondent if available - use cache
                    if hasattr(document, 'correspondent') and document.correspondent:
                        correspondent = correspondents_cache.get(document.correspondent)
                        if correspondent:
                            details.append(f"**Correspondent:** {correspondent.name}")
                        else:
                            details.append(f"**Correspondent ID:** {document.correspondent}")
                    
                    # Add document type if available - use cache
                    if hasattr(document, 'document_type') and document.document_type:
                        doc_type = doc_types_cache.get(document.document_type)
                        if doc_type:
                            details.append(f"**Document Type:** {doc_type.name}")
                        else:
                            details.append(f"**Document Type ID:** {document.document_type}")
                    
                    # Add tags if available - use cache
                    if hasattr(document, 'tags') and document.tags:
                        tag_names = []
                        for tag_id in document.tags:
                            tag = tags_cache.get(tag_id)
                            if tag:
                                tag_names.append(tag.name)
                            else:
                                tag_names.append(f"Tag #{tag_id}")
                        
                        if tag_names:
                            details.append(f"**Tags:** {', '.join(tag_names)}")
                    
                    # Add content snippet if available
                    if hasattr(document, 'content') and document.content:
                        details.append(f"\n**Content**\n```\n{document.content}\n```")
                    
                    return "\n".join(details)
            except Exception as e:
                logger.error(f"Error reading document {resource_id}: {e}")
                return f"Error reading document {resource_id}: {str(e)}"
                
        elif uri.host == "tag":
            try:
                async with PaperlessAPI() as api:
                    tag = await api.get_tag(resource_id)
                    details = [
                        f"**Tag ID:** {tag.id}",
                        f"**Name:** {tag.name}",
                        f"**Color:** {getattr(tag, 'color', 'N/A')}",
                    ]
                    
                    if hasattr(tag, 'match') and tag.match:
                        details.append(f"**Match Pattern:** {tag.match}")
                    
                    if hasattr(tag, 'is_inbox_tag') and tag.is_inbox_tag:
                        details.append(f"**Is Inbox Tag:** Yes")
                    
                    return "\n".join(details)
            except Exception as e:
                logger.error(f"Error reading tag {resource_id}: {e}")
                return f"Error reading tag {resource_id}: {str(e)}"
                
        elif uri.host == "correspondent":
            try:
                async with PaperlessAPI() as api:
                    correspondent = await api.get_correspondent(resource_id)
                    details = [
                        f"**Correspondent ID:** {correspondent.id}",
                        f"**Name:** {correspondent.name}",
                    ]
                    
                    if hasattr(correspondent, 'match') and correspondent.match:
                        details.append(f"**Match Pattern:** {correspondent.match}")
                    
                    if hasattr(correspondent, 'is_insensitive') and correspondent.is_insensitive:
                        details.append(f"**Case Insensitive Matching:** Yes")
                    
                    return "\n".join(details)
            except Exception as e:
                logger.error(f"Error reading correspondent {resource_id}: {e}")
                return f"Error reading correspondent {resource_id}: {str(e)}"
                
        elif uri.host == "document_type":
            try:
                async with PaperlessAPI() as api:
                    doc_type = await api.get_document_type(resource_id)
                    details = [
                        f"**Document Type ID:** {doc_type.id}",
                        f"**Name:** {doc_type.name}",
                    ]
                    
                    if hasattr(doc_type, 'match') and doc_type.match:
                        details.append(f"**Match Pattern:** {doc_type.match}")
                    
                    if hasattr(doc_type, 'is_insensitive') and doc_type.is_insensitive:
                        details.append(f"**Case Insensitive Matching:** Yes")
                    
                    return "\n".join(details)
            except Exception as e:
                logger.error(f"Error reading document type {resource_id}: {e}")
                return f"Error reading document type {resource_id}: {str(e)}"
        
        else:
            # Unsupported host
            raise ValueError(f"Invalid paperless URI: {uri} (host: {uri.host})")
    
    raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """
    List available prompts.
    Each prompt can have optional arguments to customize its behavior.
    """
    return [
        types.Prompt(
            name="summarize-documents",
            description="Creates a summary of documents using Whoosh query language for filtering",
            arguments=[
                types.PromptArgument(
                    name="query",
                    description="""Search query to filter documents using Whoosh query language (optional)
Examples:
- **Simple search:** invoice receipt
- **Field-specific:** type:invoice tag:important
- **Date range:** created:[2020 to 2023]
- **Logical operators:** invoice AND (paid OR unpaid)
- **Wildcards:** electr*""",
                    required=False,
                ),
                types.PromptArgument(
                    name="style",
                    description="Style of the summary (brief/detailed)",
                    required=False,
                )
            ],
        )
    ]

@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """
    Generate a prompt by combining arguments with server state.
    The prompt includes document data or notes based on the requested prompt.
    """
    if name == "summarize-documents":
        style = (arguments or {}).get("style", "brief")
        query = (arguments or {}).get("query", "")
        detail_prompt = " Give extensive details." if style == "detailed" else ""
        
        try:
            document_summaries = []
            async with PaperlessAPI() as api:
                # Fetch all entity data at once to populate cache
                await api.fetch_all_entities()
                
                # Get data from cache
                tags_cache = api._cache["tags"]
                correspondents_cache = api._cache["correspondents"]
                doc_types_cache = api._cache["document_types"]
                
                # Use search if there's a query
                if query:
                    documents = await api.search_documents(query)
                    # Limit to first 10 documents for search results to avoid huge prompts
                    documents = documents[:10] if len(documents) > 10 else documents
                    
                    for doc in documents:
                        doc_name = doc.title or doc.filename or f"Doc #{doc.id}"
                        metadata = []
                        
                        if hasattr(doc, 'created') and doc.created:
                            metadata.append(f"**Created:** {doc.created}")
                        
                        # Use cache for correspondent
                        if hasattr(doc, 'correspondent') and doc.correspondent:
                            correspondent = correspondents_cache.get(doc.correspondent)
                            if correspondent:
                                metadata.append(f"**Correspondent:** {correspondent.name}")
                            else:
                                metadata.append(f"**Correspondent ID:** {doc.correspondent}")
                        
                        # Use cache for document type
                        if hasattr(doc, 'document_type') and doc.document_type:
                            doc_type = doc_types_cache.get(doc.document_type)
                            if doc_type:
                                metadata.append(f"**Document Type:** {doc_type.name}")
                            else:
                                metadata.append(f"**Document Type ID:** {doc.document_type}")
                        
                        # Use cache for tags
                        if hasattr(doc, 'tags') and doc.tags:
                            tag_names = []
                            for tag_id in doc.tags:
                                tag = tags_cache.get(tag_id)
                                if tag:
                                    tag_names.append(tag.name)
                                else:
                                    tag_names.append(f"Tag #{tag_id}")
                            if tag_names:
                                metadata.append(f"**Tags:** {', '.join(tag_names)}")
                        
                        meta_str = "\n  ".join(metadata) if metadata else "No metadata"
                        
                        content_preview = ""
                        if hasattr(doc, 'content') and doc.content:
                            content_text = doc.content[:500] + "..." if len(doc.content) > 500 else doc.content
                            # Process content text to ensure each line is properly indented
                            content_lines = content_text.split('\n')
                            indented_content = '\n  '.join(content_lines)
                            content_preview = f"\n  **Content:** {indented_content}"
                        
                        document_summaries.append(f"- **Document #{doc.id}:** {doc_name}\n  **URL:** paperless://document/{doc.id}\n  {meta_str}{content_preview}")
                else:
                    # Use pagination for listing all documents
                    page_iter = aiter(api.get_documents_pages())
                    document_count = 0
                    
                    try:
                        while document_count < 10:  # Limit to 10 documents total
                            page = await anext(page_iter)
                            
                            for doc in page.items:
                                if document_count >= 10:
                                    break
                                    
                                doc_name = doc.title or doc.filename or f"Doc #{doc.id}"
                                metadata = []
                                
                                if hasattr(doc, 'created') and doc.created:
                                    metadata.append(f"**Created:** {doc.created}")
                                
                                # Use cache for correspondent
                                if hasattr(doc, 'correspondent') and doc.correspondent:
                                    correspondent = correspondents_cache.get(doc.correspondent)
                                    if correspondent:
                                        metadata.append(f"**Correspondent:** {correspondent.name}")
                                    else:
                                        metadata.append(f"**Correspondent ID:** {doc.correspondent}")
                                
                                # Use cache for document type
                                if hasattr(doc, 'document_type') and doc.document_type:
                                    doc_type = doc_types_cache.get(doc.document_type)
                                    if doc_type:
                                        metadata.append(f"**Document Type:** {doc_type.name}")
                                    else:
                                        metadata.append(f"**Document Type ID:** {doc.document_type}")
                                
                                # Use cache for tags
                                if hasattr(doc, 'tags') and doc.tags:
                                    tag_names = []
                                    for tag_id in doc.tags:
                                        tag = tags_cache.get(tag_id)
                                        if tag:
                                            tag_names.append(tag.name)
                                        else:
                                            tag_names.append(f"Tag #{tag_id}")
                                    if tag_names:
                                        metadata.append(f"**Tags:** {', '.join(tag_names)}")
                                
                                meta_str = "\n  ".join(metadata) if metadata else "No metadata"
                                
                                content_preview = ""
                                if hasattr(doc, 'content') and doc.content:
                                    content_text = doc.content[:500] + "..." if len(doc.content) > 500 else doc.content
                                    # Process content text to ensure each line is properly indented
                                    content_lines = content_text.split('\n')
                                    indented_content = '\n  '.join(content_lines)
                                    content_preview = f"\n  **Content:** {indented_content}"
                                
                                document_summaries.append(f"- **Document #{doc.id}:** {doc_name}\n  **URL:** paperless://document/{doc.id}\n  {meta_str}{content_preview}")
                                document_count += 1
                                
                            # If we already have 10 docs, break out of the pagination loop
                            if document_count >= 10:
                                break
                    except StopAsyncIteration:
                        # No more pages
                        pass
            
            if not document_summaries:
                document_summaries = ["No documents found"]
            
            # Prepare query explanation if a query was used
            query_explanation = ""
            if query:
                query_explanation = f"""
The documents were filtered using the Whoosh query language with query: '{query}'

Note on Paperless search: Paperless uses the Whoosh query language which supports:
- Field-specific searches (type:invoice, correspondent:university)
- Date ranges (created:[2020 to 2023])
- Logical operators (AND, OR, NOT)
- Wildcards for inexact matching (electr*)
"""
            
            return types.GetPromptResult(
                description="Summarize the documents",
                messages=[
                    types.PromptMessage(
                        role="user",
                        content=types.TextContent(
                            type="text",
                            text=f"Here are the documents to summarize{' matching query: ' + query if query else ''}:{detail_prompt}\n{query_explanation}\n"
                            + "## Results:\n"
                            + "\n".join(document_summaries),
                        ),
                    )
                ],
            )
        except Exception as e:
            logger.error(f"Error generating document summary prompt: {e}")
            return types.GetPromptResult(
                description="Error summarizing documents",
                messages=[
                    types.PromptMessage(
                        role="user",
                        content=types.TextContent(
                            type="text",
                            text=f"Error accessing documents: {str(e)}",
                        ),
                    )
                ],
            )
    
    
    else:
        raise ValueError(f"Unknown prompt: {name}")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="search-documents",
            description="""Search for documents in Paperless-ngx using Whoosh query language.
            
Paperless-ngx uses Whoosh (https://whoosh.readthedocs.io/en/latest/querylang.html) for its search engine.
You can use the following query syntax:

1. Basic keyword search:
   - invoice receipt (matches documents containing both words)

2. Field-specific searches:
   - correspondent:university (matches documents from a specific correspondent)
   - type:invoice (matches documents of a specific type)
   - tag:important (matches documents with a specific tag)

3. Date-based searches:
   - created:[2020 to 2023] (date range)
   - added:yesterday (relative date)
   - modified:today (relative date)

4. Logical expressions:
   - invoice AND (paid OR unpaid) (combines terms with logical operators)

5. Inexact matching:
   - electr* (wildcard search, matches 'electric', 'electronics', etc.)

Documents are matched against content, title, correspondent, type and tags.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query using Whoosh query language"
                    },
                },
                "required": ["query"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    if name == "search-documents":
        if not arguments:
            raise ValueError("Missing arguments")
        
        query = arguments.get("query")
        if not query:
            raise ValueError("Missing query")
        
        try:
            async with PaperlessAPI() as api:
                # Fetch all entity data at once to populate cache
                await api.fetch_all_entities()
                
                # Get data from cache
                tags_cache = api._cache["tags"]
                correspondents_cache = api._cache["correspondents"]
                doc_types_cache = api._cache["document_types"]
                
                documents = await api.search_documents(query)
                
                if not documents:
                    return [
                        types.TextContent(
                            type="text",
                            text=f"No documents found matching query: {query}",
                        )
                    ]
                
                # Add search information about Whoosh query language
                results = [
                    f"Found {len(documents)} documents matching query: {query}\n",
                    f"## Results:",
                ]
                
                for doc in documents:
                    doc_name = doc.title or doc.filename or f"Doc #{doc.id}"
                    doc_info = [f"- **Document #{doc.id}:** {doc_name}"]
                    doc_info.append(f"  **URL:** paperless://document/{doc.id}")
                    
                    if hasattr(doc, 'created') and doc.created:
                        doc_info.append(f"  **Created:** {doc.created}")
                    if hasattr(doc, 'modified') and doc.modified:
                        doc_info.append(f"  **Modified:** {doc.modified}")
                    if hasattr(doc, 'added') and doc.added:
                        doc_info.append(f"  **Added:** {doc.added}")
                    
                    # Use correspondent cache instead of individual API calls
                    if hasattr(doc, 'correspondent') and doc.correspondent:
                        correspondent = correspondents_cache.get(doc.correspondent)
                        if correspondent:
                            doc_info.append(f"  **Correspondent:** {correspondent.name}")
                        else:
                            doc_info.append(f"  **Correspondent ID:** {doc.correspondent}")
                    
                    # Use document type cache instead of individual API calls
                    if hasattr(doc, 'document_type') and doc.document_type:
                        doc_type = doc_types_cache.get(doc.document_type)
                        if doc_type:
                            doc_info.append(f"  **Document Type:** {doc_type.name}")
                        else:
                            doc_info.append(f"  **Document Type ID:** {doc.document_type}")
                    
                    # Use tags cache instead of individual API calls
                    if hasattr(doc, 'tags') and doc.tags:
                        tag_names = []
                        for tag_id in doc.tags:
                            tag = tags_cache.get(tag_id)
                            if tag:
                                tag_names.append(tag.name)
                            else:
                                tag_names.append(f"Tag #{tag_id}")
                        
                        if tag_names:
                            doc_info.append(f"  **Tags:** {', '.join(tag_names)}")
                    
                    # Add content preview if available
                    if hasattr(doc, 'content') and doc.content:
                        content_text = doc.content[:250] + "..." if len(doc.content) > 250 else doc.content
                        # Process content text to ensure each line is properly indented
                        content_lines = content_text.split('\n')
                        indented_content = '\n  '.join(content_lines)
                        doc_info.append(f"  **Content:** {indented_content}")
                    
                    results.append("\n".join(doc_info))
                
                return [
                    types.TextContent(
                        type="text",
                        text="\n".join(results),
                    )
                ]
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return [
                types.TextContent(
                    type="text",
                    text=f"Error searching documents: {str(e)}",
                )
            ]
    
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-paperless-ngx",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
