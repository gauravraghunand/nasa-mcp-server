#!/usr/bin/env python3
"""
NASA Image and Video Library MCP Server - Access NASA's vast collection of images, videos, and audio files
"""
import os
import sys
import logging
from datetime import datetime, timezone
import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("nasa-server")

# Initialize MCP server - NO PROMPT PARAMETER!
mcp = FastMCP("nasa")

# Configuration
NASA_API_BASE = "https://images-api.nasa.gov"

# === UTILITY FUNCTIONS ===

def format_media_result(item):
    """Format a single media item for display."""
    data = item.get("data", [{}])[0]
    links = item.get("links", [])
    
    # Get preview link if available
    preview_link = ""
    for link in links:
        if link.get("rel") == "preview":
            preview_link = link.get("href", "")
            break
    
    # Format the result
    result = f"""📸 **{data.get('title', 'Untitled')}**
🆔 NASA ID: {data.get('nasa_id', 'N/A')}
📅 Date: {data.get('date_created', 'Unknown')}
🏢 Center: {data.get('center', 'Unknown')}
📝 Media Type: {data.get('media_type', 'Unknown')}
📖 Description: {data.get('description', 'No description available')[:200]}...
🔍 Preview: {preview_link}
"""
    
    # Add keywords if available
    keywords = data.get('keywords', [])
    if keywords:
        result += f"🏷️ Keywords: {', '.join(keywords[:5])}"
        if len(keywords) > 5:
            result += f" (+{len(keywords)-5} more)"
    
    return result

def format_asset_manifest(items):
    """Format asset manifest for display."""
    result = "📁 **Available Asset Files:**\n\n"
    
    for item in items:
        href = item.get("href", "")
        if "~orig" in href:
            result += f"🖼️ Original: {href}\n"
        elif "~medium" in href:
            result += f"📷 Medium: {href}\n"
        elif "~small" in href:
            result += f"🔸 Small: {href}\n"
        elif "~thumb" in href:
            result += f"👁️ Thumbnail: {href}\n"
        elif "metadata.json" in href:
            result += f"📋 Metadata: {href}\n"
        else:
            result += f"📄 File: {href}\n"
    
    return result

# === MCP TOOLS ===

@mcp.tool()
async def search_nasa_media(query: str = "", media_type: str = "", center: str = "", year_start: str = "", year_end: str = "", page: str = "1", page_size: str = "10") -> str:
    """Search NASA's image and video library for media assets based on your query."""
    logger.info(f"Searching NASA media with query: {query}")
    
    if not query.strip():
        return "❌ Error: Search query is required"
    
    try:
        # Convert page and page_size to integers
        page_int = int(page) if page.strip() else 1
        page_size_int = int(page_size) if page_size.strip() else 10
        
        # Limit page size to reasonable bounds
        if page_size_int > 100:
            page_size_int = 100
        elif page_size_int < 1:
            page_size_int = 10
            
        # Build parameters
        params = {
            "q": query.strip(),
            "page": page_int,
            "page_size": page_size_int
        }
        
        if media_type.strip():
            params["media_type"] = media_type.strip()
        if center.strip():
            params["center"] = center.strip()
        if year_start.strip():
            params["year_start"] = year_start.strip()
        if year_end.strip():
            params["year_end"] = year_end.strip()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{NASA_API_BASE}/search", params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            collection = data.get("collection", {})
            items = collection.get("items", [])
            metadata = collection.get("metadata", {})
            total_hits = metadata.get("total_hits", 0)
            
            if not items:
                return f"🔍 No results found for query: '{query}'"
            
            result = f"🚀 **NASA Media Search Results**\n\n"
            result += f"📊 Found {total_hits} total results (showing page {page_int})\n\n"
            
            for i, item in enumerate(items, 1):
                result += f"**Result {i}:**\n{format_media_result(item)}\n\n"
            
            # Add pagination info
            links = collection.get("links", [])
            next_link = next((link for link in links if link.get("rel") == "next"), None)
            if next_link:
                result += f"➡️ More results available - use page {page_int + 1} to see next page"
            
            return result
            
    except ValueError as e:
        return f"❌ Error: Invalid page or page_size parameter: {str(e)}"
    except httpx.HTTPStatusError as e:
        return f"❌ NASA API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Search error: {e}")
        return f"❌ Error searching NASA media: {str(e)}"

