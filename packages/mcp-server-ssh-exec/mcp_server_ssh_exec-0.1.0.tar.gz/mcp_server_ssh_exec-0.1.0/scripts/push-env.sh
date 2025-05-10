#!/bin/bash
# Script to push environment variables to the MCP server configuration

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

# Get current directory
CURRENT_DIR=$(pwd)

# Create or update the MCP server configuration
jq --arg dir "$CURRENT_DIR" '.mcpServers."mcp-server-ssh-exec" = {
    "command": "uv",
    "args": ["--directory", $dir, "run", "mcp-server-ssh-exec"],
    "env": {
        "SSH_HOST": "'"${SSH_HOST:-}"'",
        "SSH_PORT": "'"${SSH_PORT:-22}"'",
        "SSH_USERNAME": "'"${SSH_USERNAME:-}"'",
        "SSH_PASSWORD": "'"${SSH_PASSWORD:-}"'",
        "SSH_KEY_PATH": "'"${SSH_KEY_PATH:-}"'",
        "SSH_KEY_PASSPHRASE": "'"${SSH_KEY_PASSPHRASE:-}"'"
    },
    "disabled": false,
    "autoApprove": []
}' "$CONFIG_FILE" > "$CONFIG_FILE.tmp"

# Check if the update was successful
if [ $? -eq 0 ]; then
    mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    echo "Successfully updated MCP server configuration with current environment variables."
    echo "Please restart your client to apply the changes."
else
    echo "Error: Failed to update configuration file."
    rm -f "$CONFIG_FILE.tmp"
    exit 1
fi
