import os
import pytest
import tempfile
from unittest.mock import patch, MagicMock
from mcp.shared.exceptions import McpError

from mcp_play_windows_sound.server import SoundServer, get_default_sound_folder, get_sound_folder


def test_get_default_sound_folder():
    """Test the default sound folder logic based on platform."""
    with patch('platform.system', return_value='Windows'):
        with patch.dict('os.environ', {'WINDIR': 'C:\\Windows'}):
            assert get_default_sound_folder() == 'C:\\Windows\\Media'
    
    with patch('platform.system', return_value='Linux'):
        assert get_default_sound_folder() == '/usr/share/sounds'

    with patch('platform.system', return_value='Darwin'):
        assert get_default_sound_folder() == '/usr/share/sounds'


def test_get_sound_folder_with_override():
    """Test that sound folder override works correctly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Valid folder override
        assert get_sound_folder(temp_dir) == temp_dir
        
        # Invalid folder override
        with pytest.raises(McpError, match=r"Sound folder not found:"):
            get_sound_folder("/nonexistent/folder")


def test_list_sounds_empty_folder():
    """Test listing sounds in an empty folder."""
    with tempfile.TemporaryDirectory() as temp_dir:
        sound_server = SoundServer(temp_dir)
        result = sound_server.list_sounds()
        assert result.sounds == []
        assert result.count == 0


def test_list_sounds_with_files():
    """Test listing sounds with different file types."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create some test files
        for filename in ['sound1.wav', 'sound2.mp3', 'notsound.txt', 'sound3.WAV']:
            with open(os.path.join(temp_dir, filename), 'w') as f:
                f.write('test')
        
        sound_server = SoundServer(temp_dir)
        result = sound_server.list_sounds()
        
        # Should find 3 sound files (case insensitive extension)
        assert len(result.sounds) == 3
        assert result.count == 3
        assert set(result.sounds) == {'sound1.wav', 'sound2.mp3', 'sound3.WAV'}


def test_list_sounds_invalid_folder():
    """Test listing sounds with an invalid folder."""
    sound_server = SoundServer("/nonexistent/folder")
    with pytest.raises(McpError, match=r"Sound folder not found:"):
        sound_server.list_sounds()


@pytest.mark.parametrize(
    "platform_name,sound_name,exists,subprocess_side_effect,expected_success,expected_message_pattern",
    [
        # Windows success case
        (
            "Windows",
            "chimes.wav",
            True,
            None,
            True,
            "Successfully played sound: chimes.wav"
        ),
        # macOS success case
        (
            "Darwin",
            "ping.mp3",
            True,
            None,
            True,
            "Successfully played sound: ping.mp3"
        ),
        # Linux success case with aplay
        (
            "Linux",
            "beep.wav",
            True,
            [None, FileNotFoundError()],  # aplay works, paplay would fail
            True,
            "Successfully played sound: beep.wav"
        ),
        # Linux success case with paplay (aplay not found)
        (
            "Linux",
            "beep.wav",
            True,
            [FileNotFoundError(), None],  # aplay fails, paplay works
            True,
            "Successfully played sound: beep.wav"
        ),
        # Linux failure case (no players available)
        (
            "Linux",
            "beep.wav",
            True,
            [FileNotFoundError(), FileNotFoundError()],  # both aplay and paplay fail
            False,
            "No compatible sound player found"
        ),
        # File not found case
        (
            "Windows",
            "nonexistent.wav",
            False,
            None,
            False,
            "Sound file not found: nonexistent.wav"
        ),
        # Error during playback
        (
            "Windows",
            "error.wav",
            True,
            Exception("Command failed"),
            False,
            "Error playing sound"
        ),
    ],
)
def test_play_sound(platform_name, sound_name, exists, subprocess_side_effect, expected_success, expected_message_pattern):
    """Test playing sounds under various conditions."""
    with tempfile.TemporaryDirectory() as temp_dir:
        sound_path = os.path.join(temp_dir, sound_name)
        
        # Create the sound file if it should exist
        if exists:
            with open(sound_path, 'w') as f:
                f.write('test audio data')
        
        with patch('platform.system', return_value=platform_name):
            sound_server = SoundServer(temp_dir)
            
            # Handle different subprocess behaviors based on the test case
            if subprocess_side_effect is None:
                mock_run = MagicMock()
                with patch('subprocess.run', mock_run):
                    result = sound_server.play_sound(sound_name)
            elif isinstance(subprocess_side_effect, list):
                # For the Linux cases where we try multiple players
                mock_run = MagicMock(side_effect=subprocess_side_effect)
                with patch('subprocess.run', mock_run):
                    result = sound_server.play_sound(sound_name)
            else:
                # For error cases
                mock_run = MagicMock(side_effect=subprocess_side_effect)
                with patch('subprocess.run', mock_run):
                    result = sound_server.play_sound(sound_name)
            
            assert result.sound_name == sound_name
            assert result.success == expected_success
            assert expected_message_pattern in result.message