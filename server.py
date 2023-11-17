from flask import Flask, jsonify, request
from kubernetes import client, config
import base64

app = Flask(__name__)

# Load Kubernetes config, assumes running inside a pod with service account
config.load_incluster_config()

# Define the Kubernetes API client
kube_client = client.CoreV1Api()

# Function to retrieve API key from Kubernetes secret
def get_api_key():
    secret_name = "api-key-secret"  # Replace with your secret name
    secret_namespace = "api-proxy"  # Replace with your secret's namespace

    secret = kube_client.read_namespaced_secret(secret_name, secret_namespace)
    api_key = base64.b64decode(secret.data.get('api-key')).decode('utf-8')
    print(api_key)
    return api_key


# Function to retrieve external IP of nodes
def get_node_info():
    nodes = kube_client.list_node().items
    node_info = []
    for node in nodes:
        addresses = node.status.addresses
        external_ip = next((addr.address for addr in addresses if addr.type == "ExternalIP"), None)
        node_info.append({
            "name": node.metadata.name,
            "external_ip": external_ip if external_ip else "N/A"
        })
    return node_info

# Endpoint to get node info
@app.route('/node-info', methods=['GET'])
def node_info():
    api_key = request.headers.get('X-API-Key')

    # Check if API key matches the stored key in Kubernetes secret
    expected_api_key = get_api_key()

    if api_key != expected_api_key:
        return jsonify({"error": "Unauthorized"}), 401

    node_info = get_node_info()
    return jsonify({"nodes": node_info})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
