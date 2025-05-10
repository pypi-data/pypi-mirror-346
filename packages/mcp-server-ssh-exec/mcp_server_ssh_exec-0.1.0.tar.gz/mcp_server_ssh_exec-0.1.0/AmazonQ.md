# MCP Server SSH Exec

This is an MCP server that provides SSH connection and command execution capabilities through the Model Context Protocol (MCP).

## Features

- Connect to SSH servers using password or key-based authentication
- Execute commands on remote servers
- Upload and download files
- List directory contents
- Secure connection handling

## Usage

The server provides the following tools:

1. **connect** - Establish an SSH connection
   - Parameters: host, port, username, password, key_path, key_passphrase (all optional, will use environment variables if not provided)

2. **disconnect** - Close the SSH connection
   - No parameters required

3. **execute** - Run a command on the remote server
   - Parameters: command (required), timeout (optional, in seconds)

4. **upload** - Upload a file to the remote server
   - Parameters: local_path (required), remote_path (required)

5. **list_files** - List files in a directory on the remote server
   - Parameters: path (required)

6. **download** - Download a file from the remote server
   - Parameters: remote_path (required), local_path (required)

## Configuration

The server can be configured using environment variables:

- SSH_HOST - The hostname or IP address of the SSH server
- SSH_PORT - The port number (default: 22)
- SSH_USERNAME - The username for authentication
- SSH_PASSWORD - The password for authentication (if using password auth)
- SSH_KEY_PATH - Path to the private key file (if using key-based auth)
- SSH_KEY_PASSPHRASE - Passphrase for the private key (if required)

## Example

```python
# Connect to an SSH server
mcp-server-ssh-exec___connect(host="example.com", username="user", password="pass")

# Execute a command
result = mcp-server-ssh-exec___execute(command="ls -la")

# Upload a file
mcp-server-ssh-exec___upload(local_path="/path/to/local/file", remote_path="/path/to/remote/file")

# List files in a directory
files = mcp-server-ssh-exec___list_files(path="/home/user")

# Download a file
mcp-server-ssh-exec___download(remote_path="/path/to/remote/file", local_path="/path/to/local/file")

# Disconnect
mcp-server-ssh-exec___disconnect()
```
