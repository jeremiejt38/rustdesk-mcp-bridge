"""Local desktop automation backend for the MCP bridge."""

from __future__ import annotations

import base64
import io
import json
from dataclasses import dataclass
from typing import Literal

import httpx
import mss
import pyautogui  # type: ignore[import-untyped]
from PIL import Image


@dataclass(frozen=True)
class Point:
    """2D screen coordinate."""

    x: int
    y: int


@dataclass(frozen=True)
class Size:
    """Screen or region size."""

    width: int
    height: int


class DesktopController:
    """Control the local desktop: capture screen, move/click mouse, type keys."""

    def __init__(self) -> None:
        self._mss = mss.mss()
        self._pyautogui = pyautogui
        self._pyautogui.FAILSAFE = True
        self._pyautogui.PAUSE = 0.05

    def get_screen_size(self) -> Size:
        """Return the size of the primary monitor."""
        monitor = self._mss.monitors[0]
        return Size(width=monitor["width"], height=monitor["height"])

    def list_monitors(self) -> list[dict[str, int]]:
        """Return the available monitors with their absolute virtual coordinates."""
        return [
            {
                "index": i,
                "left": monitor["left"],
                "top": monitor["top"],
                "width": monitor["width"],
                "height": monitor["height"],
            }
            for i, monitor in enumerate(self._mss.monitors[1:])
        ]

    def capture_screen(
        self,
        monitor_index: int | None = None,
        region: tuple[int, int, int, int] | None = None,
        format: Literal["png", "jpeg"] = "png",
        quality: int = 85,
    ) -> str:
        """Capture the screen and return it as a base64-encoded data URI.

        Args:
            monitor_index: Index of the monitor to capture (None = full virtual screen).
            region: Optional (left, top, width, height) rectangle.
            format: Output image format.
            quality: JPEG quality (ignored for PNG).

        Returns:
            Base64 data URI string, e.g. ``data:image/png;base64,...``.
        """
        if region:
            monitor = {"left": region[0], "top": region[1], "width": region[2], "height": region[3]}
        elif monitor_index is not None:
            monitor = self._mss.monitors[monitor_index + 1]
        else:
            monitor = self._mss.monitors[0]
        screenshot = self._mss.grab(monitor)
        image = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

        buffer = io.BytesIO()
        if format == "png":
            image.save(buffer, format="PNG")
            mime = "image/png"
        else:
            image.save(buffer, format="JPEG", quality=quality)
            mime = "image/jpeg"

        encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
        return f"data:{mime};base64,{encoded}"

    def move_mouse(self, x: int, y: int) -> None:
        """Move the cursor to absolute screen coordinates."""
        self._pyautogui.moveTo(x, y, duration=0.0)

    def click(
        self,
        x: int | None = None,
        y: int | None = None,
        button: Literal["left", "right", "middle"] = "left",
        clicks: int = 1,
        interval: float = 0.0,
    ) -> None:
        """Click at optional absolute coordinates or current cursor position."""
        if x is not None and y is not None:
            self._pyautogui.click(x, y, button=button, clicks=clicks, interval=interval)
        else:
            self._pyautogui.click(button=button, clicks=clicks, interval=interval)

    def mouse_down(self, button: Literal["left", "right", "middle"] = "left") -> None:
        """Press a mouse button without releasing it."""
        self._pyautogui.mouseDown(button=button)

    def mouse_up(self, button: Literal["left", "right", "middle"] = "left") -> None:
        """Release a mouse button."""
        self._pyautogui.mouseUp(button=button)

    def type_text(self, text: str, interval: float = 0.01) -> None:
        """Type a Unicode string."""
        self._pyautogui.typewrite(text, interval=interval)

    def send_key(self, key: str) -> None:
        """Press and release a single key or key combination.

        Combinations use plus signs, e.g. ``ctrl+a`` or ``ctrl+shift+t``.
        """
        parts = [part.strip() for part in key.split("+") if part.strip()]
        if len(parts) == 1:
            self._pyautogui.press(parts[0])
        else:
            self._pyautogui.hotkey(*parts)

    def _ollama_vision_query(
        self,
        prompt: str,
        image_data: str | None = None,
        model: str = "llava:7b",
        ollama_url: str = "http://localhost:11434/api/chat",
    ) -> str:
        """Ask a local Ollama vision model a question about an image.

        If ``image_data`` is not provided, the current screen is captured first.
        """
        if image_data is None:
            image_data = self.capture_screen(format="jpeg", quality=85).split(",", 1)[1]
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "images": [image_data],
                }
            ],
            "stream": False,
        }
        response = httpx.post(ollama_url, json=payload, timeout=180.0)
        response.raise_for_status()
        return str(response.json()["message"]["content"])

    def describe_image(
        self,
        image_uri: str,
        prompt: str = "Describe this image.",
        model: str = "llava:7b",
        ollama_url: str = "http://localhost:11434/api/chat",
    ) -> str:
        """Ask a local Ollama vision model about a provided base64 image URI."""
        image_data = image_uri.split(",", 1)[1]
        return self._ollama_vision_query(
            prompt, image_data=image_data, model=model, ollama_url=ollama_url
        )

    def describe_screen(
        self,
        prompt: str = "Describe this screenshot.",
        model: str = "llava:7b",
        ollama_url: str = "http://localhost:11434/api/chat",
    ) -> str:
        """Capture the screen and ask a local Ollama vision model to describe it.

        Args:
            prompt: The question/prompt sent to the vision model.
            model: Ollama model name supporting vision.
            ollama_url: Full URL to Ollama chat endpoint.

        Returns:
            The model's text response.
        """
        return self._ollama_vision_query(prompt, model=model, ollama_url=ollama_url)

    def locate_element(
        self,
        target: str,
        model: str = "llava:7b",
        monitor_index: int | None = None,
        ollama_url: str = "http://localhost:11434/api/chat",
    ) -> dict[str, int]:
        """Capture the screen and locate the center of a UI element by label.

        Args:
            target: Text label of the UI element to find.
            model: Ollama vision model name.
            monitor_index: Optional monitor index to restrict the search to.
            ollama_url: Full URL to Ollama chat endpoint.

        Returns:
            A dict with integer keys ``x`` and ``y`` representing the center of
            the element in absolute virtual-screen coordinates.
        """
        if monitor_index is not None:
            monitor = self._mss.monitors[monitor_index + 1]
            width = monitor["width"]
            height = monitor["height"]
            image = self.capture_screen(
                monitor_index=monitor_index, format="jpeg", quality=85
            ).split(",", 1)[1]
        else:
            size = self.get_screen_size()
            width = size.width
            height = size.height
            image = None
        prompt = (
            f"In this {width}x{height} screenshot, locate the UI element labeled '{target}'. "
            "Return the axis-aligned bounding box of that element as normalized "
            "coordinates [x_min, y_min, x_max, y_max] where each value is between 0 and 1, "
            "with (0,0) top-left and (1,1) bottom-right. Reply ONLY with the JSON array."
        )
        raw = self._ollama_vision_query(
            prompt, image_data=image, model=model, ollama_url=ollama_url
        )
        box = self._parse_bounding_box(raw, width, height)
        if monitor_index is not None:
            box["x"] += monitor["left"]
            box["y"] += monitor["top"]
        return box

    def _parse_bounding_box(self, raw: str, width: int, height: int) -> dict[str, int]:
        """Parse a model response containing a bounding box and return center coords."""
        # Try a JSON array first: [x_min, y_min, x_max, y_max]
        import re

        array_pattern = (
            r"\[\s*(\d?\.?\d+)\s*,\s*(\d?\.?\d+)\s*,"
            r"\s*(\d?\.?\d+)\s*,\s*(\d?\.?\d+)\s*\]"
        )
        array_match = re.search(array_pattern, raw)
        if array_match:
            return self._center_from_box(array_match.groups(), width, height)

        # Some models wrap the box in a JSON object (possibly keyed by label).
        for obj_match in re.finditer(r"\{[^\{\}]*\}", raw, re.S):
            try:
                obj = json.loads(obj_match.group(0))
            except Exception:
                continue
            if any(isinstance(v, dict) for v in obj.values()):
                for v in obj.values():
                    if isinstance(v, dict):
                        coords = self._extract_box(v)
                        if coords:
                            return self._center_from_box(coords, width, height)
            coords = self._extract_box(obj)
            if coords:
                return self._center_from_box(coords, width, height)

        # Fall back to a JSON object with x/y center coordinates.
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                coords = json.loads(raw[start : end + 1])
                return {"x": int(coords["x"]), "y": int(coords["y"])}
            except Exception:
                pass

        # Last resort: find x= and y= integer values.
        match = re.search(
            r"['\"]?x['\"]?\s*[:=]\s*(\d+).*?['\"]?y['\"]?\s*[:=]\s*(\d+)", raw, re.S
        )
        if match:
            return {"x": int(match.group(1)), "y": int(match.group(2))}

        raise ValueError(f"Could not parse coordinates from model response: {raw}")

    def _extract_box(self, data: dict) -> tuple[str, ...] | None:
        """Return (x_min, y_min, x_max, y_max) from a dict if present."""
        keys = (("x_min", "y_min", "x_max", "y_max"), ("x1", "y1", "x2", "y2"))
        for x0, y0, x1, y1 in keys:
            if x0 in data and y0 in data and x1 in data and y1 in data:
                return (str(data[x0]), str(data[y0]), str(data[x1]), str(data[y1]))
        return None

    def _center_from_box(
        self, values: tuple[str, ...], width: int, height: int
    ) -> dict[str, int]:
        x_min, y_min, x_max, y_max = (float(v) for v in values)
        return {
            "x": int(round((x_min + x_max) / 2 * width)),
            "y": int(round((y_min + y_max) / 2 * height)),
        }
