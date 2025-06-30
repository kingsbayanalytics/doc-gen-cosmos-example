#!/usr/bin/env python3
"""Diagnose PromptFlow service endpoints and capabilities."""

import requests
import subprocess
import json

def check_pf_service_endpoints():
    """Check what endpoints are available on the PromptFlow service."""
    print("=== Checking PromptFlow Service Endpoints ===")
    
    base_url = "http://127.0.0.1:23333"
    test_paths = [
        "/",
        "/v1.0",
        "/v1.0/flows",
        "/api/flows",
        "/flows",
        "/api/v1/flows",
        "/api/v1.0/flows",
        "/v1.0/flow_runs",
        "/api/flow_runs",
    ]
    
    for path in test_paths:
        try:
            response = requests.get(f"{base_url}{path}", timeout=5)
            print(f"{path}: {response.status_code} - {response.text[:100]}...")
        except Exception as e:
            print(f"{path}: ERROR - {str(e)}")
    print()

def check_pf_commands():
    """Check available pf commands for serving flows."""
    print("=== Checking PromptFlow CLI Commands ===")
    
    # Check main pf commands
    try:
        result = subprocess.run(["pf", "--help"], capture_output=True, text=True)
        print("Available pf commands:")
        for line in result.stdout.split('\n'):
            if 'serve' in line.lower() or 'flow' in line.lower():
                print(f"  {line.strip()}")
    except Exception as e:
        print(f"Error checking pf commands: {e}")
    print()
    
    # Check pf flow subcommands
    try:
        result = subprocess.run(["pf", "flow", "--help"], capture_output=True, text=True)
        print("Available pf flow subcommands:")
        for line in result.stdout.split('\n'):
            if 'serve' in line.lower() or 'test' in line.lower() or 'run' in line.lower():
                print(f"  {line.strip()}")
    except Exception as e:
        print(f"Error checking pf flow commands: {e}")
    print()

def check_flow_serve_option():
    """Check if we can serve the flow directly."""
    print("=== Checking Flow Serve Option ===")
    
    try:
        # Try pf flow serve --help
        result = subprocess.run(["pf", "flow", "serve", "--help"], capture_output=True, text=True)
        if result.returncode == 0:
            print("'pf flow serve' command is available!")
            print("Usage:", result.stdout.split('\n')[0])
            print("\nTo serve a flow locally, you might use:")
            print("  pf flow serve --source /path/to/flow --port 8080")
        else:
            print("'pf flow serve' command not found or errored")
            print("Error:", result.stderr)
    except Exception as e:
        print(f"Error checking pf flow serve: {e}")
    print()

def check_running_flows():
    """Check if any flows are currently being served."""
    print("=== Checking Running Flows ===")
    
    try:
        # Check for any flow-related processes
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        flow_processes = [line for line in result.stdout.split('\n') if 'flow' in line.lower() and 'promptflow' in line.lower()]
        if flow_processes:
            print("Found flow-related processes:")
            for proc in flow_processes[:5]:  # Show first 5
                print(f"  {proc[:150]}...")
        else:
            print("No flow-serving processes found")
    except Exception as e:
        print(f"Error checking processes: {e}")
    print()

if __name__ == "__main__":
    check_pf_service_endpoints()
    check_pf_commands()
    check_flow_serve_option()
    check_running_flows()
    
    print("\n=== DIAGNOSIS SUMMARY ===")
    print("1. The pf service at port 23333 appears to be a UI/tracing service")
    print("2. To serve flows via REST API, you likely need to use 'pf flow serve'")
    print("3. This would start a separate server specifically for the flow")