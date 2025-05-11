import click
from .dht_node import DHTNode
import json
import time
import socket
import sys

@click.group()
def cli():
    """Simple DHT CLI interface."""
    pass

@cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=5000, type=int, help='Port to bind to')
@click.option('--bootstrap', help='Comma-separated list of bootstrap nodes (host:port)')
def start(host, port, bootstrap):
    """Start a new DHT node."""
    bootstrap_nodes = bootstrap.split(',') if bootstrap else []
    
    try:
        node = DHTNode(host, port, bootstrap_nodes)
        node.start()
        
        click.echo(f"Node started successfully on {host}:{port}")
        click.echo(f"Public IP: {node.public_ip}")
        click.echo(f"Node ID: {node.id}")
        
        if bootstrap_nodes:
            click.echo(f"Connected to bootstrap nodes: {', '.join(bootstrap_nodes)}")
        
        click.echo("Press Ctrl+C to stop the node...")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            click.echo("Stopping node...")
            node.stop()
            click.echo("Node stopped.")
    except Exception as e:
        click.echo(f"Error starting node: {e}")
        sys.exit(1)

def _send_message(host: str, port: int, message: dict, timeout: int = 5) -> dict:
    """Send a message to a DHT node and wait for response."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Set timeout before sending
        sock.settimeout(timeout)
        
        # Send message
        click.echo(f"Connecting to node at {host}:{port}...")
        sock.sendto(json.dumps(message).encode(), (host, port))
        
        # Wait for response
        try:
            data, _ = sock.recvfrom(4096)
            return json.loads(data.decode())
        except socket.timeout:
            click.echo(f"Error: No response received from {host}:{port} within {timeout} seconds")
            click.echo("Possible reasons:")
            click.echo("1. The node is not running")
            click.echo("2. The port is blocked by a firewall")
            click.echo("3. The node is behind NAT without port forwarding")
            sys.exit(1)
    except Exception as e:
        click.echo(f"Error sending message: {e}")
        sys.exit(1)
    finally:
        sock.close()

@cli.command()
@click.option('--host', required=True, help='Host of the DHT node')
@click.option('--port', required=True, type=int, help='Port of the DHT node')
@click.option('--timeout', default=5, help='Timeout in seconds')
@click.argument('key')
@click.argument('value')
def put(host, port, timeout, key, value):
    """Store a key-value pair in the DHT."""
    response = _send_message(host, port, {
        'type': 'store',
        'key': key,
        'value': value
    }, timeout)
    
    if response.get('type') == 'store_ack':
        click.echo(f"Successfully stored {key}={value}")
        click.echo("Value has been replicated to all nodes in the network")
    else:
        click.echo(f"Failed to store {key}={value}")
        click.echo(f"Response: {response}")

@cli.command()
@click.option('--host', required=True, help='Host of the DHT node')
@click.option('--port', required=True, type=int, help='Port of the DHT node')
@click.option('--timeout', default=5, help='Timeout in seconds')
@click.argument('key')
def get(host, port, timeout, key):
    """Retrieve a value from the DHT."""
    response = _send_message(host, port, {
        'type': 'get',
        'key': key
    }, timeout)
    
    if response.get('type') == 'get_response':
        value = response.get('value')
        if value is None:
            click.echo(f"No value found for key: {key}")
        else:
            click.echo(f"Value for {key}: {value}")
    else:
        click.echo(f"Failed to retrieve value for key: {key}")
        click.echo(f"Response: {response}")

@cli.command()
@click.option('--host', required=True, help='Host of the DHT node')
@click.option('--port', required=True, type=int, help='Port of the DHT node')
@click.option('--timeout', default=5, help='Timeout in seconds')
def info(host, port, timeout):
    """Get information about a DHT node."""
    response = _send_message(host, port, {
        'type': 'info_request'
    }, timeout)
    
    if response.get('type') == 'info_response':
        node_id = response.get('node_id', 'Unknown')
        peer_count = response.get('peer_count', 0)
        data_count = response.get('data_count', 0)
        
        click.echo(f"Node ID: {node_id}")
        click.echo(f"Connected peers: {peer_count}")
        click.echo(f"Stored key-value pairs: {data_count}")
    else:
        click.echo("Failed to get node information")

def main():
    """Entry point for the CLI."""
    cli()

if __name__ == '__main__':
    main() 