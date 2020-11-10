---
title: Release notes
nav_order: 99
---

![Microchip logo](https://raw.githubusercontent.com/wiki/Microchip-MPLAB-Harmony/Microchip-MPLAB-Harmony.github.io/images/microchip_logo.png)
![Harmony logo small](https://raw.githubusercontent.com/wiki/Microchip-MPLAB-Harmony/Microchip-MPLAB-Harmony.github.io/images/microchip_mplab_harmony_logo_small.png)

# Microchip MPLAB® Harmony 3 Release Notes

## Graphics Release v3.7.1 (Aria Archive)
### Updates

* M32DC-97 - Fix for textfield widget issues
* MH3-45200 - 180 degree rotated fill fix for gfx2d gpu
* MH3-45615 - Fix buffer swapping in LCDC driver
* MH3-45616 - Enable alpha-blended Nano2D GPU fills

### Known Issues

* Aria: Code is compliant to MISRA C 2012 Mandatory guidelines, with the exception of Rule 9.1 (Code 530). In gfx.c, the variable args is falsely detected in violation of Code 530: "Symbol not initialized" at line 358. In fact, va_start at line 358 is exactly where args is initialized.
* Aria: When regenerating demo applications, keep all code between comments \/\/CUSTOM CODE and \/\/END OF CUSTOM CODE. Custom code is added to perform specific functionality.
* Applications running on SAM E70 in combination with LCC will observe visual rendering artifacts on display during SD card R/W access. There is no loss in SD Card data.
* For applications on SAM E54 + CPRO with the 24-bit passthrough board, Pin 7 of the EXT1 connector should drive the backlight. However, on rev1.0 of the board, it is not connected to any pin on the MCU. As a workaround, it needs to be connected to a v3.3 pin.

For a list of post release issues that affect this release, refer to MPLAB Harmony [GFX Issues and Errata](https://github.com/Microchip-MPLAB-Harmony/gfx/wiki/Issues-and-Errata).

### Development Tools

* [MPLAB® X IDE v5.40 or above](https://www.microchip.com/mplab/mplab-x-ide)
* [MPLAB® XC32 C/C++ Compiler v2.41](https://www.microchip.com/mplab/compilers)
* MPLAB® X IDE plug-ins:
    * MPLAB® Harmony Configurator (MHC) v3.4.2 and above.

### Dependent Components

* [BSP v3.7.0](https://github.com/Microchip-MPLAB-Harmony/bsp/releases/tag/v3.7.0)
* [Core v3.7.2 ](https://github.com/Microchip-MPLAB-Harmony/core/releases/tag/v3.7.2)
* [dev_packs v3.7.0 ](https://github.com/Microchip-MPLAB-Harmony/dev_packs/releases/tag/v3.7.0)
* [Harmony 3 USB v3.6.0](https://github.com/Microchip-MPLAB-Harmony/usb/releases/tag/v3.6.0)
* [Harmony 3 CMSIS-FreeRTOS v10.2.0](https://github.com/ARM-software/CMSIS-FreeRTOS)
* [IAR Embedded WorkBench ARM v8.40.1](https://www.iar.com/iar-embedded-workbench/#!?architecture=Arm)




