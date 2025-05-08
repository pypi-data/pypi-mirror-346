import json
import os
import platform
import subprocess
from enum import Enum
from typing import Dict, List, Optional, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import EmbeddedResource, ImageContent, TextContent, Tool
from mcp.shared.exceptions import McpError
from pydantic import BaseModel


class SoundTools(str, Enum):
    PLAY_SOUND = "play_sound"
    LIST_SOUNDS = "list_sounds"


class SoundResult(BaseModel):
    sound_name: str
    success: bool
    message: str


class SoundListResult(BaseModel):
    sounds: List[str]
    count: int


def get_default_sound_folder() -> str:
    """Get the default Windows sound folder based on platform"""
    if platform.system() == "Windows":
        # Windows Media directory
        return os.path.join(os.environ["WINDIR"], "Media")
    else:
        # On non-Windows platforms, return a placeholder
        return "/usr/share/sounds"


def get_sound_folder(sound_folder_override: Optional[str] = None) -> str:
    """Get the sound folder path, with optional override"""
    if sound_folder_override:
        if os.path.isdir(sound_folder_override):
            return sound_folder_override
        raise McpError(f"Sound folder not found: {sound_folder_override}")
    
    return get_default_sound_folder()


class SoundServer:
    def __init__(self, sound_folder: str):
        self.sound_folder = sound_folder
    
    def list_sounds(self) -> SoundListResult:
        """List available Windows sounds"""
        try:
            sound_files = []
            if os.path.isdir(self.sound_folder):
                sound_files = [f for f in os.listdir(self.sound_folder) 
                               if os.path.isfile(os.path.join(self.sound_folder, f)) 
                               and f.lower().endswith(('.wav', '.mp3'))]
                
                return SoundListResult(
                    sounds=sound_files,
                    count=len(sound_files)
                )
            else:
                raise McpError(f"Sound folder not found: {self.sound_folder}")
        except Exception as e:
            raise McpError(f"Error listing sounds: {str(e)}")

    def play_sound(self, sound_name: str) -> SoundResult:
        """Play the specified Windows sound"""
        sound_path = os.path.join(self.sound_folder, sound_name)
        
        if not os.path.isfile(sound_path):
            return SoundResult(
                sound_name=sound_name,
                success=False,
                message=f"Sound file not found: {sound_name}"
            )
        
        try:
            if platform.system() == "Windows":
                # Use Windows-specific PowerShell command to play sound
                subprocess.run(
                    ["powershell", "-c", f"(New-Object Media.SoundPlayer '{sound_path}').PlaySync()"],
                    check=True
                )
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["afplay", sound_path], check=True)
            else:  # Linux and other systems
                # Try to use aplay or paplay if available
                try:
                    subprocess.run(["aplay", sound_path], check=True)
                except FileNotFoundError:
                    try:
                        subprocess.run(["paplay", sound_path], check=True)
                    except FileNotFoundError:
                        return SoundResult(
                            sound_name=sound_name,
                            success=False,
                            message="No compatible sound player found (aplay or paplay)"
                        )
                        
            return SoundResult(
                sound_name=sound_name,
                success=True,
                message=f"Successfully played sound: {sound_name}"
            )
        except Exception as e:
            return SoundResult(
                sound_name=sound_name,
                success=False,
                message=f"Error playing sound: {str(e)}"
            )


async def serve(sound_folder_override: Optional[str] = None) -> None:
    server = Server("mcp-play-windows-sound")
    sound_folder = get_sound_folder(sound_folder_override)
    sound_server = SoundServer(sound_folder)

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        """List available sound tools."""
        return [
            Tool(
                name=SoundTools.LIST_SOUNDS.value,
                description="List all available Windows system sounds",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            ),
            Tool(
                name=SoundTools.PLAY_SOUND.value,
                description="Play a Windows system sound by name",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "sound_name": {
                            "type": "string",
                            "description": "Name of the Windows sound file to play (including extension)",
                        }
                    },
                    "required": ["sound_name"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: Dict
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls for sound operations."""
        try:
            match name:
                case SoundTools.LIST_SOUNDS.value:
                    result = sound_server.list_sounds()
                
                case SoundTools.PLAY_SOUND.value:
                    sound_name = arguments.get("sound_name")
                    if not sound_name:
                        raise ValueError("Missing required argument: sound_name")
                    
                    result = sound_server.play_sound(sound_name)
                
                case _:
                    raise ValueError(f"Unknown tool: {name}")

            return [
                TextContent(type="text", text=json.dumps(result.model_dump(), indent=2))
            ]

        except Exception as e:
            raise ValueError(f"Error processing mcp-play-windows-sound query: {str(e)}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)