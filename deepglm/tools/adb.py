"""ADB command wrappers for Android device control.

This module provides functions for interacting with Android devices via ADB.
All functions are currently placeholder implementations that raise NotImplementedError.
They will be implemented in Phase 2 of the project.

The functions include type hints and detailed docstrings to guide future implementation.
"""

from typing import List


# Type aliases for future implementation
class DeviceInfo:
    """Information about an Android device.

    Attributes will include:
        device_id: Unique device identifier
        model: Device model name
        android_version: Android OS version
        status: Device status (online/offline)
    """

    pass


class PackageInfo:
    """Information about an installed Android package.

    Attributes will include:
        package_name: Package identifier (e.g., com.example.app)
        version: Package version string
        is_system: Whether this is a system app
    """

    pass


# Device Information Functions


def get_devices() -> List[str]:
    """Get list of connected Android device IDs.

    Returns:
        List of device IDs (e.g., ["emulator-5554", "192.168.1.100:5555"])

    Raises:
        NotImplementedError: This function is not yet implemented (Phase 2)

    Future Implementation:
        - Call `adb devices` command
        - Parse output to extract device IDs
        - Return list of connected devices
        - Handle case where no devices are connected
    """
    raise NotImplementedError(
        "get_devices() is not yet implemented. "
        "This will be implemented in Phase 2 with actual ADB integration."
    )


def get_device_info(device_id: str) -> DeviceInfo:
    """Get detailed information about a specific device.

    Args:
        device_id: The device identifier (e.g., "emulator-5554")

    Returns:
        DeviceInfo object with device details

    Raises:
        NotImplementedError: This function is not yet implemented (Phase 2)

    Future Implementation:
        - Call `adb -s {device_id} shell getprop` for device properties
        - Extract model, Android version, and other info
        - Return structured DeviceInfo object
    """
    raise NotImplementedError(
        "get_device_info() is not yet implemented. "
        "This will be implemented in Phase 2 with actual ADB integration."
    )


def get_battery_level(device_id: str) -> int:
    """Get the current battery level of a device.

    Args:
        device_id: The device identifier

    Returns:
        Battery percentage (0-100)

    Raises:
        NotImplementedError: This function is not yet implemented (Phase 2)
    """
    raise NotImplementedError(
        "get_battery_level() is not yet implemented. "
        "This will be implemented in Phase 2 with actual ADB integration."
    )


# Input Event Functions


def tap(device_id: str, x: int, y: int) -> bool:
    """Simulate a tap event at screen coordinates.

    Args:
        device_id: The device identifier
        x: X coordinate in pixels
        y: Y coordinate in pixels

    Returns:
        True if successful, False otherwise

    Raises:
        NotImplementedError: This function is not yet implemented (Phase 2)

    Future Implementation:
        - Execute: `adb -s {device_id} shell input tap {x} {y}`
        - Check return code for success
        - Handle device offline errors
    """
    raise NotImplementedError(
        "tap() is not yet implemented. "
        "This will be implemented in Phase 2 with actual ADB integration."
    )


def swipe(
    device_id: str,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    duration_ms: int = 300,
) -> bool:
    """Simulate a swipe gesture from one point to another.

    Args:
        device_id: The device identifier
        x1: Start X coordinate
        y1: Start Y coordinate
        x2: End X coordinate
        y2: End Y coordinate
        duration_ms: Duration of swipe in milliseconds

    Returns:
        True if successful, False otherwise

    Raises:
        NotImplementedError: This function is not yet implemented (Phase 2)
    """
    raise NotImplementedError(
        "swipe() is not yet implemented. "
        "This will be implemented in Phase 2 with actual ADB integration."
    )


def input_text(device_id: str, text: str) -> bool:
    """Input text into the currently focused field.

    Args:
        device_id: The device identifier
        text: The text to input (spaces and special chars must be escaped)

    Returns:
        True if successful, False otherwise

    Raises:
        NotImplementedError: This function is not yet implemented (Phase 2)
    """
    raise NotImplementedError(
        "input_text() is not yet implemented. "
        "This will be implemented in Phase 2 with actual ADB integration."
    )


def press_key(device_id: str, key_code: str) -> bool:
    """Press a hardware key (e.g., HOME, BACK, ENTER).

    Args:
        device_id: The device identifier
        key_code: Key code (e.g., "KEYCODE_HOME", "KEYCODE_BACK")

    Returns:
        True if successful, False otherwise

    Raises:
        NotImplementedError: This function is not yet implemented (Phase 2)
    """
    raise NotImplementedError(
        "press_key() is not yet implemented. "
        "This will be implemented in Phase 2 with actual ADB integration."
    )


# Screen Capture Functions


def capture_screen(device_id: str, save_path: str) -> str:
    """Capture the device screen and save to file.

    Args:
        device_id: The device identifier
        save_path: Local file path to save the screenshot

    Returns:
        Path to the saved screenshot file

    Raises:
        NotImplementedError: This function is not yet implemented (Phase 2)

    Future Implementation:
        - Execute: `adb -s {device_id} shell screencap -p /sdcard/screenshot.png`
        - Pull file: `adb -s {device_id} pull /sdcard/screenshot.png {save_path}`
        - Clean up device temp file
        - Return actual save path
    """
    raise NotImplementedError(
        "capture_screen() is not yet implemented. "
        "This will be implemented in Phase 2 with actual ADB integration."
    )


# App Management Functions


def list_packages(device_id: str) -> List[str]:
    """List all installed package names on the device.

    Args:
        device_id: The device identifier

    Returns:
        List of package names (e.g., ["com.android.settings", "com.example.app"])

    Raises:
        NotImplementedError: This function is not yet implemented (Phase 2)
    """
    raise NotImplementedError(
        "list_packages() is not yet implemented. "
        "This will be implemented in Phase 2 with actual ADB integration."
    )


def launch_app(device_id: str, package_name: str) -> bool:
    """Launch an app by package name.

    Args:
        device_id: The device identifier
        package_name: Package name (e.g., "com.example.app")

    Returns:
        True if successful, False otherwise

    Raises:
        NotImplementedError: This function is not yet implemented (Phase 2)
    """
    raise NotImplementedError(
        "launch_app() is not yet implemented. "
        "This will be implemented in Phase 2 with actual ADB integration."
    )


def force_stop_app(device_id: str, package_name: str) -> bool:
    """Force stop an app by package name.

    Args:
        device_id: The device identifier
        package_name: Package name

    Returns:
        True if successful, False otherwise

    Raises:
        NotImplementedError: This function is not yet implemented (Phase 2)
    """
    raise NotImplementedError(
        "force_stop_app() is not yet implemented. "
        "This will be implemented in Phase 2 with actual ADB integration."
    )


def install_app(device_id: str, apk_path: str) -> bool:
    """Install an APK file on the device.

    Args:
        device_id: The device identifier
        apk_path: Local path to the APK file

    Returns:
        True if successful, False otherwise

    Raises:
        NotImplementedError: This function is not yet implemented (Phase 2)
    """
    raise NotImplementedError(
        "install_app() is not yet implemented. "
        "This will be implemented in Phase 2 with actual ADB integration."
    )


def uninstall_app(device_id: str, package_name: str) -> bool:
    """Uninstall an app from the device.

    Args:
        device_id: The device identifier
        package_name: Package name to uninstall

    Returns:
        True if successful, False otherwise

    Raises:
        NotImplementedError: This function is not yet implemented (Phase 2)
    """
    raise NotImplementedError(
        "uninstall_app() is not yet implemented. "
        "This will be implemented in Phase 2 with actual ADB integration."
    )
