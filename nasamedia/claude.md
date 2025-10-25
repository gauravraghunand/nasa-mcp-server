# NASA Image and Video Library MCP Server - Implementation Guide

## Overview

This MCP server provides Claude with the ability to search and access NASA's extensive media collection through their public Image and Video Library API. The server implements five core tools that allow comprehensive interaction with NASA's digital assets.

## API Integration Details

### Base Configuration
- **API Endpoint**: https://images-api.nasa.gov
- **Authentication**: None required (public API)
- **Response Format**: Collection+JSON
- **Rate Limiting**: None specified by NASA

### Supported Media Types
- **Images**: JPEG, PNG, TIFF formats
- **Videos**: MP4, MOV with optional captions (VTT/SRT)
- **Audio**: MP3, WAV files from missions

## Tool Implementations

### 1. search_nasa_media
**Purpose**: Primary search interface for NASA's media collection

**Parameters**:
- `query` (required): Free text search terms
- `media_type`: Filter by "image", "video", "audio" (comma-separated)
- `center`: NASA center filter (JSC, JPL, GSFC, etc.)
- `year_start`/`year_end`: Date range filters (YYYY format)
- `page`/`page_size`: Pagination controls (max 100 per page)

**Key Features**:
- Comprehensive metadata display including titles, descriptions, keywords
- Preview link extraction from Collection+JSON responses
- Smart result formatting with emoji indicators
- Pagination support with next page hints

### 2. get_nasa_asset
**Purpose**: Retrieve all available file formats for a specific media asset

**Functionality**:
- Fetches asset manifest using NASA ID
- Categorizes files by type (original, medium, small, thumbnail, metadata)
- Provides direct download links for each format
- Essential for accessing high-resolution content

### 3. get_nasa_metadata
**Purpose**: Access detailed technical metadata for assets

**Returns**:
- Direct link to JSON metadata file
- Contains EXIF data, technical specifications
- Extended descriptions and attribution information
- Camera/instrument details for scientific imagery

### 4. get_nasa_captions
**Purpose**: Access video captions and subtitles

**Application**:
- Only works with video assets
- Returns VTT or SRT caption file locations
- Essential for accessibility and content understanding
- Supports multiple languages where available

### 5. browse_nasa_album
**Purpose**: Explore curated NASA media collections

**Popular Albums**:
- `apollo`: Apollo mission collection
- `hubble`: Hubble Space Telescope imagery
- `mars`: Mars exploration content  
- `iss`: International Space Station media

## Response Formatting Guidelines

### Visual Indicators
- 🚀 NASA branding and space theme
- 📸 Media type indicators
- 🆔 NASA ID display
- 📅 Date formatting
- 🔍 Preview link highlighting

### Error Handling
- ❌ Clear error messages for invalid requests
- 404 handling for non-existent NASA IDs
- Timeout protection (30-second limit)
- Graceful API failure responses

## Usage Patterns

### Effective Search Strategies
1. **Broad to Narrow**: Start with general terms, then use filters
2. **Mission Names**: Use specific mission identifiers (Apollo 11, Curiosity, etc.)
3. **Scientific Terms**: Leverage NASA's technical vocabulary
4. **Date Ranges**: Combine with mission timelines for precision

### Common Workflows
1. **Discovery**: Search → Browse results → Get asset details
2. **Research**: Search with filters → Get metadata → Download files
3. **Media Collection**: Album browse → Asset details → File downloads

## Technical Considerations

### Performance Optimization
- Pagination prevents overwhelming responses
- Preview links enable quick content assessment  
- Async HTTP client for concurrent requests
- Reasonable timeout values

### Error Recovery
- Comprehensive HTTP status code handling
- Network failure graceful degradation
- Invalid parameter validation
- Missing data fallbacks

### Data Processing
- Collection+JSON parsing
- Media type categorization
- Link extraction and validation
- Metadata formatting for readability

## Claude Integration Best Practices

### Natural Language Processing
- Interpret user intent for NASA content
- Map colloquial terms to NASA vocabulary
- Suggest related searches and albums
- Provide context for scientific imagery

### Response Formatting
- Structure responses for scan-ability
- Include direct action links
- Provide usage hints and tips
- Balance detail with readability

### Multi-Turn Conversations
- Remember previous search contexts
- Suggest follow-up actions
- Build on discovered NASA IDs
- Guide users through workflows

## Maintenance and Updates

### Monitoring
- Track API response times
- Monitor for NASA API changes
- Watch for new album additions
- Observe search pattern effectiveness

### Future Enhancements
- Advanced filtering options
- Batch asset processing
- Favorite/bookmark functionality
- Enhanced metadata parsing

## Security Notes

- Public API requires no authentication
- No user data stored or transmitted
- Read-only operations only
- Standard HTTP security practices applied

## Code Architecture

### Utility Functions
- `format_media_result()`: Formats individual search results with metadata
- `format_asset_manifest()`: Categorizes and displays available file formats

### Error Handling Strategy
- Graceful degradation for network issues
- User-friendly error messages
- Proper HTTP status code interpretation
- Timeout protection for all API calls

### Logging Implementation
- Structured logging to stderr for Docker compatibility
- Request/response logging for debugging
- Error tracking with stack traces
- Performance monitoring capabilities

## Development Guidelines

### Code Standards
- Single-line docstrings only (multi-line causes gateway errors)
- Empty string defaults instead of None values
- Comprehensive input validation
- Consistent error message formatting

### Testing Approach
- Direct server execution for development
- MCP protocol compliance testing
- API endpoint validation
- Error scenario coverage

### Deployment Considerations
- Docker containerization for portability
- Non-root user execution for security
- Environment variable configuration
- Health check endpoints for monitoring