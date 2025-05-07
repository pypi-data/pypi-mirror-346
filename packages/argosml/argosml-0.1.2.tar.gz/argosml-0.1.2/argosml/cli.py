import argparse
import subprocess
import sys
import os
from pathlib import Path
import http.server
import socketserver
import threading

def start_mlflow_server(host, port):
    """Start the MLflow server with the given host and port."""
    cmd = [
        "mlflow", "server",
        "--host", host,
        "--port", str(port),
        "--app-name", "mlflow_cors"
    ]
    process = subprocess.Popen(cmd)
    return process

def start_reports_server(port=8444):
    """Start a simple HTTP server to serve the reports dashboard."""
    package_dir = Path(__file__).resolve().parent
    dist_dir = package_dir / "reports_dashboard" / "dist" / "spa"

    if not dist_dir.exists():
        print(f"❌ Error: Reports dashboard files not found at {dist_dir}")
        print("👉 Please run `npm run build` in the reports_dashboard folder.")
        sys.exit(1)

    os.chdir(dist_dir)

    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"📊 Serving reports dashboard at http://localhost:{port}")
        httpd.serve_forever()

def start(args):
    """Start both the MLflow server and the dashboard server."""
    mlflow_process = start_mlflow_server(args.host, args.port)
    print(f"🚀 Started MLflow server at http://{args.host}:{args.port}")

    reports_thread = threading.Thread(target=start_reports_server, daemon=True)
    reports_thread.start()

    try:
        mlflow_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down MLflow server...")
        mlflow_process.terminate()
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="ArgosML CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser("start", help="Start ArgosML services")
    start_parser.add_argument("--host", default="127.0.0.1", help="MLflow server host")
    start_parser.add_argument("--port", type=int, default=8787, help="MLflow server port")

    args = parser.parse_args()

    if args.command == "start":
        start(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
