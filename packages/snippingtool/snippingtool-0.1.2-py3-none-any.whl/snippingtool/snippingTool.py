import win32api
import pyautogui
import tkinter as tk
from PIL import ImageGrab


class SnippingTool:
    """
    SnippingTool is a tool that allows users to capture a region of the screen by selecting it with the mouse.
    The tool provides an interface for the user to draw a selection rectangle, and once the mouse button is released,
    the selected area is captured as an image.
    """

    def __init__(self):
        """
        Initializes the SnippingTool instance by setting up the Tkinter window, canvas,
        and default values for the selection area and mouse state.
        """

        self._root = tk.Tk()
        self._root.attributes('-fullscreen', True)
        self._root.attributes('-topmost', True)
        self._root.attributes('-alpha', 0.3)
        self._root.configure(bg='black')
        self._root.config(cursor="crosshair")

        self._canvas = tk.Canvas(self._root, bg='black', highlightthickness=0)
        self._canvas.pack(fill=tk.BOTH, expand=True)

        self._first = (0, 0)
        self._last = (0, 0)
        self._selection_rect = None
        self._pressed = False
        self._started = False

    def _draw_selection(self, current):
        """
        Draws a rectangle on the canvas to represent the selection area.

        Args:
            current (tuple): The current (x, y) position of the mouse during the selection process.
        """

        x1, y1 = self._first
        x2, y2 = current
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        if self._selection_rect:
            self._canvas.delete(self._selection_rect)

        self._selection_rect = self._canvas.create_rectangle(x1, y1, x2, y2, outline='red', width=1, fill='gray80')

    def _capture_and_return_image(self):
        """
        Captures the area defined by the selection rectangle and returns the image and bounding box.

        Returns:
            tuple: A tuple containing the captured image and the bounding box of the selected area.

        Raises:
            RuntimeError: If the capture fails for any reason.
        """

        x1, y1 = self._first
        x2, y2 = self._last

        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        box = (x1, y1, x2, y2)

        try:
            image = ImageGrab.grab(bbox=box)
            return image, box
        except Exception as e:
            raise RuntimeError(f"Failed to capture image: {e}")

    def capture(self):
        """
        Waits for the user to select an area by dragging the mouse. Once the mouse button is released,
        the selected area is captured.

        Returns:
            tuple: A tuple containing the captured image and the bounding box of the selected area.
        """

        state_left = win32api.GetKeyState(0x01)

        while True:
            current_state = win32api.GetKeyState(0x01)
            mouse_position = pyautogui.position()

            if current_state != state_left:
                state_left = current_state
                self._pressed = current_state < 0

            try:
                if self._pressed:
                    if not self._started:
                        self._first = mouse_position

                    self._started = True
                    self._draw_selection(mouse_position)

                elif not self._pressed and self._started:
                    self._last = mouse_position
                    self._root.destroy()
                    return self._capture_and_return_image()

                self._root.update_idletasks()
                self._root.update()

            except Exception as e:
                raise RuntimeError(f"An error occurred during capture: {e}")
