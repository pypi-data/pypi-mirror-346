import http.server
import socketserver
import json
import subprocess
import os
import signal
import threading
from urllib.parse import parse_qs
import time
import glob
import sys
import tempfile
import socket
import pkg_resources
import argparse

# Store active processes
active_processes = {}

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    
    return os.path.join(base_path, relative_path)

class ProcessManager:
    def __init__(self):
        self.processes = {}
        self.paused_processes = {}  # Store paused processes separately
        self.lock = threading.Lock()
        # Get the absolute path of the package directory
        self.package_dir = os.path.dirname(os.path.abspath(__file__))

    def get_agent_runtimes(self):
        runtime_files = glob.glob(os.path.join(self.package_dir, 'agent_runtimes/*.py'))
        runtimes = {}
        for f in runtime_files:
            name = os.path.splitext(os.path.basename(f))[0]
            try:
                result = subprocess.run(['python', f, '--help'],
                                     capture_output=True, text=True)
                if result.returncode == 0:
                    help_data = json.loads(result.stdout)
                    display_name = help_data.get('display_name', name)
                    runtimes[name] = display_name
            except Exception:
                runtimes[name] = name
        return runtimes

    def get_agent_fields(self, agent_name):
        try:
            agent_path = os.path.join(self.package_dir, f'agent_runtimes/{agent_name}.py')
            result = subprocess.run(['python', agent_path, '--help'],
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error getting fields for {agent_name}:")
                print(result.stderr)
                return None
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error getting fields for {agent_name}:")
            print(str(e))
            return None

    def start_process(self, agent_runtime_name, form_data):
        if "agent_name" not in form_data:
            print(f"Error: agent_name not found in form_data for runtime {agent_runtime_name}")
        with self.lock:
            try:
                # Create a unique temporary file path
                proc_file = os.path.join(tempfile.gettempdir(), f'niopub_{form_data["agent_name"]}.proc')
                
                # Start the agent process directly with subprocess.Popen
                agent_path = os.path.join(self.package_dir, f'agent_runtimes/{agent_runtime_name}.py')
                process = subprocess.Popen(
                    ['python', agent_path, json.dumps(form_data), proc_file],
                    stdout=subprocess.DEVNULL,  # Redirect stdout to DEVNULL since we don't use it
                    stderr=subprocess.PIPE,
                    text=True,
                    preexec_fn=os.setpgrp  # Start the process in its own process group
                )
                
                # Store the process information
                self.processes[process.pid] = {
                    'runtime_status': 'Running',
                    'agent_runtime_name': agent_runtime_name,
                    'form_data': form_data,
                    'proc_file': proc_file,
                    'last_check': time.time(),
                    'process': process  # Store the Popen object for better process management
                }
                
                # Start a thread to monitor the process and proc_file
                def monitor_process():
                    while True:
                        try:
                            # Check if process is still alive
                            if process.poll() is not None:
                                # Process has died, clean up
                                with self.lock:
                                    if process.pid in self.processes:
                                        del self.processes[process.pid]
                                try:
                                    os.remove(proc_file)
                                except OSError:
                                    pass  # File might already be gone
                                break
                            
                            # Read process output
                            output = process.stderr.readline()
                            if output:
                                print(f"[{agent_runtime_name}] {output.strip()}")
                            
                            # Update status from proc_file
                            try:
                                with open(proc_file, 'r') as f:
                                    status_data = json.load(f)
                                    with self.lock:
                                        if process.pid in self.processes:
                                            self.processes[process.pid].update(status_data)
                                            self.processes[process.pid]['last_check'] = time.time()
                            except (FileNotFoundError, json.JSONDecodeError):
                                pass
                            
                            time.sleep(0.1)  # Small sleep to prevent busy-waiting
                            
                        except Exception as e:
                            print(f"Error monitoring process {process.pid}: {str(e)}")
                            time.sleep(1)
                
                monitor_thread = threading.Thread(target=monitor_process)
                monitor_thread.daemon = True
                monitor_thread.start()
                
                return process.pid
                
            except Exception as e:
                print(f"Error starting {agent_runtime_name}:")
                print(str(e))
                return None

    def stop_process(self, pid, delete_data=False, pause=False):
        print(f"{'Pausing' if pause else 'Stopping'} process {pid}")
        with self.lock:
            if pid in self.processes:
                try:
                    print(f"Process {pid} stopping")
                    process_info = self.processes[pid]
                    proc_file = process_info.get('proc_file')
                    process = process_info.get('process')
                    
                    # First try to terminate the process using the Popen object
                    if process:
                        try:
                            process.terminate()
                            # Wait a bit for graceful shutdown
                            print(f"Process {pid} terminating")
                            time.sleep(0.5)
                            # Force kill if still running
                            if process.poll() is None:
                                process.kill()
                            print(f"Process {pid} terminated")
                        except Exception as e:
                            print(f"Error terminating process object: {str(e)}")
                            # As a fallback, try to kill the process directly
                            try:
                                os.kill(pid, signal.SIGTERM)
                                time.sleep(0.5)
                                try:
                                    os.kill(pid, signal.SIGKILL)
                                except ProcessLookupError:
                                    pass  # Process already dead
                            except ProcessLookupError:
                                pass  # Process might already be dead
                    
                    # Clean up the proc file
                    if proc_file:
                        try:
                            os.remove(proc_file)
                        except OSError:
                            pass  # File might already be gone
                    
                    print(f"Process {pid} stopped")
                    if pause:
                        # Save the process state to paused_processes
                        self.paused_processes[pid] = {
                            'agent_runtime_name': process_info['agent_runtime_name'],
                            'form_data': process_info['form_data'],
                            'runtime_status': 'Paused'
                        }
                    
                    # Remove from process list - this will cause the monitor thread to exit
                    del self.processes[pid]
                except Exception as e:
                    print(f"Error {'pausing' if pause else 'stopping'} process {pid}:")
                    print(str(e))
                    if pid in self.processes:
                        del self.processes[pid]
            
            # If delete_data is True, also remove from paused_processes
            if delete_data and pid in self.paused_processes:
                del self.paused_processes[pid]

    def pause_process(self, pid):
        self.stop_process(pid, pause=True)

    def resume_process(self, pid):
        if pid in self.paused_processes:
            try:
                # Get the saved process info
                process_info = self.paused_processes[pid]
                
                # Start a new process using the saved configuration
                new_pid = self.start_process(process_info['agent_runtime_name'], process_info['form_data'])
                
                if new_pid is not None:
                    # Remove from paused processes
                    del self.paused_processes[pid]
                    return new_pid
                return None
                    
            except Exception as e:
                print(f"Error resuming process {pid}:")
                print(str(e))
                return None

    def get_processes(self):
        with self.lock:
            # Return combination of active and paused processes
            all_processes = {**self.processes, **self.paused_processes}
            return all_processes

    def shutdown_all_processes(self):
        """Stop all active and paused processes"""
        # First stop all active processes
        for pid in list(self.processes.keys()):
            try:
                process_info = self.processes[pid]
                process = process_info.get('process')
                if process:
                    process.terminate()
            except Exception as e:
                print(f"Error terminating process {pid}: {str(e)}")
            self.stop_process(pid, delete_data=True)
        
        # Then stop all paused processes
        for pid in list(self.paused_processes.keys()):
            try:
                del self.paused_processes[pid]
            except Exception as e:
                print(f"Error removing paused process {pid}: {str(e)}")
        print("All processes stopped")

process_manager = ProcessManager()

def get_status(info):
    if 'runtime_status' in info:
        if info['runtime_status'] == 'Paused':
            return 'Paused'
        if info['runtime_status'] == 'Running':
            if info.get('status', '') == 'Online':
                return 'Online'
            else:
                return 'Running'
        else:
            return 'Offline'
    else:
        return 'Unknown'

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Override to disable logging
        pass

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            index_path = get_resource_path('index.html')
            with open(index_path, 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/images/niopub_studio.png':
            try:
                image_path = get_resource_path('images/niopub_studio.png')
                with open(image_path, 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'image/png')
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, "Logo not found")
        elif self.path == '/processes':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            processes = process_manager.get_processes()
            process_list = [
                {
                    'pid': pid,
                    'status': get_status(info),
                    'agent_runtime_name': info['agent_runtime_name'],
                    'form_data': info['form_data']
                }
                for pid, info in processes.items()
            ]
            self.wfile.write(json.dumps(process_list).encode())
        elif self.path == '/agent-runtimes':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            runtimes = process_manager.get_agent_runtimes()
            self.wfile.write(json.dumps(runtimes).encode())
        elif self.path.startswith('/agent-fields/'):
            agent_name = self.path.split('/')[-1]
            fields = process_manager.get_agent_fields(agent_name)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(fields).encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/start':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode())
            
            agent_runtime_name = data['agent_runtime_name'][0]
            form_data = json.loads(data['form_data'][0])
            
            pid = process_manager.start_process(agent_runtime_name, form_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'pid': pid}).encode())
            
        elif self.path == '/pause':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode())
            
            pid = int(data['pid'][0])
            process_manager.pause_process(pid)
            
            self.send_response(200)
            self.end_headers()
            
        elif self.path == '/resume':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode())
            
            pid = int(data['pid'][0])
            new_pid = process_manager.resume_process(pid)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'pid': new_pid}).encode())
            
        elif self.path == '/stop':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode())
            
            pid = int(data['pid'][0])
            delete_data = data.get('delete_data', ['false'])[0].lower() == 'true'
            process_manager.stop_process(pid, delete_data)
            
            self.send_response(200)
            self.end_headers()

class ExitException(Exception):
    pass

def run_server(port):
    httpd = socketserver.TCPServer(("", port), MyHandler)
    # Allow reuse of the address
    httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f"Niopub Studio is running. You can interact with it at http://localhost:{port} on your browser.")
    
    def signal_handler(signum, frame):
        print("\nShutting down server and all processes...")
        # First shutdown all processes
        process_manager.shutdown_all_processes()
        
        # Force exit immediately
        raise ExitException()
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        httpd.serve_forever()
    except ExitException:
        print("Exiting...")
        httpd.shutdown()
    except Exception as e:
        print(f"Error: {str(e)}")
        httpd.shutdown()

def main():
    parser = argparse.ArgumentParser(description='NioPub Server - A local server for running AI agents')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on (default: 8000)')
    parser.add_argument('--version', action='version', version=f'%(prog)s {pkg_resources.get_distribution("niopub").version}')
    
    args = parser.parse_args()
    run_server(args.port)

if __name__ == "__main__":
    main() 