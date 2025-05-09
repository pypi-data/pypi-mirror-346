# SnippingTool

SnippingTool is a simple and intuitive screen capture tool that allows you to select a region of the screen using your mouse. Once the area is selected, the tool captures the region as an image. It uses a transparent overlay to let you draw a selection area, and once you release the mouse button, the tool captures and returns the image.

## Usage

To use the SnippingTool, you just need to initialize the tool and call the `capture()` method. Here's a basic example of how to use it:

```python
from snippingtool import SnippingTool

# Create an instance of SnippingTool
snipping = SnippingTool()

# Capture a selected area of the screen
image, bounding_box = snipping.capture()

# Save the captured image to a file
image.save('captured_area.png')

# Print the bounding box of the captured area
print(f'Bounding box: {bounding_box}')
```

## License

This code is open-source and licensed under the MIT License. Feel free to use, modify, and distribute the code as per your requirements.