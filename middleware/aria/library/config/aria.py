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

def instantiateComponent(component):
	projectPath = "config/" + Variables.get("__CONFIGURATION_NAME") + "/gfx/libaria"
	
	component.setHelpFile("../../docs/help_harmony_gfx_html_alias.h")
	#component.setHelp("IDH_HTML_GFX_CMP__5__Aria_Graphics_LIbrary_Component")
	
	execfile(Module.getPath() + "/config/aria_config.py")
	execfile(Module.getPath() + "/utils/config/aria_utils.py")
	execfile(Module.getPath() + "/third_party/config/aria_thirdparty.py")
	execfile(Module.getPath() + "/config/aria_demomode.py")
	execfile(Module.getPath() + "/config/aria_rtos.py")
	execfile(Module.getPath() + "/config/aria_files.py")

	LIBARIA_SYS_DEFINITIONS_H = component.createFileSymbol("LIBARIA_SYS_DEFINITIONS_H", None)
	LIBARIA_SYS_DEFINITIONS_H.setType("STRING")
	LIBARIA_SYS_DEFINITIONS_H.setOutputName("core.LIST_SYSTEM_DEFINITIONS_H_INCLUDES")
	LIBARIA_SYS_DEFINITIONS_H.setSourcePath("templates/system/libaria_definitions.h.ftl")
	LIBARIA_SYS_DEFINITIONS_H.setMarkup(True)
	
	LIBARIA_SYS_INIT_C = component.createFileSymbol("LIBARIA_SYS_INIT_C", None)
	LIBARIA_SYS_INIT_C.setType("STRING")
	LIBARIA_SYS_INIT_C.setOutputName("core.LIST_SYSTEM_INIT_C_INITIALIZE_MIDDLEWARE")
	LIBARIA_SYS_INIT_C.setSourcePath("templates/system/libaria_init.c.ftl")
	LIBARIA_SYS_INIT_C.setMarkup(True)

	LIBARIA_SYS_TASK_C = component.createFileSymbol("LIBARIA_SYS_TASK_C", None)
	LIBARIA_SYS_TASK_C.setType("STRING")
	LIBARIA_SYS_TASK_C.setOutputName("core.LIST_SYSTEM_TASKS_C_CALL_LIB_TASKS")
	LIBARIA_SYS_TASK_C.setSourcePath("templates/system/libaria_tasks.c.ftl")
	LIBARIA_SYS_TASK_C.setMarkup(True)

	LIBARIA_SYS_RTOS_TASK_C = component.createFileSymbol("LIBARIA_SYS_RTOS_TASK_C", None)
	LIBARIA_SYS_RTOS_TASK_C.setType("STRING")
	LIBARIA_SYS_RTOS_TASK_C.setOutputName("core.LIST_SYSTEM_RTOS_TASKS_C_DEFINITIONS")
	LIBARIA_SYS_RTOS_TASK_C.setSourcePath("templates/system/libaria_rtos_tasks.c.ftl")
	LIBARIA_SYS_RTOS_TASK_C.setMarkup(True)
	LIBARIA_SYS_RTOS_TASK_C.setEnabled((Database.getSymbolValue("HarmonyCore", "SELECT_RTOS") != "BareMetal"))
	LIBARIA_SYS_RTOS_TASK_C.setDependencies(enableAriaRTOSTask, ["HarmonyCore.SELECT_RTOS"])
	
	Database.setSymbolValue("core", "XC32_HEAP_SIZE", 16384, 1) 

def onAttachmentConnected(source, target):
	if source["id"] == "gfx_hal":
		target["component"].setSymbolValue("GlobalPaletteModeHint", source["component"].getSymbolValue("useGlobalPalette"), 1)
		target["component"].setSymbolValue("DisableGlobalPaletteModeHint", True, 1)

def onAttachmentDisconnected(source, target):
	if source["id"] == "gfx_hal":
		target["component"].clearSymbolValue("GlobalPaletteModeHint")
		target["component"].clearSymbolValue("DisableGlobalPaletteModeHint")
	
def onDemoModeEnable(enableDemoMode, event):
	enableDemoMode.getComponent().getSymbolByID("demoModeRecordInput").setVisible(event["value"])
	enableDemoMode.getComponent().getSymbolByID("demoModeRecordTickPeriod").setVisible(event["value"])
	enableDemoMode.getComponent().getSymbolByID("demoModeMaxEvents").setVisible(event["value"])
	enableDemoMode.getComponent().getSymbolByID("demoModeIdleTimeout").setVisible(event["value"])
	enableDemoMode.getComponent().getSymbolByID("demoModeReplayDelay").setVisible(event["value"])
	event["source"].getSymbolByID("LIBARIA_DEMO_MODE_H").setEnabled(event["value"])
	event["source"].getSymbolByID("LIBARIA_DEMO_MODE_C").setEnabled(event["value"])
	
