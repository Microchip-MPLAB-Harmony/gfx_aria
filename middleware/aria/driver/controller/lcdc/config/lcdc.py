# coding: utf-8
##############################################################################
# Copyright (C) 2018 Microchip Technology Inc. and its subsidiaries.
#
# Subject to your compliance with these terms, you may use Microchip software
# and any derivatives exclusively with Microchip products. It is your
# responsibility to comply with third party license terms applicable to your
# use of third party software (including open source software) that may
# accompany Microchip software.
#
# THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
# EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
# WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
# PARTICULAR PURPOSE.
#
# IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE,
# INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND
# WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS
# BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
# FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
# ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
# THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
##############################################################################

def instantiateComponent(comp):
	projectPath = "config/" + Variables.get("__CONFIGURATION_NAME") + "/gfx/driver/lcdc"
	
	HALConnected = comp.createBooleanSymbol("HALConnected", None)
	HALConnected.setVisible(False)
	HALConnected.setDependencies(onHALConnected, ["HALConnected"])
	
	# these two symbols are read by the HAL for initialization purposes
	# they must match the function names in the actual driver code
	DriverInfoFunction = comp.createStringSymbol("DriverInfoFunction", None)
	DriverInfoFunction.setLabel("Driver Info Function Name")
	DriverInfoFunction.setReadOnly(True)
	DriverInfoFunction.setDefaultValue("driverLCDCInfoGet")
	DriverInfoFunction.setVisible(False)
	
	DriverInitFunction = comp.createStringSymbol("DriverInitFunction", None)
	DriverInitFunction.setLabel("Driver Init Function Name")
	DriverInitFunction.setReadOnly(True)
	DriverInitFunction.setDefaultValue("driverLCDCContextInitialize")
	DriverInitFunction.setVisible(False)
	
	# configuration options
	HALComment = comp.createCommentSymbol("HALComment", None)
	HALComment.setLabel("Some settings are being managed by the GFX Core and have been hidden.")
	HALComment.setVisible(False)
	
	DisplayWidth = comp.createIntegerSymbol("DisplayWidth", None)
	DisplayWidth.setLabel("Width")
	DisplayWidth.setDescription("The width of the frame buffer in pixels.")
	DisplayWidth.setDefaultValue(480)
	DisplayWidth.setMin(1)

	DisplayHeight = comp.createIntegerSymbol("DisplayHeight", None)
	DisplayHeight.setLabel("Height")
	DisplayHeight.setDescription("The height of the frame buffer in pixels.")
	DisplayHeight.setDefaultValue(272)
	DisplayHeight.setMin(1)

	DisplayTimingOptionsEnabled = comp.createBooleanSymbol("DisplayTimingOptionsEnabled", None)
	DisplayTimingOptionsEnabled.setLabel("Display Timing Options Enabled")
	DisplayTimingOptionsEnabled.setDescription("Hints to the HAL if display timing is configurable for this display.")
	DisplayTimingOptionsEnabled.setDefaultValue(True)
	DisplayTimingOptionsEnabled.setVisible(False)

	OutputColorMode = comp.createKeyValueSetSymbol("OutputColorMode", None)
	OutputColorMode.setLabel("Output Color Mode")
	OutputColorMode.setOutputMode("Value")
	OutputColorMode.setDescription("Output Color Mode")
	OutputColorMode.addKey("12 BPP", "LCDC_OUTPUT_COLOR_MODE_12BPP", "12 bits per pixel")
	OutputColorMode.addKey("16 BPP", "LCDC_OUTPUT_COLOR_MODE_16BPP", "16 bits per pixel")
	OutputColorMode.addKey("18 BPP", "LCDC_OUTPUT_COLOR_MODE_18BPP", "18 bits per pixel")
	OutputColorMode.addKey("24 BPP", "LCDC_OUTPUT_COLOR_MODE_24BPP", "24 bits per pixel")
	OutputColorMode.setDefaultValue(3)

	DisplayGuardTime = comp.createIntegerSymbol("DisplayGuardTime", None)
	DisplayGuardTime.setLabel("Display Guard Time (Frames)")
	DisplayGuardTime.setDescription("Number of frames inserted before and after LCDDISP assertion.")
	DisplayGuardTime.setDefaultValue(30)
	DisplayGuardTime.setMin(1)

	### Clock Settings Menu
	ClockSettingsMenu = comp.createMenuSymbol("ClockSettingsMenu", None)
	ClockSettingsMenu.setLabel("Clock Settings")

	#### Get the master clock source value
	MasterClockSource = comp.createComboSymbol("MasterClockSource", ClockSettingsMenu, ["CLK_MCK"])
	MasterClockSource.setLabel("Master Clock Source")
	MasterClockSource.setDescription("The source master clock")
	MasterClockSource.setDefaultValue("CLK_MCK")
	
	MasterClockValue = 166000000
	try:
		if ("9X60" in str(Variables.get("__PROCESSOR"))):
			MasterClockValue = Database.getSymbolValue("core", "MCK_FREQUENCY")
		else:
			MasterClockValue = Database.getSymbolValue("core", "MCK_CLK_FREQUENCY")
	except:
		print(MasterClockSource.getValue() + " symbol not found")
		MasterClockValue = 200000000

	MasterClockSourceValue = comp.createIntegerSymbol("MasterClockSourceValue", ClockSettingsMenu)
	MasterClockSourceValue.setLabel("Master Clock (Hz)")
	MasterClockSourceValue.setReadOnly(True)
	MasterClockSourceValue.setDescription("The source master clock.")
	MasterClockSourceValue.setDefaultValue(MasterClockValue)
	MasterClockSourceValue.setUseSingleDynamicValue(True)
	MasterClockSourceValue.setMin(1)
	
	PixelClockDiv = comp.createIntegerSymbol("PixelClockDiv", ClockSettingsMenu)
	PixelClockDiv.setLabel("Clock Divider")
	PixelClockDiv.setDescription("The divider value used to generate pixel clock from clock source.")
	PixelClockDiv.setDefaultValue(7)
	PixelClockDiv.setMin(2)
	PixelClockDiv.setMax(32)
	PixelClockDiv.setDependencies(onPixelClockDivSet, ["PixelClockDiv"])
	
	defaultClockValue = MasterClockSourceValue.getValue() / PixelClockDiv.getValue() 

	PixelClock = comp.createIntegerSymbol("PixelClock", ClockSettingsMenu)
	PixelClock.setLabel("Pixel Clock (Hz)")
	PixelClock.setDescription("The approximate pixel clock frequency generated by the LCDC.")
	PixelClock.setDefaultValue(defaultClockValue)
	PixelClock.setMin(1)
	PixelClock.setReadOnly(True)

	### Layer Configuration Menu
	LayerConfigurationMenu = comp.createMenuSymbol("LayerConfigurationMenu", None)
	LayerConfigurationMenu.setLabel("Layer Configuration")
	
	EnableLayersMenu = comp.createMenuSymbol("EnableLayersMenu", LayerConfigurationMenu)
	EnableLayersMenu.setLabel("Enable Layers")
	
	BaseLayerEnable = comp.createBooleanSymbol("BaseLayerEnable", EnableLayersMenu)
	BaseLayerEnable.setLabel("Base Layer")
	BaseLayerEnable.setDescription("Enables Base Layer (always enabled)")
	BaseLayerEnable.setDefaultValue(True)
	BaseLayerEnable.setReadOnly(True)
	BaseLayerEnable.setDependencies(OnLayersEnabled, ["BaseLayerEnable"])
	
	Overlay1LayerEnable = comp.createBooleanSymbol("Overlay1LayerEnable", EnableLayersMenu)
	Overlay1LayerEnable.setLabel("Overlay 1")
	Overlay1LayerEnable.setDescription("Enables Overlay1")
	Overlay1LayerEnable.setDefaultValue(True)
	Overlay1LayerEnable.setDependencies(OnLayersEnabled, ["Overlay1LayerEnable"])
	
	HEOLayerEnable = comp.createBooleanSymbol("HEOLayerEnable", EnableLayersMenu)
	HEOLayerEnable.setLabel("High-End Overlay (HEO)")
	HEOLayerEnable.setDescription("Enables High-End Overlay")
	HEOLayerEnable.setDefaultValue(False)
	HEOLayerEnable.setReadOnly(True)
	HEOLayerEnable.setDependencies(OnLayersEnabled, ["HEOLayerEnable"])
	
	Overlay2LayerEnable = comp.createBooleanSymbol("Overlay2LayerEnable", EnableLayersMenu)
	Overlay2LayerEnable.setLabel("Overlay 2")
	Overlay2LayerEnable.setDescription("Enables Overlay2")
	Overlay2LayerEnable.setDefaultValue(True)
	Overlay2LayerEnable.setDependencies(OnLayersEnabled, ["Overlay2LayerEnable"])
	
	GlobalAlphaEnable = comp.createBooleanSymbol("GlobalAlphaEnable", LayerConfigurationMenu)
	GlobalAlphaEnable.setLabel("Enable Global Alpha")
	GlobalAlphaEnable.setDescription("Enables Global Alpha control of all layers. This disables local alpha for color modes with per pixel alpha channel.")
	GlobalAlphaEnable.setDefaultValue(False)
	
	#Shadow symbol counter for number of layers used - not user modifiable (hidden)
	TotalNumLayers = comp.createIntegerSymbol("TotalNumLayers", LayerConfigurationMenu)
	TotalNumLayers.setLabel("Number of Layers")
	TotalNumLayers.setDescription("Number of layers enabled")
	TotalNumLayers.setVisible(False)
	
	### Display Timing Settings
	DisplaySettingsMenu = comp.createMenuSymbol("DisplaySettingsMenu", None)
	DisplaySettingsMenu.setLabel("Display Settings")

	DisplayBacklightEnable = comp.createIntegerSymbol("DisplayBacklightEnable", DisplaySettingsMenu)
	DisplayBacklightEnable.setLabel("Back Light Enable Value")
	DisplayBacklightEnable.setDescription("The value used to enable the display back light.")
	DisplayBacklightEnable.setDefaultValue(1)

	DisplayVSYNCNegative = comp.createBooleanSymbol("DisplayVSYNCNegative", DisplaySettingsMenu)
	DisplayVSYNCNegative.setLabel("VSYNC Negative?")
	DisplayVSYNCNegative.setDescription("Indicates if this display requries negative VSYNC polarity.")
	DisplayVSYNCNegative.setDefaultValue(True)

	DisplayHSYNCNegative = comp.createBooleanSymbol("DisplayHSYNCNegative", DisplaySettingsMenu)
	DisplayHSYNCNegative.setLabel("HSYNC Negative?")
	DisplayHSYNCNegative.setDescription("Indicates if this display requries negative HSYNC polarity.")
	DisplayHSYNCNegative.setDefaultValue(True)

	DisplayDataEnable = comp.createBooleanSymbol("DisplayDataEnable", DisplaySettingsMenu)
	DisplayDataEnable.setLabel("Use Data Enable?")
	DisplayDataEnable.setDescription("Indicates if this display requries the use of the Data Enable line.")
	DisplayDataEnable.setDefaultValue(True)

	DisplayDataEnablePolarity = comp.createBooleanSymbol("DisplayDataEnablePolarity", DisplaySettingsMenu)
	DisplayDataEnablePolarity.setLabel("Data Enable Polarity Positive?")
	DisplayDataEnablePolarity.setDescription("Indicates if this display Data Enable polarity is positive.")
	DisplayDataEnablePolarity.setDefaultValue(True)

	##### LCDC Does not control the Chip Select I/O, disable and hide
	DisplayUseChipSelect = comp.createBooleanSymbol("DisplayUseChipSelect", DisplaySettingsMenu)
	DisplayUseChipSelect.setLabel("Use Chip Select?")
	DisplayUseChipSelect.setDescription("Indicates if this display uses the chip select line.")
	DisplayUseChipSelect.setDefaultValue(False)
	DisplayUseChipSelect.setVisible(False)

	DisplayChipSelectPolarity = comp.createBooleanSymbol("DisplayChipSelectPolarity", DisplaySettingsMenu)
	DisplayChipSelectPolarity.setLabel("Chip Select Polarity Positive?")
	DisplayChipSelectPolarity.setDescription("Indicates if this display chip select line should be positive.")
	DisplayChipSelectPolarity.setDefaultValue(True)
	DisplayChipSelectPolarity.setVisible(False)
	
	DisplayUseReset = comp.createBooleanSymbol("DisplayUseReset", DisplaySettingsMenu)
	DisplayUseReset.setLabel("Use Reset?")
	DisplayUseReset.setDescription("Indicates if this display reset line should be used.")
	DisplayUseReset.setDefaultValue(True)
	DisplayUseReset.setVisible(False)

	DisplayResetPolarity = comp.createBooleanSymbol("DisplayResetPolarity", DisplaySettingsMenu)
	DisplayResetPolarity.setLabel("Reset Polarity Positive?")
	DisplayResetPolarity.setDescription("Indicates if this display reset line should be reset positive.")
	DisplayResetPolarity.setDefaultValue(True)
	DisplayResetPolarity.setVisible(False)
	### End of unused settings

	### Frame buffer settings
	FrameBufferSettingsMenu = comp.createMenuSymbol("FrameBufferSettingsMenu", None)
	FrameBufferSettingsMenu.setLabel("Frame Buffer Settings")
	
	FrameBufferColorMode = comp.createKeyValueSetSymbol("FrameBufferColorMode", FrameBufferSettingsMenu)
	FrameBufferColorMode.setLabel("FrameBuffer Color Mode")
	FrameBufferColorMode.setOutputMode("Value")
	FrameBufferColorMode.setDescription("FrameBuffer Color Mode")
	FrameBufferColorMode.addKey("GS_8", "GFX_COLOR_MODE_GS_8", "Grayscale or Palette 8bpp")
	FrameBufferColorMode.addKey("RGB_565", "GFX_COLOR_MODE_RGB_565", "RGB565 16bpp")
	FrameBufferColorMode.addKey("RGB_888", "GFX_COLOR_MODE_RGB_888", "RGB888 24bpp")
	FrameBufferColorMode.addKey("RGBA_8888", "GFX_COLOR_MODE_RGBA_8888", "RGBA8888 32bpp")
	FrameBufferColorMode.addKey("ARGB_8888", "GFX_COLOR_MODE_ARGB_8888", "ARGB8888 32bpp")
	FrameBufferColorMode.setDefaultValue(3)

	DoubleBuffer = comp.createBooleanSymbol("DoubleBuffer", FrameBufferSettingsMenu)
	DoubleBuffer.setLabel("Use Double Buffering?")
	DoubleBuffer.setDescription("<html>Uses an additional buffer for off-screen drawing.<br>Eliminates screen tearing but doubles the required memory.</html>")

	UseCachedFrameBuffer = comp.createBooleanSymbol("UseCachedFrameBuffer", FrameBufferSettingsMenu)
	UseCachedFrameBuffer.setLabel("Uses Cached Frame Buffers?")
	UseCachedFrameBuffer.setDescription("Specifies if frame buffers are to be cached and need to be managed by the LCDC driver.")
	UseCachedFrameBuffer.setDefaultValue(False)
	UseCachedFrameBuffer.setDependencies(OnCacheEnabled, ["core.DATA_CACHE_ENABLE"])
	### End of frame buffer settings
	
	### Backlight PWM Menu
	BacklightPWMSettingsMenu = comp.createMenuSymbol("BacklightPWMSettingsMenu", None)
	BacklightPWMSettingsMenu.setLabel("Backlight PWM Settings")
	
	BacklightPWMEnable = comp.createBooleanSymbol("BacklightPWMEnable", BacklightPWMSettingsMenu)
	BacklightPWMEnable.setLabel("Enable Backlight PWM")
	BacklightPWMEnable.setDescription("Enables Control of the Backlight PWM")
	BacklightPWMEnable.setDefaultValue(True)

	BacklightPWMClockSource = comp.createComboSymbol("BacklightPWMClockSource", BacklightPWMSettingsMenu, ["CLK_SLOW", "CLK_MCK"])
	BacklightPWMClockSource.setLabel("PWM Clock Source")
	BacklightPWMClockSource.setDescription("The source PWM clock")
	BacklightPWMClockSource.setDefaultValue("CLK_MCK")

	BacklightPWMClockPrescaler = comp.createKeyValueSetSymbol("BacklightPWMClockPrescaler", BacklightPWMSettingsMenu)
	BacklightPWMClockPrescaler.setLabel("Backlight PWM Prescaler")
	BacklightPWMClockPrescaler.setOutputMode("Value")
	BacklightPWMClockPrescaler.setDescription("FrameBuffer Color Mode")
	BacklightPWMClockPrescaler.addKey("DIV_1", str(0), "Div 1")
	BacklightPWMClockPrescaler.addKey("DIV_2", str(1), "Div 2")
	BacklightPWMClockPrescaler.addKey("DIV_4", str(2), "Div 4")
	BacklightPWMClockPrescaler.addKey("DIV_8", str(3), "Div 8")
	BacklightPWMClockPrescaler.addKey("DIV_16", str(4), "Div 16")
	BacklightPWMClockPrescaler.addKey("DIV_32", str(5), "Div 32")
	BacklightPWMClockPrescaler.addKey("DIV_64", str(6), "Div 64")
	BacklightPWMClockPrescaler.setDefaultValue(5)
	
	BacklightBrightnessDefault = comp.createIntegerSymbol("BacklightBrightnessDefault", BacklightPWMSettingsMenu)
	BacklightBrightnessDefault.setLabel("Backlight Brightness %")
	BacklightBrightnessDefault.setDescription("Backlight Brightness Percent (0 - 100)")
	BacklightBrightnessDefault.setDefaultValue(100)
	BacklightBrightnessDefault.setMin(0)
	BacklightBrightnessDefault.setMax(100)
	### End of Backlight PWM Menu
	

	### Unsupported symbols, but may be queried by GFX HAL
	UnsupportedOptionsMenu = comp.createMenuSymbol("UnsupportedOptionsMenu", None)
	UnsupportedOptionsMenu.setLabel("Unsupported options group")
	UnsupportedOptionsMenu.setVisible(False)
	
	LCCRefresh = comp.createBooleanSymbol("LCCRefresh", UnsupportedOptionsMenu)
	LCCRefresh.setLabel("Use Aggressive Refresh Strategy?")
	
	PaletteMode = comp.createBooleanSymbol("PaletteMode", FrameBufferSettingsMenu)
	PaletteMode.setLabel("Use 8-bit Palette?")
	PaletteMode.setDescription("<html>Enables frame buffer compression.<br>Uses an 8-bit color lookup table to reduce the required<br>frame buffer memory size.  This also reduces the<br>maximum avilable color count to 256 and significantly<br>slows down display refresh speed.</html>")
	PaletteMode.setDefaultValue(False)
	PaletteMode.setVisible(False)
	### End of unsupported options
	
	# generated code files
	GFX_LCDC_C = comp.createFileSymbol("GFX_LCDC_C", None)
	GFX_LCDC_C.setDestPath("gfx/driver/controller/lcdc/")
	GFX_LCDC_C.setSourcePath("templates/drv_gfx_lcdc.c.ftl")
	GFX_LCDC_C.setOutputName("drv_gfx_lcdc.c")
	GFX_LCDC_C.setProjectPath(projectPath)
	GFX_LCDC_C.setType("SOURCE")
	GFX_LCDC_C.setMarkup(True)
	
	GFX_LCDC_H = comp.createFileSymbol("GFX_LCDC_H", None)
	GFX_LCDC_H.setSourcePath("templates/drv_gfx_lcdc.h")
	GFX_LCDC_H.setDestPath("gfx/driver/controller/lcdc/")
	GFX_LCDC_H.setOutputName("drv_gfx_lcdc.h")
	GFX_LCDC_H.setProjectPath(projectPath)
	GFX_LCDC_H.setType("HEADER")
	#GFX_LCDC_H.setMarkup(True)
	
	### Update the layers count - do this last
	numLayers = 0
	if (BaseLayerEnable.getValue() == True):
		numLayers += 1
	if (Overlay1LayerEnable.getValue() == True):
		numLayers += 1
	if (Overlay2LayerEnable.getValue() == True):
		numLayers += 1
	if (HEOLayerEnable.getValue() == True):
		numLayers += 1
	TotalNumLayers.setValue(numLayers, 1)

