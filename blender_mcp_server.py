#!/usr/bin/env python3
"""
Blender MCP Server
A Model Context Protocol server for controlling Blender 3D software.
"""

# CRITICAL: Redirect stdout IMMEDIATELY before any imports
# This prevents Blender's C-level output from polluting the JSON-RPC channel
import sys
import os

# Save the original stdout file descriptor BEFORE any other code runs
_original_stdout_fd = os.dup(sys.stdout.fileno())

# Redirect stdout to devnull at the OS level immediately
if sys.platform == "win32":
    _devnull_fd = os.open("nul", os.O_WRONLY)
else:
    _devnull_fd = os.open("/dev/null", os.O_WRONLY)

os.dup2(_devnull_fd, sys.stdout.fileno())
os.close(_devnull_fd)

# Now we can import everything else
import asyncio
import json
from typing import Any
import logging
import site

# Add user site-packages to sys.path
# This allows Blender to find packages installed with pip install --user
user_site = site.getusersitepackages()
if user_site not in sys.path:
    sys.path.insert(0, user_site)
    print(f"Added user site-packages to path: {user_site}", file=sys.stderr)

# Import bpy (Blender Python API)
try:
    import bpy
    BLENDER_AVAILABLE = True
    print("Blender Python API loaded successfully", file=sys.stderr)
except ImportError:
    BLENDER_AVAILABLE = False
    print("Warning: bpy module not available. This script must be run from within Blender.", file=sys.stderr)

# Now restore stdout for MCP JSON-RPC communication
os.dup2(_original_stdout_fd, sys.stdout.fileno())
os.close(_original_stdout_fd)

# Recreate sys.stdout with the restored file descriptor
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stdout.flush()

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import mcp.server.stdio

# Configure logging to stderr (not stdout, as MCP uses stdout for JSON-RPC)
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,  # Log to stderr instead of stdout
    format='[%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger("blender-mcp")

# Suppress Blender's internal logging to stdout
if BLENDER_AVAILABLE:
    # Redirect Blender's logging to stderr
    import logging as blender_logging
    for handler in blender_logging.root.handlers[:]:
        blender_logging.root.removeHandler(handler)

    stderr_handler = blender_logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(blender_logging.Formatter('[Blender] %(levelname)s: %(message)s'))
    blender_logging.root.addHandler(stderr_handler)

