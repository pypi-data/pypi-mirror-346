.PHONY: install-server mcp-inspector

install-server:  # Install the Groundlight server in Claude Desktop
	uv run mcp install framegrab_mcp_server.py --name "framegrab"

mcp-inspector:  # Run the MCP inspector
	uv run mcp dev framegrab_mcp_server.py

build-docker:  # Build the Docker image for the Groundlight MCP server
	docker build -t framegrab-mcp-server .

run-docker:  # Run the Docker container
	docker run -it --rm framegrab-mcp-server

push-docker:  # Push the Docker image to the registry
	docker tag framegrab-mcp-server groundlight/framegrab-mcp-server:latest
	docker push groundlight/framegrab-mcp-server
