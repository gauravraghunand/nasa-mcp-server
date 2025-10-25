# nasa-mcp-server
A Model Context Protocol (MCP) server that provides your AI assistant (e.g., Claude Desktop, LM Studio) with direct, secure access to NASA's vast collection of images, videos, and audio files through the public NASA Image and Video Library API.

## Features

This server implements five core tools for comprehensive interaction with NASA's digital media:

  * **`search_nasa_media`**: Search the media library by query, media type, NASA center, and date range.
  * **`get_nasa_asset`**: Retrieve all available file formats (original, medium, small, metadata) for a specific NASA ID.
  * **`get_nasa_metadata`**: Get the direct link to the JSON file containing detailed EXIF and technical specifications.
  * **`get_nasa_captions`**: Access caption/subtitle files (VTT/SRT) for video content.
  * **`browse_nasa_album`**: Browse curated collections like 'apollo', 'hubble', and 'mars'.

## Prerequisites

To run this custom MCP server, you must have the following installed and configured:

1.  **Docker Desktop** (with the **MCP Toolkit** enabled in Beta Features).
2.  An **LLM Client** that supports MCP, such as Claude Desktop.
3.  The necessary project files: `Dockerfile`, `requirements.txt`, `nasa_server.py`, `custom.yaml`, and `registry.yaml` (from this repository).

## Installation and Setup

Follow these steps to build the Docker image, configure the MCP Gateway, and connect it to your LLM client.

### Step 1: Prepare the Project Directory

1.  Create a new directory (e.g., `nasa-mcp-server`) and place the provided files (`Dockerfile`, `requirements.txt`, `nasa_server.py`) inside it.
2.  Navigate into the directory via your terminal:
    ```bash
    cd nasa-mcp-server
    ```

### Step 2: Build the Docker Image

The `Dockerfile` creates a secure container running as a non-root user (`mcpuser`) with the necessary Python dependencies (`mcp[cli]` and `httpx`).

1.  Build the Docker image with the tag `nasa-mcp-server`:
    ```bash
    docker build -t nasa-mcp-server:latest .
    ```

### Step 3: Create the Custom Catalog

You need to tell the Docker MCP Gateway about your new server and its tools. The `custom.yaml` file defines the server in a format the gateway understands.

1.  Locate your local Docker MCP catalogs directory. On most systems, this is:
      * **Windows:** `C:\Users\<username>\.docker\mcp\catalogs\`
      * **macOS/Linux:** `~/.docker/mcp/catalogs/`
2.  Copy or ensure the provided **`custom.yaml`** file is placed inside this `catalogs/` directory. If you already have a custom catalog, merge the `nasa` entry into it.

### Step 4: Update the Registry

The Docker MCP Registry tracks which servers are *installed* and available to the client. You must manually add your server to this file.

1.  Locate the registry file:
      * **Windows:** `C:\Users\<username>\.docker\mcp\registry.yaml`
      * **macOS/Linux:** `~/.docker/mcp/registry.yaml`
2.  Edit the **`registry.yaml`** file and ensure the `nasa` entry is present under the `registry:` key:
    ```yaml
    registry:
      # ... other servers you may have
      nasa: # <- Add this entry
        ref: "" 
    ```

### Step 5: Configure the LLM Client (Claude Desktop Example)

You need to ensure your LLM client is configured to check your custom catalog for tools.

1.  Locate the configuration file for your client. For **Claude Desktop**, this is typically `claude_desktop_config.json` in a hidden app data folder.

2.  Verify the `mcp-toolkit-gateway` command includes a reference to your custom catalog file (`custom.yaml`):

    ```json
    {
      "mcpServers": {
        "mcp-toolkit-gateway": {
          "command": "docker",
          "args": [
            "run",
            // ... other arguments ...
            "--catalog=/mcp/catalogs/docker-mcp.yaml",
            "--catalog=/mcp/catalogs/custom.yaml", // <- Ensure this is present
            // ... other arguments ...
            ]
        }
      }
    }
    ```

### Step 6: Test and Use the Server

1.  **Restart your LLM client** (e.g., Claude Desktop).

2.  In a chat, check the "Search and tools" menu to confirm the **"NASA Image and Video Library"** tool and its functions (`search_nasa_media`, `browse_nasa_album`, etc.) are available.

3.  Ask a question that requires the tool, and the AI should execute the correct function:

    **Example Prompt:**

    > "Find recent Mars rover videos using the NASA media tool, and then show me the file formats for the first result's asset ID."

-----

## API Details

  * **Base URL**: `https://images-api.nasa.gov`
  * **Authentication**: None required (public API)
  * **Security**: The server is designed for read-only operations and runs as a non-root user in a container.