# Initialize MCP server
app = Server("blender-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Blender tools."""
    return [
        Tool(
            name="create_cube",
            description="Create a cube in the Blender scene",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Location [x, y, z] for the cube",
                        "default": [0, 0, 0]
                    },
                    "scale": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Scale [x, y, z] for the cube",
                        "default": [1, 1, 1]
                    },
                    "name": {
                        "type": "string",
                        "description": "Name for the cube object"
                    }
                }
            }
        ),
        Tool(
            name="create_sphere",
            description="Create a UV sphere in the Blender scene",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Location [x, y, z] for the sphere",
                        "default": [0, 0, 0]
                    },
                    "radius": {
                        "type": "number",
                        "description": "Radius of the sphere",
                        "default": 1.0
                    },
                    "name": {
                        "type": "string",
                        "description": "Name for the sphere object"
                    }
                }
            }
        ),
        Tool(
            name="delete_object",
            description="Delete an object from the scene by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the object to delete"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="list_objects",
            description="List all objects in the current scene",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="move_object",
            description="Move an object to a new location",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the object to move"
                    },
                    "location": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "New location [x, y, z]"
                    }
                },
                "required": ["name", "location"]
            }
        ),
        Tool(
            name="set_material",
            description="Set or create a material for an object",
            inputSchema={
                "type": "object",
                "properties": {
                    "object_name": {
                        "type": "string",
                        "description": "Name of the object"
                    },
                    "material_name": {
                        "type": "string",
                        "description": "Name for the material"
                    },
                    "color": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "RGBA color [r, g, b, a] values between 0 and 1",
                        "default": [0.8, 0.8, 0.8, 1.0]
                    }
                },
                "required": ["object_name", "material_name"]
            }
        ),
        Tool(
            name="render_scene",
            description="Render the current scene to an image file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Output file path for the render"
                    },
                    "resolution_x": {
                        "type": "integer",
                        "description": "Render resolution width",
                        "default": 1920
                    },
                    "resolution_y": {
                        "type": "integer",
                        "description": "Render resolution height",
                        "default": 1080
                    }
                },
                "required": ["filepath"]
            }
        ),
        Tool(
            name="save_blend_file",
            description="Save the current Blender file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path where to save the .blend file"
                    }
                },
                "required": ["filepath"]
            }
        ),
        Tool(
            name="execute_python",
            description="Execute arbitrary Python code in Blender's context",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute"
                    }
                },
                "required": ["code"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls for Blender operations."""

    if not BLENDER_AVAILABLE:
        return [TextContent(
            type="text",
            text="Error: Blender Python API (bpy) is not available. This server must be run from within Blender."
        )]

    try:
        if name == "create_cube":
            location = arguments.get("location", [0, 0, 0])
            scale = arguments.get("scale", [1, 1, 1])
            obj_name = arguments.get("name")

            bpy.ops.mesh.primitive_cube_add(location=location)
            obj = bpy.context.active_object
            obj.scale = scale

            if obj_name:
                obj.name = obj_name

            return [TextContent(
                type="text",
                text=f"Created cube '{obj.name}' at location {location} with scale {scale}"
            )]

        elif name == "create_sphere":
            location = arguments.get("location", [0, 0, 0])
            radius = arguments.get("radius", 1.0)
            obj_name = arguments.get("name")

            bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
            obj = bpy.context.active_object

            if obj_name:
                obj.name = obj_name

            return [TextContent(
                type="text",
                text=f"Created sphere '{obj.name}' at location {location} with radius {radius}"
            )]

        elif name == "delete_object":
            obj_name = arguments["name"]
            obj = bpy.data.objects.get(obj_name)

            if obj is None:
                return [TextContent(
                    type="text",
                    text=f"Error: Object '{obj_name}' not found"
                )]

            bpy.data.objects.remove(obj, do_unlink=True)
            return [TextContent(
                type="text",
                text=f"Deleted object '{obj_name}'"
            )]

        elif name == "list_objects":
            objects = [obj.name for obj in bpy.data.objects]
            return [TextContent(
                type="text",
                text=f"Objects in scene:\n" + "\n".join(f"- {obj}" for obj in objects)
            )]

        elif name == "move_object":
            obj_name = arguments["name"]
            location = arguments["location"]

            obj = bpy.data.objects.get(obj_name)
            if obj is None:
                return [TextContent(
                    type="text",
                    text=f"Error: Object '{obj_name}' not found"
                )]

            obj.location = location
            return [TextContent(
                type="text",
                text=f"Moved object '{obj_name}' to location {location}"
            )]

        elif name == "set_material":
            obj_name = arguments["object_name"]
            mat_name = arguments["material_name"]
            color = arguments.get("color", [0.8, 0.8, 0.8, 1.0])

            obj = bpy.data.objects.get(obj_name)
            if obj is None:
                return [TextContent(
                    type="text",
                    text=f"Error: Object '{obj_name}' not found"
                )]

            # Create or get material
            mat = bpy.data.materials.get(mat_name)
            if mat is None:
                mat = bpy.data.materials.new(name=mat_name)
                mat.use_nodes = True

            # Set color
            if mat.use_nodes:
                principled = mat.node_tree.nodes.get('Principled BSDF')
                if principled:
                    principled.inputs['Base Color'].default_value = color

            # Assign material to object
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)

            return [TextContent(
                type="text",
                text=f"Set material '{mat_name}' with color {color[:3]} on object '{obj_name}'"
            )]

        elif name == "render_scene":
            filepath = arguments["filepath"]
            res_x = arguments.get("resolution_x", 1920)
            res_y = arguments.get("resolution_y", 1080)

            scene = bpy.context.scene
            scene.render.resolution_x = res_x
            scene.render.resolution_y = res_y
            scene.render.filepath = filepath

            bpy.ops.render.render(write_still=True)

            return [TextContent(
                type="text",
                text=f"Rendered scene to {filepath} at {res_x}x{res_y}"
            )]

        elif name == "save_blend_file":
            filepath = arguments["filepath"]
            bpy.ops.wm.save_as_mainfile(filepath=filepath)

            return [TextContent(
                type="text",
                text=f"Saved Blender file to {filepath}"
            )]

        elif name == "execute_python":
            code = arguments["code"]

            # Create a namespace with bpy available
            namespace = {"bpy": bpy}

            # Execute the code
            exec(code, namespace)

            # Get any output
            result = namespace.get("result", "Code executed successfully")

            return [TextContent(
                type="text",
                text=str(result)
            )]

        else:
            return [TextContent(
                type="text",
                text=f"Error: Unknown tool '{name}'"
            )]

    except Exception as e:
        logger.error(f"Error executing {name}: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=f"Error executing {name}: {str(e)}"
        )]


async def main():
    """Main entry point for the server."""
    # Ensure stdout is clean for MCP JSON-RPC communication
    sys.stdout.flush()
    sys.stderr.flush()

    logger.info("Starting Blender MCP Server...")

    if not BLENDER_AVAILABLE:
        logger.warning("Blender Python API not available - limited functionality")

    # Run the MCP server
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    except Exception as e:
        logger.error(f"MCP server error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    # Final check: ensure no buffered output in stdout
    sys.stdout.flush()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down Blender MCP Server...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
