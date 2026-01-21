#!/usr/bin/env python3
"""
Blender MCP Wrapper Script
This wrapper launches Blender with the MCP server and filters stdout to prevent JSON parsing errors.
"""

import sys
import subprocess
import os
import threading

def filter_output(pipe, target_stream):
    """Filter Blender's output and only forward valid lines."""
    for line in iter(pipe.readline, b''):
        try:
            # Try to decode the line
            decoded = line.decode('utf-8', errors='ignore')

            # Skip Blender's startup messages that aren't JSON
            skip_patterns = [
                'Blender',
                'Read blend:',
                'Saved session',
                'Info:',
                'Warning:',
                'found bundled python:'
            ]

            # Check if this line should be skipped
            should_skip = any(pattern in decoded for pattern in skip_patterns)

            # If it looks like JSON (starts with {) or is important, pass it through
            stripped = decoded.strip()
            if not should_skip or stripped.startswith('{'):
                target_stream.buffer.write(line)
                target_stream.buffer.flush()
        except Exception:
            # If there's any error, just pass the line through
            target_stream.buffer.write(line)
            target_stream.buffer.flush()

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
        print(f"Error: Blender not found at {blender_exe}", file=sys.stderr)
        print("Please update the blender_exe path in this wrapper script.", file=sys.stderr)
        sys.exit(1)

    # Launch Blender
    try:
        process = subprocess.Popen(
            [blender_exe, '--background', '--python', mcp_server_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )

        # Create threads to handle output filtering
        stdout_thread = threading.Thread(
            target=filter_output,
            args=(process.stdout, sys.stdout),
            daemon=True
        )
        stderr_thread = threading.Thread(
            target=lambda: process.stderr.read(),  # Just consume stderr
            daemon=True
        )

        stdout_thread.start()
        stderr_thread.start()

        # Forward stdin to Blender
        try:
            for line in sys.stdin.buffer:
                process.stdin.write(line)
                process.stdin.flush()
        except (BrokenPipeError, IOError):
            pass

        # Wait for process to complete
        process.wait()
        sys.exit(process.returncode)

    except FileNotFoundError:
        print(f"Error: Blender executable not found: {blender_exe}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error launching Blender: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