def showAriaRTOSMenu(symbol, event):
	symbol.setVisible(event["value"] != "BareMetal")
	symbol.getComponent().getSymbolByID("useRTOSExtensions").setValue(event["value"] != "BareMetal", 1)
	
def enableAriaRTOSExtensions(symbol, event):
	enableAriaExtensionsFiles(symbol.getComponent(), event["value"] == True)

def enableAriaRTOSSymbol(symbol, event):
	if (event["value"] == "True"):
		symbol.setEnabled(True)
	else:
		symbol.setEnabled(False)

def enableAriaExtensionsFiles(component, enable):
	print("Enabling extension files " + str(enable))
### Enable/Disable the RTOS extension files
	component.getSymbolByID("LIBARIA_RTOS_H").setEnabled(enable)
	component.getSymbolByID("LIBARIA_CONTEXT_RTOS_H").setEnabled(enable)
	component.getSymbolByID("LIBARIA_EVENT_RTOS_H").setEnabled(enable)
	component.getSymbolByID("LIBARIA_INPUT_RTOS_H").setEnabled(enable)
	component.getSymbolByID("LIBARIA_RTOS_C").setEnabled(enable)
	component.getSymbolByID("LIBARIA_CONTEXT_RTOS_C").setEnabled(enable)
	component.getSymbolByID("LIBARIA_EVENT_RTOS_C").setEnabled(enable)
	component.getSymbolByID("LIBARIA_INPUT_RTOS_C").setEnabled(enable)
	
#def useAriaRTOSExtensions(symbol, event):
#	symbol.getComponent().getSymbolByID("rtosFullBlockingMode").setVisible(event["value"] == True)
#	symbol.getComponent().getSymbolByID("rtosEnableTaskDelay").setValue(event["value"] == False, 1)
#	enableAriaExtensionsFiles(symbol.getComponent(), event["value"] == True)

def onEnableInputChanged(enableInput, event):
	enableInput.getComponent().setDependencyEnabled("sys_input", event["value"])
	
def onGenAriaDesignChanged(genAriaDesign, event):
	genAriaEvents = genAriaDesign.getComponent().getSymbolByID("genAriaDesign")
	genAriaEvents.setVisible(event["value"])
	genAriaEvents.setEnabled(event["value"])
	
	genAriaMacros = genAriaDesign.getComponent().getSymbolByID("genAriaMacros")
	genAriaMacros.setVisible(event["value"])
	genAriaMacros.setEnabled(event["value"])
	
def onJPEGEnableChanged(JPEGEnable, event):
	event["source"].getSymbolByID("GFXU_IMAGE_JPG_COMMON_H").setEnabled(event["value"])
	event["source"].getSymbolByID("GFXU_IMAGE_JPG_COMMON_C").setEnabled(event["value"])
	event["source"].getSymbolByID("JIDCTINT_C").setEnabled(event["value"])
	event["source"].getSymbolByID("GFXU_IMAGE_JPG_INTERNAL_C").setEnabled(event["value"])
	event["source"].getSymbolByID("GFXU_IMAGE_JPG_EXTERNAL_C").setEnabled(event["value"])
	
def onPNGEnableChanged(JPEGEnable, event):
	event["source"].getSymbolByID("GFXU_IMAGE_PNG_EXTERNAL_C").setEnabled(event["value"])
	event["source"].getSymbolByID("GFXU_IMAGE_PNG_INTERNAL_C").setEnabled(event["value"])
	event["source"].getSymbolByID("LODE_PNG_DECODER_H").setEnabled(event["value"])
	event["source"].getSymbolByID("LODE_PNG_DECODER_C").setEnabled(event["value"])
	
def onUseGlobalPaletteChanged(useGlobalPalette, event):
	# connected to HAL, update the global palette hint
	if event["source"].getDependencyComponent("gfx_hal") != None:
		Database.setSymbolValue("gfx_hal", "GlobalPaletteModeHint", event["value"], 1)
	
def enableAriaRTOSTask(symbol, event):
    if (event["value"] != "BareMetal"):
        symbol.setEnabled(True)
    else:
        symbol.setEnabled(False)

def onAppFileEnabled(symbol, event):
	symbol.setValue(event["value"])

def onAppNameChanged(symbol, event):
	appHeaderName = event["value"] + ".h"
	symbol.setValue(appHeaderName)