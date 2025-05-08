# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2025 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_usb_host_mouse`
================================================================================

Helper class that encapsulates the objects needed for user code to interact with
a USB mouse, draw a visible cursor, and determine when buttons are pressed.


* Author(s): Tim Cocks

Implementation Notes
--------------------

**Hardware:**

* `USB Wired Mouse - Two Buttons plus Wheel <https://www.adafruit.com/product/2025>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads


# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

import array

import adafruit_usb_host_descriptors
import supervisor
import usb
from displayio import OnDiskBitmap, TileGrid

__version__ = "1.0.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_USB_Host_Mouse.git"

BUTTONS = ["left", "right", "middle"]


def find_and_init_boot_mouse():
    mouse_interface_index, mouse_endpoint_address = None, None
    mouse_device = None

    # scan for connected USB device and loop over any found
    print("scanning usb")
    for device in usb.core.find(find_all=True):
        # print device info
        print(f"{device.idVendor:04x}:{device.idProduct:04x}")
        print(device.manufacturer, device.product)
        print()
        config_descriptor = adafruit_usb_host_descriptors.get_configuration_descriptor(device, 0)
        print(config_descriptor)

        _possible_interface_index, _possible_endpoint_address = (
            adafruit_usb_host_descriptors.find_boot_mouse_endpoint(device)
        )
        if _possible_interface_index is not None and _possible_endpoint_address is not None:
            mouse_device = device
            mouse_interface_index = _possible_interface_index
            mouse_endpoint_address = _possible_endpoint_address
            print(
                f"mouse interface: {mouse_interface_index} "
                + f"endpoint_address: {hex(mouse_endpoint_address)}"
            )

    mouse_was_attached = None
    if mouse_device is not None:
        # detach the kernel driver if needed
        if mouse_device.is_kernel_driver_active(0):
            mouse_was_attached = True
            mouse_device.detach_kernel_driver(0)
        else:
            mouse_was_attached = False

        # set configuration on the mouse so we can use it
        mouse_device.set_configuration()

        # load the mouse cursor bitmap
        mouse_bmp = OnDiskBitmap("/launcher_assets/mouse_cursor.bmp")

        # make the background pink pixels transparent
        mouse_bmp.pixel_shader.make_transparent(0)

        # create a TileGrid for the mouse, using its bitmap and pixel_shader
        mouse_tg = TileGrid(mouse_bmp, pixel_shader=mouse_bmp.pixel_shader)

        return BootMouse(mouse_device, mouse_endpoint_address, mouse_tg, mouse_was_attached)

    # if no mouse found
    return None


class BootMouse:
    def __init__(self, device, endpoint_address, tilegrid, was_attached):
        self.device = device
        self.tilegrid = tilegrid
        self.endpoint = endpoint_address
        self.buffer = array.array("b", [0] * 8)
        self.was_attached = was_attached

        self.display_size = (supervisor.runtime.display.width, supervisor.runtime.display.height)

    @property
    def x(self):
        return self.tilegrid.x

    @property
    def y(self):
        return self.tilegrid.y

    def release(self):
        if self.was_attached and not self.device.is_kernel_driver_active(0):
            self.device.attach_kernel_driver(0)

    def update(self):
        try:
            # attempt to read data from the mouse
            # 20ms timeout, so we don't block long if there
            # is no data
            count = self.device.read(self.endpoint, self.buffer, timeout=20)  # noqa: F841, var assigned but not used
        except usb.core.USBTimeoutError:
            # skip the rest if there is no data
            return None

        # update the mouse tilegrid x and y coordinates
        # based on the delta values read from the mouse
        self.tilegrid.x = max(0, min((self.display_size[0]) - 1, self.tilegrid.x + self.buffer[1]))
        self.tilegrid.y = max(0, min((self.display_size[1]) - 1, self.tilegrid.y + self.buffer[2]))

        pressed_btns = []
        for i, button in enumerate(BUTTONS):
            # check if each button is pressed using bitwise AND shifted
            # to the appropriate index for this button
            if self.buffer[0] & (1 << i) != 0:
                # append the button name to the string to show if
                # it is being clicked.
                pressed_btns.append(button)

        if len(pressed_btns) > 0:
            return pressed_btns
