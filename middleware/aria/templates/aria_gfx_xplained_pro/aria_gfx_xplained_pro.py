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

componentsIDTable = ["HarmonyCore", "gfx_hal", "aria_gfx_library", "gfx_disp_atmxt-xpro_320x480", "gfx_driver_ili9488"]
autoConnectTable = [["gfx_hal", "gfx_display", "gfx_disp_atmxt-xpro_320x480", "gfx_display"],
					["aria_gfx_library", "gfx_hal", "gfx_hal", "gfx_hal"],
					["gfx_hal", "gfx_display_driver", "gfx_driver_ili9488", "gfx_driver_ili9488"]]
deactivateIDTable = ["FreeRTOS"]

execfile(Module.getPath() + "../common/pin_config.py")
execfile(Module.getPath() + "../common/bsp_utils.py")
execfile(Module.getPath() + "../common/display_utils.py")

pinConfigureFxn = configurePins
pinResetFxn = resetPins

#Add BSP support
execfile(Module.getPath() + "Support_BSP_SAM_E70_Xplained_Ultra.py")
execfile(Module.getPath() + "Support_BSP_SAM_C21_Xplained_Pro.py")
execfile(Module.getPath() + "Support_BSP_SAM_E54_Xplained_Pro.py")
execfile(Module.getPath() + "Support_BSP_SAM_E54_Curiosity_Ultra.py")
execfile(Module.getPath() + "Support_BSP_PIC32MZ_EF_Curiosity.py")

def enableConfigPins(bspID, configID, enable):
	global pinConfigureFxn
	if (enable == True):
		print("enableCOnfig " + configID)
	else:
		print("disableCOnfig " + configID)
	pinConfig = getBSPSupportNode(bspID, configID).getPinConfig()

	if (enable == True):
		pinConfigureFxn(pinConfig)
	else:
		pinResetFxn(pinConfig)

def enableConfig(bspID, configID, enable):
	componentIDTable = getBSPSupportNode(bspID, configID).getComponentActivateList()
	deactivateIDTable = getBSPSupportNode(bspID, configID).getComponentDeactivateList()
	autoConnectTable = getBSPSupportNode(bspID, configID).getComponentAutoConnectList()
	if (enable == True):
		if (componentIDTable != None):
			res = Database.activateComponents(componentIDTable)
		if (deactivateIDTable != None):
			res = Database.deactivateComponents(deactivateIDTable)
		if (autoConnectTable != None):
			res = Database.connectDependencies(autoConnectTable)
		try:
			getBSPSupportNode(bspID, configID).getEventCallbackFxn()("configure")
		except:
			print("No event callback for " + bspID + " configID.")
	elif (enable == False):
		if (componentIDTable != None):
			res = Database.deactivateComponents(componentIDTable)
		try:
			getBSPSupportNode(bspID, configID).getEventCallbackFxn()("unconfigure")
		except:
			print("No event callback for " + bspID + " configID.")
	enableConfigPins(bspID, configID, enable)

def configureDisplayInterface(bspID, interface):
	print("Configuring for " + str(interface) + " Interface.")
	if (bspID == None):
		print("No BSP used, will not configure")
	else:
		DisplayInterfaceList = getDisplayInterfaces(bspID)
		if (DisplayInterfaceList != None):
			if (str(interface) in DisplayInterfaceList):
				for val in DisplayInterfaceList:
					if (val != interface):
						enableConfig(bspID, val, False)
				enableConfig(bspID, interface, True)
			else:
				print(str(interface) + " display interface is not supported.")

def onDisplayInterfaceSelected(interfaceSelected, event):
	bspID = getSupportedBSP()
	newDisplayInterface= interfaceSelected.getComponent().getSymbolByID("DisplayInterface").getValue()
	currDisplayInterface = interfaceSelected.getComponent().getSymbolByID("currDisplayInterface").getValue()
	interfaceSelected.getComponent().getSymbolByID("currDisplayInterface").setValue(event["value"], 0)
	configureDisplayInterface(bspID, str(newDisplayInterface))

def instantiateComponent(templateComponent):
	global componentsIDTable
	global autoConnectTable
	global supportedBSPsIDList
	
	#Check if a supported BSP is loaded
	bspUsedKeyID = getSupportedBSP()
	
	DisplayInterfaceList = getDisplayInterfaces(bspUsedKeyID)

	#if there is no list, build the list from the interfaces for each supported BSP
	if (DisplayInterfaceList == None):
		DisplayInterfaceList = []
		bspSupportedList = getSupportedBSPList()
		for bsp in bspSupportedList:
			DisplayInterfaceList += getDisplayInterfaces(bsp)
	
	# Remove duplicates
	DisplayInterfaceList = list(dict.fromkeys(DisplayInterfaceList))

	DisplayInterface = templateComponent.createComboSymbol("DisplayInterface", None, DisplayInterfaceList)
	DisplayInterface.setLabel("Display Interface")
	DisplayInterface.setDescription("Configures the display controller interface to the maXTouch Xplained Pro.")
	DisplayInterface.setDependencies(onDisplayInterfaceSelected, ["DisplayInterface"])
	DisplayInterface.setVisible(True)

	# Shadow display interface symbol
	currDisplayInterface = templateComponent.createComboSymbol("currDisplayInterface", None, DisplayInterfaceList)
	currDisplayInterface.setVisible(False)

	res = Database.activateComponents(componentsIDTable)
	res = Database.connectDependencies(autoConnectTable)
	res = Database.deactivateComponents(deactivateIDTable);
	
	if (bspUsedKeyID != None):
		DisplayInterface.setDefaultValue(getDefaultDisplayInterface(bspUsedKeyID))
		currDisplayInterface.setDefaultValue(getDefaultDisplayInterface(bspUsedKeyID))
		configureDisplayInterface(bspUsedKeyID, str(currDisplayInterface.getValue()))
	else:
		print("No BSP used, only software components are configured. Please add board-specific components.")

