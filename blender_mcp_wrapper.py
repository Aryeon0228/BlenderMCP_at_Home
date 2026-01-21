#!/usr/bin/env python3
"""
Blender MCP Wrapper Script
This wrapper launches Blender with the MCP server and filters stdout to prevent JSON parsing errors.
"""

import sys
import subprocess
import os
import threading
import select

def filter_output(pipe, target_stream):
    """Filter Blender's output and only forward valid JSON-RPC lines."""
    buffer = b''

    for line in iter(pipe.readline, b''):
        if not line:
            break

        try:
            # Accumulate data
            buffer += line

            # Try to decode
            decoded = line.decode('utf-8', errors='ignore').strip()

            # Skip Blender's startup messages that aren't JSON
            skip_patterns = [
                'Blender',
                'Read blend:',
                'Saved session',
                'Info:',
                'Warning:',
                'found bundled python:',
                'Color management',
                'Read new prefs:',
                'Switching to fully guarded memory allocator'
            ]

            # Check if this line should be skipped
            should_skip = any(pattern in decoded for pattern in skip_patterns)

            # Only pass through valid JSON-RPC messages
            if decoded.startswith('{') or decoded.startswith('['):
                # This looks like JSON, pass it through
                target_stream.buffer.write(line)
                target_stream.buffer.flush()
            elif not should_skip and decoded and not decoded.startswith('['):
                # Unknown line that might be important - log to stderr instead
                sys.stderr.write(f"[Wrapper] Filtered: {decoded}\n")
                sys.stderr.flush()

        except Exception as e:
            # Log errors to stderr
            sys.stderr.write(f"[Wrapper] Error filtering output: {e}\n")
            sys.stderr.flush()

def forward_stdin(process):
    """Forward stdin to the Blender process."""
    try:
        while True:
            # Read from stdin
            data = sys.stdin.buffer.read(1024)
            if not data:
                break

            # Write to process
            process.stdin.write(data)
            process.stdin.flush()
    except (BrokenPipeError, IOError, OSError) as e:
        sys.stderr.write(f"[Wrapper] stdin closed: {e}\n")
        sys.stderr.flush()
    finally:
        try:
            process.stdin.close()
        except:
            pass

def main():
    """Launch Blender with the MCP server."""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mcp_server_script = os.path.join(script_dir, 'blender_mcp_server.py')

    # Blender executable path - adjust if needed
    if sys.platform == "win32":
        blender_exe = r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"
    else:
        blender_exe = "blender"

    # Check if Blender exists
    if not os.path.exists(blender_exe) and sys.platform == "win32":
        sys.stderr.write(f"Error: Blender not found at {blender_exe}\n")
        sys.stderr.write("Please update the blender_exe path in this wrapper script.\n")
        sys.stderr.flush()
        sys.exit(1)

    sys.stderr.write(f"[Wrapper] Starting Blender from {blender_exe}\n")
    sys.stderr.write(f"[Wrapper] MCP server script: {mcp_server_script}\n")
    sys.stderr.flush()

    # Launch Blender
    try:
        process = subprocess.Popen(
            [blender_exe, '--background', '--python', mcp_server_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            bufsize=0  # Unbuffered
        )

        sys.stderr.write("[Wrapper] Blender process started\n")
        sys.stderr.flush()

        # Create thread to handle stdin forwarding
        stdin_thread = threading.Thread(
            target=forward_stdin,
            args=(process,),
            daemon=True
        )
        stdin_thread.start()

        # Create thread to handle stdout filtering
        stdout_thread = threading.Thread(
            target=filter_output,
            args=(process.stdout, sys.stdout),
            daemon=True
        )
        stdout_thread.start()

        # Forward stderr to our stderr
        def forward_stderr():
            for line in iter(process.stderr.readline, b''):
                if line:
                    sys.stderr.buffer.write(b'[Blender] ' + line)
                    sys.stderr.buffer.flush()

        stderr_thread = threading.Thread(
            target=forward_stderr,
            daemon=True
        )
        stderr_thread.start()

        # Wait for process to complete
        returncode = process.wait()

        sys.stderr.write(f"[Wrapper] Blender exited with code {returncode}\n")
        sys.stderr.flush()

        sys.exit(returncode)

    except FileNotFoundError:
        sys.stderr.write(f"Error: Blender executable not found: {blender_exe}\n")
        sys.stderr.flush()
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error launching Blender: {e}\n")
        sys.stderr.flush()
        sys.exit(1)

if __name__ == "__main__":
    main()
