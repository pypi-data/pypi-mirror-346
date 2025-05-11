"""
Tests for the CLI module
"""

import sys
import unittest
from unittest.mock import MagicMock, patch

from vlc_gesture_control.cli import main


class TestCLI(unittest.TestCase):
    """Test cases for the CLI module"""

    @patch("vlc_gesture_control.cli.version")
    @patch("argparse.ArgumentParser.parse_args")
    @patch("vlc_gesture_control.cli.lazy_import_cpu")
    def test_main_cpu_mode(self, mock_lazy_import_cpu, mock_parse_args, mock_version):
        """Test CLI in CPU mode calls the correct function"""
        # Setup
        mock_version.return_value = "1.1.2"
        mock_args = MagicMock()
        mock_args.mode = "cpu"
        mock_args.camera = 0
        mock_args.debug = False
        mock_parse_args.return_value = mock_args
        
        # Mock the lazy import to return a function
        mock_cpu_main = MagicMock()
        mock_lazy_import_cpu.return_value = mock_cpu_main

        # Call function
        main()

        # Assertions
        mock_lazy_import_cpu.assert_called_once()
        mock_cpu_main.assert_called_once_with(camera_index=0, debug=False)

    @patch("vlc_gesture_control.cli.version")
    @patch("argparse.ArgumentParser.parse_args")
    @patch("vlc_gesture_control.cli.lazy_import_gpu")
    def test_main_gpu_mode(self, mock_lazy_import_gpu, mock_parse_args, mock_version):
        """Test CLI in GPU mode calls the correct function"""
        # Setup
        mock_version.return_value = "1.1.2"
        mock_args = MagicMock()
        mock_args.mode = "gpu"
        mock_args.camera = 1
        mock_args.debug = True
        mock_parse_args.return_value = mock_args
        
        # Mock the lazy import to return a function
        mock_gpu_main = MagicMock()
        mock_lazy_import_gpu.return_value = mock_gpu_main

        # Call function
        main()

        # Assertions
        mock_lazy_import_gpu.assert_called_once()
        mock_gpu_main.assert_called_once_with(camera_index=1, debug=True)

    @patch("vlc_gesture_control.cli.version")
    @patch("argparse.ArgumentParser.parse_args")
    @patch("vlc_gesture_control.cli.lazy_import_gpu")
    @patch("vlc_gesture_control.cli.lazy_import_cpu")
    @patch("sys.exit")
    def test_main_import_error_gpu(self, mock_exit, mock_lazy_import_cpu, mock_lazy_import_gpu, mock_parse_args, mock_version):
        """Test CLI handles ImportError for GPU mode gracefully"""
        # Setup
        mock_version.return_value = "1.1.2"
        mock_args = MagicMock()
        mock_args.mode = "gpu"
        mock_args.debug = False
        mock_parse_args.return_value = mock_args
        
        # Simulate GPU not available
        mock_lazy_import_gpu.return_value = None
        # But CPU is available
        mock_cpu_main = MagicMock()
        mock_lazy_import_cpu.return_value = mock_cpu_main

        # Call function
        with patch("builtins.print") as mock_print:
            main()

        # Assertions
        mock_lazy_import_gpu.assert_called_once()
        mock_lazy_import_cpu.assert_called_once()
        mock_cpu_main.assert_called_once_with(camera_index=0, debug=False)
        mock_print.assert_any_call("Falling back to CPU mode due to missing GPU dependencies")

    @patch("vlc_gesture_control.cli.version")
    @patch("argparse.ArgumentParser.parse_args")
    @patch("vlc_gesture_control.cli.lazy_import_gpu")
    @patch("vlc_gesture_control.cli.lazy_import_cpu")
    @patch("sys.exit")
    def test_main_no_modules_available(self, mock_exit, mock_lazy_import_cpu, mock_lazy_import_gpu, mock_parse_args, mock_version):
        """Test CLI handles the case when no modules are available"""
        # Setup
        mock_version.return_value = "1.1.2"
        mock_args = MagicMock()
        mock_args.mode = "gpu"
        mock_args.debug = False
        mock_parse_args.return_value = mock_args
        
        # Simulate neither GPU nor CPU available
        mock_lazy_import_gpu.return_value = None
        mock_lazy_import_cpu.return_value = None

        # Call function
        with patch("builtins.print") as mock_print:
            main()

        # Check that sys.exit was called with code 1 (error)
        mock_exit.assert_called_once_with(1)

    @patch("vlc_gesture_control.cli.version")
    @patch("argparse.ArgumentParser.parse_args")
    @patch("vlc_gesture_control.cli.lazy_import_cpu")
    @patch("sys.exit")
    def test_main_keyboard_interrupt(self, mock_exit, mock_lazy_import_cpu, mock_parse_args, mock_version):
        """Test CLI handles KeyboardInterrupt gracefully"""
        # Setup
        mock_version.return_value = "1.1.2"
        mock_args = MagicMock()
        mock_args.mode = "cpu"
        mock_args.debug = False
        mock_parse_args.return_value = mock_args

        # Create a CPU main function that raises KeyboardInterrupt
        mock_cpu_main = MagicMock(side_effect=KeyboardInterrupt())
        mock_lazy_import_cpu.return_value = mock_cpu_main

        # Call function
        with patch("sys.stdout"):  # Suppress stdout for cleaner test output
            main()

        # Assertions
        mock_exit.assert_called_once_with(0)


if __name__ == "__main__":
    unittest.main()
