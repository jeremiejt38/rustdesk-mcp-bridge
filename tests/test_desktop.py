"""Tests for the desktop automation backend."""

from __future__ import annotations

import base64
import sys
from unittest.mock import MagicMock, patch

import pytest

# pyautogui requires a display; replace it with a mock before importing the
# desktop module so tests can run on headless CI machines.
sys.modules["pyautogui"] = MagicMock()

from rustdesk_mcp_bridge.desktop import (  # noqa: E402, I001
    DesktopController,
    Size,
)



@pytest.fixture
def controller() -> DesktopController:
    with (
        patch("rustdesk_mcp_bridge.desktop.mss") as mock_mss,
        patch("rustdesk_mcp_bridge.desktop.pyautogui") as mock_pyautogui,
    ):
        instance = DesktopController()
        instance._mss_instance = mock_mss.mss.return_value
        instance._pyautogui = mock_pyautogui
        yield instance


def test_get_screen_size(controller: DesktopController) -> None:
    controller._mss.monitors = [{"left": 0, "top": 0, "width": 1920, "height": 1080}]
    assert controller.get_screen_size() == Size(1920, 1080)


def test_capture_screen_png(controller: DesktopController) -> None:
    # Minimal BGRA 2x1 image: two blue-ish pixels.
    raw_bgra = b"\xff\x00\x00\xff\x00\xff\x00\xff"
    screenshot = MagicMock()
    screenshot.size = (2, 1)
    screenshot.bgra = raw_bgra
    controller._mss.grab.return_value = screenshot

    uri = controller.capture_screen(format="png")
    assert uri.startswith("data:image/png;base64,")
    decoded = base64.b64decode(uri.split(",")[1])
    assert decoded[:4] == b"\x89PNG"


def test_capture_screen_jpeg(controller: DesktopController) -> None:
    raw_bgra = b"\xff\x00\x00\xff\x00\xff\x00\xff"
    screenshot = MagicMock()
    screenshot.size = (2, 1)
    screenshot.bgra = raw_bgra
    controller._mss.grab.return_value = screenshot

    uri = controller.capture_screen(format="jpeg")
    assert uri.startswith("data:image/jpeg;base64,")


def test_move_mouse(controller: DesktopController) -> None:
    controller.move_mouse(100, 200)
    controller._pyautogui.moveTo.assert_called_once_with(100, 200, duration=0.0)


def test_click_with_coordinates(controller: DesktopController) -> None:
    controller.click(50, 75, button="right", clicks=2, interval=0.1)
    controller._pyautogui.click.assert_called_once_with(
        50, 75, button="right", clicks=2, interval=0.1
    )


def test_click_without_coordinates(controller: DesktopController) -> None:
    controller.click()
    controller._pyautogui.click.assert_called_once_with(
        button="left", clicks=1, interval=0.0
    )


def test_mouse_down_and_up(controller: DesktopController) -> None:
    controller.mouse_down("middle")
    controller.mouse_up("middle")
    controller._pyautogui.mouseDown.assert_called_once_with(button="middle")
    controller._pyautogui.mouseUp.assert_called_once_with(button="middle")


def test_type_text(controller: DesktopController) -> None:
    controller.type_text("hello")
    controller._pyautogui.typewrite.assert_called_once_with("hello", interval=0.01)


def test_send_key_single(controller: DesktopController) -> None:
    controller.send_key("enter")
    controller._pyautogui.press.assert_called_once_with("enter")


def test_send_key_combination(controller: DesktopController) -> None:
    controller.send_key("ctrl + a")
    controller._pyautogui.hotkey.assert_called_once_with("ctrl", "a")
