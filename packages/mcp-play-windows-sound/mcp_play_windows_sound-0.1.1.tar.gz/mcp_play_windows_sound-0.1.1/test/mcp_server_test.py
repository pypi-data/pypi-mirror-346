import os
import json
import pytest
import tempfile
import asyncio
from unittest.mock import patch, MagicMock

from mcp_play_windows_sound.server import serve


@pytest.mark.asyncio
async def test_list_tools():
    """Test that the MCP server correctly defines the available tools."""
    mock_server = MagicMock()
    # Capture the tools registration
    with patch('mcp_play_windows_sound.server.Server', return_value=mock_server):
        # Create a dummy event loop and stop it immediately to avoid full execution
        await asyncio.create_task(asyncio.sleep(0))
        await serve()
    
    # Extract the list_tools function and call it
    list_tools_func = mock_server.list_tools.call_args[0][0]
    tools = await list_tools_func()
    
    # Verify we have exactly 2 tools
    assert len(tools) == 2
    
    # Check tool definitions
    tool_names = [tool.name for tool in tools]
    assert "list_sounds" in tool_names
    assert "play_sound" in tool_names
    
    # Verify the play_sound tool requires a sound_name parameter
    play_sound_tool = next(tool for tool in tools if tool.name == "play_sound")
    assert "sound_name" in play_sound_tool.inputSchema["properties"]
    assert "sound_name" in play_sound_tool.inputSchema["required"]


@pytest.mark.asyncio
async def test_call_tool_list_sounds():
    """Test that the MCP server can list sounds properly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create some test sound files
        for filename in ['test1.wav', 'test2.mp3']:
            with open(os.path.join(temp_dir, filename), 'w') as f:
                f.write('test audio data')
        
        mock_server = MagicMock()
        
        # Execute with our temp directory as the sound folder
        with patch('mcp_play_windows_sound.server.Server', return_value=mock_server):
            with patch('mcp_play_windows_sound.server.get_sound_folder', return_value=temp_dir):
                await asyncio.create_task(asyncio.sleep(0))
                await serve()
        
        # Extract the call_tool function and call it with list_sounds
        call_tool_func = mock_server.call_tool.call_args[0][0]
        result = await call_tool_func("list_sounds", {})
        
        # Should be a single TextContent result
        assert len(result) == 1
        assert result[0].type == "text"
        
        # Parse the JSON response
        response = json.loads(result[0].text)
        assert "sounds" in response
        assert "count" in response
        assert response["count"] == 2
        assert set(response["sounds"]) == {"test1.wav", "test2.mp3"}


@pytest.mark.asyncio
async def test_call_tool_play_sound_success():
    """Test that the MCP server can play a sound successfully."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test sound file
        test_filename = "test.wav"
        with open(os.path.join(temp_dir, test_filename), 'w') as f:
            f.write('test audio data')
        
        mock_server = MagicMock()
        
        # Mock subprocess.run to simulate successful playback
        with patch('mcp_play_windows_sound.server.Server', return_value=mock_server):
            with patch('mcp_play_windows_sound.server.get_sound_folder', return_value=temp_dir):
                with patch('subprocess.run'):
                    await asyncio.create_task(asyncio.sleep(0))
                    await serve()
        
        # Extract the call_tool function and call it with play_sound
        call_tool_func = mock_server.call_tool.call_args[0][0]
        result = await call_tool_func("play_sound", {"sound_name": test_filename})
        
        # Should be a single TextContent result
        assert len(result) == 1
        assert result[0].type == "text"
        
        # Parse the JSON response
        response = json.loads(result[0].text)
        assert response["sound_name"] == test_filename
        assert response["success"] is True
        assert "Successfully played sound" in response["message"]


@pytest.mark.asyncio
async def test_call_tool_play_sound_not_found():
    """Test that the MCP server handles non-existent sound files correctly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        mock_server = MagicMock()
        
        # Execute with our temp directory as the sound folder
        with patch('mcp_play_windows_sound.server.Server', return_value=mock_server):
            with patch('mcp_play_windows_sound.server.get_sound_folder', return_value=temp_dir):
                await asyncio.create_task(asyncio.sleep(0))
                await serve()
        
        # Extract the call_tool function and call it with a non-existent sound
        call_tool_func = mock_server.call_tool.call_args[0][0]
        result = await call_tool_func("play_sound", {"sound_name": "nonexistent.wav"})
        
        # Should be a single TextContent result
        assert len(result) == 1
        assert result[0].type == "text"
        
        # Parse the JSON response
        response = json.loads(result[0].text)
        assert response["sound_name"] == "nonexistent.wav"
        assert response["success"] is False
        assert "Sound file not found" in response["message"]


@pytest.mark.asyncio
async def test_call_tool_invalid_tool():
    """Test that the MCP server handles invalid tool names correctly."""
    mock_server = MagicMock()
    
    # Execute with mocked server
    with patch('mcp_play_windows_sound.server.Server', return_value=mock_server):
        await asyncio.create_task(asyncio.sleep(0))
        await serve()
    
    # Extract the call_tool function and call it with an invalid tool name
    call_tool_func = mock_server.call_tool.call_args[0][0]
    
    # Should raise a ValueError
    with pytest.raises(ValueError, match=r"Unknown tool: invalid_tool"):
        await call_tool_func("invalid_tool", {})


@pytest.mark.asyncio
async def test_call_tool_missing_arguments():
    """Test that the MCP server handles missing arguments correctly."""
    mock_server = MagicMock()
    
    # Execute with mocked server
    with patch('mcp_play_windows_sound.server.Server', return_value=mock_server):
        await asyncio.create_task(asyncio.sleep(0))
        await serve()
    
    # Extract the call_tool function and call it without the required sound_name
    call_tool_func = mock_server.call_tool.call_args[0][0]
    
    # Should raise a ValueError
    with pytest.raises(ValueError, match=r"Missing required argument: sound_name"):
        await call_tool_func("play_sound", {})