#!/bin/bash
# Script to synchronize environment variables with the MCP server configuration

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed. Please install jq first."
    exit 1
fi

# Default config file locations
CLINE_CONFIG="$HOME/.config/cline/config.json"
CLAUDE_CONFIG_MAC="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
CLAUDE_CONFIG_WIN="%APPDATA%/Claude/claude_desktop_config.json"

# Determine which config file to use
if [ -f "$CLINE_CONFIG" ]; then
    CONFIG_FILE="$CLINE_CONFIG"
    echo "Using Cline configuration at $CONFIG_FILE"
elif [ -f "$CLAUDE_CONFIG_MAC" ]; then
    CONFIG_FILE="$CLAUDE_CONFIG_MAC"
    echo "Using Claude Desktop configuration at $CONFIG_FILE"
elif [ -f "$CLAUDE_CONFIG_WIN" ]; then
    CONFIG_FILE="$CLAUDE_CONFIG_WIN"
    echo "Using Claude Desktop configuration at $CONFIG_FILE"
else
    echo "Error: Could not find a valid configuration file."
    exit 1
fi

# Extract environment variables from the configuration
if jq -e '.mcpServers."mcp-server-ssh-exec"' "$CONFIG_FILE" > /dev/null 2>&1; then
    echo "Extracting environment variables from configuration..."
    
    # Extract each environment variable
    SSH_HOST=$(jq -r '.mcpServers."mcp-server-ssh-exec".env.SSH_HOST // ""' "$CONFIG_FILE")
    SSH_PORT=$(jq -r '.mcpServers."mcp-server-ssh-exec".env.SSH_PORT // "22"' "$CONFIG_FILE")
    SSH_USERNAME=$(jq -r '.mcpServers."mcp-server-ssh-exec".env.SSH_USERNAME // ""' "$CONFIG_FILE")
    SSH_PASSWORD=$(jq -r '.mcpServers."mcp-server-ssh-exec".env.SSH_PASSWORD // ""' "$CONFIG_FILE")
    SSH_KEY_PATH=$(jq -r '.mcpServers."mcp-server-ssh-exec".env.SSH_KEY_PATH // ""' "$CONFIG_FILE")
    SSH_KEY_PASSPHRASE=$(jq -r '.mcpServers."mcp-server-ssh-exec".env.SSH_KEY_PASSPHRASE // ""' "$CONFIG_FILE")
    
    # Export the variables
    export SSH_HOST
    export SSH_PORT
    export SSH_USERNAME
    export SSH_PASSWORD
    export SSH_KEY_PATH
    export SSH_KEY_PASSPHRASE
    
    echo "Environment variables have been set:"
    echo "SSH_HOST=$SSH_HOST"
    echo "SSH_PORT=$SSH_PORT"
    echo "SSH_USERNAME=$SSH_USERNAME"
    echo "SSH_PASSWORD=********" # Don't print the actual password
    echo "SSH_KEY_PATH=$SSH_KEY_PATH"
    echo "SSH_KEY_PASSPHRASE=********" # Don't print the actual passphrase
else
    echo "Error: mcp-server-ssh-exec configuration not found in $CONFIG_FILE"
    exit 1
fi
