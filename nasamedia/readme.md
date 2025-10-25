# NASA Image and Video Library MCP Server

A Model Context Protocol (MCP) server that provides access to NASA's vast collection of images, videos, and audio files through the NASA Image and Video Library API.

## Purpose

This MCP server provides a secure interface for AI assistants to search and access NASA's extensive media collection including space imagery, mission videos, audio recordings, and scientific visualizations.

## Features

### Current Implementation

- **`search_nasa_media`** - Search NASA's media library with flexible parameters including query terms, media type filters, date ranges, and pagination
- **`get_nasa_asset`** - Retrieve all available file formats and sizes for a specific NASA media asset by its NASA ID
- **`get_nasa_metadata`** - Get the metadata file location containing detailed EXIF data and technical specifications
- **`get_nasa_captions`** - Access caption/subtitle files for NASA video content (VTT/SRT format)
- **`browse_nasa_album`** - Browse curated NASA media albums like 'apollo', 'hubble', 'mars', and 'iss'

## Prerequisites

- Docker Desktop with MCP Toolkit enabled
- Docker MCP CLI plugin (`docker mcp` command)
- No API key required - NASA's Image and Video Library API is public

## Installation

See the step-by-step instructions provided with the files.

## Usage Examples

In Claude Desktop, you can ask:

- "Show me images of the Apollo 11 moon landing"
- "Find recent Mars rover videos"
- "Search for Hubble telescope images of galaxies"
- "Get me audio files from space missions"
- "Browse the International Space Station album"
- "Find images from NASA's Jet Propulsion Laboratory from 2020-2023"
- "Show me the available file formats for NASA ID as11-40-5874"

### Search Parameters

The search tool supports various filters:
- **Media Type**: image, video, audio (or combinations)
- **NASA Center**: JSC, JPL, GSFC, ARC, etc.
- **Date Ranges**: Use year_start and year_end (YYYY format)
- **Pagination**: Control page size and navigate through results

### Popular NASA Albums

Try browsing these curated collections:
- `apollo` - Apollo mission imagery
- `hubble` - Hubble Space Telescope images
- `mars` - Mars exploration content
- `iss` - International Space Station media
- `jpl` - Jet Propulsion Laboratory content

## Architecture

```
Claude Desktop → MCP Gateway → NASA MCP Server → NASA Images API
                                     ↓
                            https://images-api.nasa.gov
```

## Development

### Local Testing

```bash
# Run directly (no environment variables needed)
python nasa_server.py

# Test MCP protocol
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python nasa_server.py
```

### Adding New Tools

1. Add the function to `nasa_server.py`
2. Decorate with `@mcp.tool()`
3. Update the catalog entry with the new tool name
4. Rebuild the Docker image

## API Details

This server uses NASA's public Image and Video Library API:
- **Base URL**: https://images-api.nasa.gov
- **Authentication**: None required
- **Rate Limits**: None specified
- **Data Format**: Collection+JSON responses
- **Media Types**: Images (JPEG, PNG, TIFF), Videos (MP4, MOV), Audio (MP3, WAV)

### File Formats Available

For each media asset, multiple formats are typically available:
- **Original**: Full resolution, uncompressed
- **Medium**: Web-optimized medium resolution
- **Small**: Thumbnail-sized preview
- **Metadata**: JSON file with technical details and EXIF data

## Troubleshooting

### Tools Not Appearing

- Verify Docker image built successfully
- Check catalog and registry files
- Ensure Claude Desktop config includes custom catalog
- Restart Claude Desktop

### Search Issues

- Verify internet connectivity
- Try simpler search terms
- Check if NASA API is accessible
- Use specific NASA centers or date ranges to narrow results

### No Results Found

- Try broader search terms
- Check spelling of NASA center names
- Verify date ranges are in YYYY format
- Some older content may have limited metadata

## Security Considerations

- No authentication required - public API
- Running as non-root user
- No sensitive data handling
- All requests are read-only

## Performance Notes

- Search results are paginated (default 10 items, max 100)
- API responses include preview links for quick access
- Large media files are linked, not embedded
- Metadata files are separate downloads

## License

MIT License