@mcp.tool()
async def get_nasa_asset(nasa_id: str = "") -> str:
    """Get available files and formats for a specific NASA media asset by its NASA ID."""
    logger.info(f"Getting NASA asset: {nasa_id}")
    
    if not nasa_id.strip():
        return "❌ Error: NASA ID is required"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{NASA_API_BASE}/asset/{nasa_id.strip()}", timeout=30)
            response.raise_for_status()
            data = response.json()
            
            collection = data.get("collection", {})
            items = collection.get("items", [])
            
            if not items:
                return f"❌ No asset files found for NASA ID: {nasa_id}"
            
            result = f"🚀 **NASA Asset: {nasa_id}**\n\n"
            result += format_asset_manifest(items)
            
            return result
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"❌ NASA ID not found: {nasa_id}"
        return f"❌ NASA API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Asset retrieval error: {e}")
        return f"❌ Error retrieving NASA asset: {str(e)}"

@mcp.tool()
async def get_nasa_metadata(nasa_id: str = "") -> str:
    """Get the metadata file location for a specific NASA media asset."""
    logger.info(f"Getting NASA metadata for: {nasa_id}")
    
    if not nasa_id.strip():
        return "❌ Error: NASA ID is required"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{NASA_API_BASE}/metadata/{nasa_id.strip()}", timeout=30)
            response.raise_for_status()
            data = response.json()
            
            location = data.get("location", "")
            
            if not location:
                return f"❌ No metadata location found for NASA ID: {nasa_id}"
            
            result = f"📋 **Metadata for NASA Asset: {nasa_id}**\n\n"
            result += f"📄 Metadata JSON Location: {location}\n\n"
            result += "💡 Download this JSON file to access detailed metadata about the asset including EXIF data, technical specifications, and extended descriptions."
            
            return result
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"❌ NASA ID not found: {nasa_id}"
        return f"❌ NASA API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Metadata retrieval error: {e}")
        return f"❌ Error retrieving NASA metadata: {str(e)}"

@mcp.tool()
async def get_nasa_captions(nasa_id: str = "") -> str:
    """Get caption file location for a NASA video asset (VTT/SRT subtitles)."""
    logger.info(f"Getting NASA captions for: {nasa_id}")
    
    if not nasa_id.strip():
        return "❌ Error: NASA ID is required"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{NASA_API_BASE}/captions/{nasa_id.strip()}", timeout=30)
            response.raise_for_status()
            data = response.json()
            
            location = data.get("location", "")
            
            if not location:
                return f"❌ No captions found for NASA ID: {nasa_id} (may not be a video or captions may not be available)"
            
            result = f"🎬 **Video Captions for NASA Asset: {nasa_id}**\n\n"
            result += f"📝 Caption File Location: {location}\n\n"
            result += "💡 Download this VTT or SRT file to access video captions/subtitles."
            
            return result
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"❌ NASA ID not found or no captions available: {nasa_id}"
        return f"❌ NASA API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Captions retrieval error: {e}")
        return f"❌ Error retrieving NASA captions: {str(e)}"

@mcp.tool()
async def browse_nasa_album(album_name: str = "", page: str = "1") -> str:
    """Browse contents of a NASA media album by name (e.g., 'apollo', 'hubble', 'mars')."""
    logger.info(f"Browsing NASA album: {album_name}")
    
    if not album_name.strip():
        return "❌ Error: Album name is required (examples: 'apollo', 'hubble', 'mars', 'iss')"
    
    try:
        page_int = int(page) if page.strip() else 1
        
        params = {"page": page_int} if page_int > 1 else {}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{NASA_API_BASE}/album/{album_name.strip()}", params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            collection = data.get("collection", {})
            items = collection.get("items", [])
            metadata = collection.get("metadata", {})
            total_hits = metadata.get("total_hits", 0)
            
            if not items:
                return f"❌ Album not found or empty: '{album_name}'. Try albums like 'apollo', 'hubble', 'mars', or 'iss'"
            
            result = f"📚 **NASA Album: {album_name}**\n\n"
            result += f"📊 Total items in album: {total_hits} (showing page {page_int})\n\n"
            
            for i, item in enumerate(items[:5], 1):  # Show first 5 items
                result += f"**Item {i}:**\n{format_media_result(item)}\n\n"
            
            if len(items) > 5:
                result += f"... and {len(items) - 5} more items on this page\n\n"
            
            # Add pagination info
            links = collection.get("links", [])
            next_link = next((link for link in links if link.get("rel") == "next"), None)
            if next_link:
                result += f"➡️ More items available - use page {page_int + 1} to see next page"
            
            return result
            
    except ValueError as e:
        return f"❌ Error: Invalid page parameter: {str(e)}"
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"❌ Album not found: '{album_name}'. Try albums like 'apollo', 'hubble', 'mars', or 'iss'"
        return f"❌ NASA API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Album browsing error: {e}")
        return f"❌ Error browsing NASA album: {str(e)}"

# === SERVER STARTUP ===
if __name__ == "__main__":
    logger.info("Starting NASA Image and Video Library MCP server...")
    
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)