def onHALConnected(halConnected, event):
	halConnected.getComponent().getSymbolByID("HALComment").setVisible(event["value"] == True)
	halConnected.getComponent().getSymbolByID("DisplayWidth").setVisible(event["value"] == False)
	halConnected.getComponent().getSymbolByID("DisplayHeight").setVisible(event["value"] == False)
	halConnected.getComponent().getSymbolByID("DoubleBuffer").setVisible(event["value"] == False)
	halConnected.getComponent().getSymbolByID("PaletteMode").setVisible(event["value"] == False)
	halConnected.getComponent().getSymbolByID("DisplaySettingsMenu").setVisible(event["value"] == False)
	halConnected.getComponent().getSymbolByID("FrameBufferColorMode").setVisible(event["value"] == False)

	### Update the layer count hint in GFX HAL
	numLayers = halConnected.getComponent().getSymbolValue("TotalNumLayers")
	Database.setSymbolValue("gfx_hal", "HardwareLayerCountHint", numLayers, 1)
	
def OnCacheEnabled(cacheEnabled, event):
	cacheEnabled.getComponent().setSymbolValue("UseCachedFrameBuffer", event["value"] == True, 1)
	
def OnLayersEnabled(layerEnabled, event):
	numLayers = 0
	if (layerEnabled.getComponent().getSymbolValue("BaseLayerEnable") == True):
		numLayers += 1
	if (layerEnabled.getComponent().getSymbolValue("Overlay1LayerEnable") == True):
		numLayers += 1
	if (layerEnabled.getComponent().getSymbolValue("Overlay2LayerEnable") == True):
		numLayers += 1
	if (layerEnabled.getComponent().getSymbolValue("HEOLayerEnable") == True):
		numLayers += 1
	layerEnabled.getComponent().setSymbolValue("TotalNumLayers", numLayers, 1)
	if (layerEnabled.getComponent().getSymbolValue("HALConnected") == True):
		Database.setSymbolValue("gfx_hal", "HardwareLayerCountHint", numLayers, 1)

def onPixelClockDivSet(pixelClockDivSet, event):
	SourceClockValue = pixelClockDivSet.getComponent().getSymbolValue("MasterClockSourceValue")
	PixelClockValue = int(SourceClockValue) / int(event["value"])
	pixelClockDivSet.getComponent().setSymbolValue("PixelClock", PixelClockValue, 1)
	print("Pixel clock is " + str(PixelClockValue))
	if (pixelClockDivSet.getComponent().getSymbolValue("HALConnected") == True):
		Database.setSymbolValue("gfx_hal", "PixelClockHint", PixelClockValue, 1)
