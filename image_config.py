import time
from OV5642_reg import (
    ov5642_320x240,
    ov5642_640x480,
    ov5642_1024x768,
    ov5642_1280x960,
    ov5642_1600x1200,
    ov5642_2048x1536,
    ov5642_2592x1944
)

# =====================================================
# RESOLUTION
# =====================================================

def set_resolution(cam, mode):
    """
    cam  : Arducam object instance
    mode : string resolution name

    Available:
        "QVGA"  -> 320x240
        "VGA"   -> 640x480
        "XGA"   -> 1024x768
        "SXGA"  -> 1280x960
        "UXGA"  -> 1600x1200
        "QXGA"  -> 2048x1536
        "5MP"   -> 2592x1944
    """

    modes = {
        "QVGA":  ov5642_320x240,
        "VGA":   ov5642_640x480,
        "XGA":   ov5642_1024x768,
        "SXGA":  ov5642_1280x960,
        "UXGA":  ov5642_1600x1200,
        "QXGA":  ov5642_2048x1536,
        "5MP":   ov5642_2592x1944,
    }

    mode = mode.upper()

    if mode not in modes:
        raise ValueError("Invalid resolution mode")

    cam.wrSensorRegs16_8(modes[mode])
    time.sleep(0.1)


# =====================================================
# JPEG QUALITY
# =====================================================

def set_jpeg_quality(cam, mode):
    """
    cam  : Arducam object instance
    mode : "HIGH", "MEDIUM", "LOW"

    HIGH   -> better quality, larger file
    LOW    -> smaller file, more compression
    """

    quality_map = {
        "HIGH":   0x04,
        "MEDIUM": 0x10,
        "LOW":    0x20,
    }

    mode = mode.upper()

    if mode not in quality_map:
        raise ValueError("Invalid JPEG quality mode")

    cam.wrSensorReg16_8(0x4407, quality_map[mode])


# =====================================================
# ORIENTATION (Mirror / Flip)
# =====================================================

def set_orientation(cam, mode):
    """
    cam  : Arducam object instance
    mode : "NORMAL", "MIRROR", "FLIP", "MIRROR_FLIP"
    """

    orientation_map = {
        "NORMAL":      0xA8,
        "MIRROR":      0xA8,
        "FLIP":        0xC8,
        "MIRROR_FLIP": 0xE8,
    }

    mode = mode.upper()

    if mode not in orientation_map:
        raise ValueError("Invalid orientation mode")

    cam.wrSensorReg16_8(0x3818, orientation_map[mode])


# =====================================================
# BRIGHTNESS
# =====================================================

def set_brightness(cam, mode):
    """
    cam  : Arducam object instance
    mode : "LOW", "NORMAL", "HIGH"
    """

    brightness_map = {
        "LOW":    0x00,
        "NORMAL": 0x10,
        "HIGH":   0x20,
    }

    mode = mode.upper()

    if mode not in brightness_map:
        raise ValueError("Invalid brightness mode")

    cam.wrSensorReg16_8(0x5587, brightness_map[mode])


# =====================================================
# CONTRAST
# =====================================================

def set_contrast(cam, mode):
    """
    cam  : Arducam object instance
    mode : "LOW", "NORMAL", "HIGH"
    """

    contrast_map = {
        "LOW":    0x10,
        "NORMAL": 0x20,
        "HIGH":   0x30,
    }

    mode = mode.upper()

    if mode not in contrast_map:
        raise ValueError("Invalid contrast mode")

    cam.wrSensorReg16_8(0x5586, contrast_map[mode])
