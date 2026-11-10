"""
   DWFConstants (definitions file for DWF library)
   Author:  Digilent, Inc.
   Revision:  2024-07-24

   Must install:                       
       Python 2.7 or 3
"""

from ctypes import c_int, c_ubyte, c_double

# device handle
# HDWF
hdwfNone = c_int(0)

# device enumeration filters
enumfilterAll = c_int(0)

enumfilterType = c_int(0x8000000)
enumfilterUSB = c_int(0x0000001)
enumfilterNetwork = c_int(0x0000002)
enumfilterAXI = c_int(0x0000004)
enumfilterRemote = c_int(0x1000000)
enumfilterAudio = c_int(0x2000000)
enumfilterDemo = c_int(0x4000000)

# device ID
devidEExplorer = c_int(1)
devidDiscovery = c_int(2)
devidDiscovery2 = c_int(3)
devidDDiscovery = c_int(4)
devidADP3X50 = c_int(6)
devidADP5250 = c_int(8)
devidDPS3340 = c_int(9)
devidDiscovery3 = c_int(10)
devidADP5470 = c_int(11)
devidADP5490 = c_int(12)
devidADP2230 = c_int(14)

# device version
devverEExplorerC = c_int(2)
devverEExplorerE = c_int(4)
devverEExplorerF = c_int(5)
devverDiscoveryA = c_int(1)
devverDiscoveryB = c_int(2)
devverDiscoveryC = c_int(3)

# trigger source
trigsrcNone = c_ubyte(0)
trigsrcPC = c_ubyte(1)
trigsrcDetectorAnalogIn = c_ubyte(2)
trigsrcDetectorDigitalIn = c_ubyte(3)
trigsrcAnalogIn = c_ubyte(4)
trigsrcDigitalIn = c_ubyte(5)
trigsrcDigitalOut = c_ubyte(6)
trigsrcAnalogOut1 = c_ubyte(7)
trigsrcAnalogOut2 = c_ubyte(8)
trigsrcAnalogOut3 = c_ubyte(9)
trigsrcAnalogOut4 = c_ubyte(10)
trigsrcExternal1 = c_ubyte(11)
trigsrcExternal2 = c_ubyte(12)
trigsrcExternal3 = c_ubyte(13)
trigsrcExternal4 = c_ubyte(14)
trigsrcHigh = c_ubyte(15)
trigsrcLow = c_ubyte(16)
trigsrcClock = c_ubyte(17)

# instrument states
DwfStateReady = c_ubyte(0)
DwfStateConfig = c_ubyte(4)
DwfStatePrefill = c_ubyte(5)
DwfStateArmed = c_ubyte(1)
DwfStateWait = c_ubyte(7)
DwfStateTriggered = c_ubyte(3)
DwfStateRunning = c_ubyte(3)
DwfStateNotDone = c_ubyte(6)
DwfStateDone = c_ubyte(2)

# DwfEnumConfigInfo
DECIAnalogInChannelCount = c_int(1)
DECIAnalogOutChannelCount = c_int(2)
DECIAnalogIOChannelCount = c_int(3)
DECIDigitalInChannelCount = c_int(4)
DECIDigitalOutChannelCount = c_int(5)
DECIDigitalIOChannelCount = c_int(6)
DECIAnalogInBufferSize = c_int(7)
DECIAnalogOutBufferSize = c_int(8)
DECIDigitalInBufferSize = c_int(9)
DECIDigitalOutBufferSize = c_int(10)

# acquisition modes:
acqmodeSingle = c_int(0)
acqmodeScanShift = c_int(1)
acqmodeScanScreen = c_int(2)
acqmodeRecord = c_int(3)
acqmodeOvers = c_int(4)
acqmodeSingle1 = c_int(5)

# analog acquisition filter:
filterDecimate = c_int(0)
filterAverage = c_int(1)
filterMinMax = c_int(2)
filterAverageFit = c_int(3)

# analog in trigger mode:
trigtypeEdge = c_int(0)
trigtypePulse = c_int(1)
trigtypeTransition = c_int(2)
trigtypeWindow = c_int(3)

# trigger slope:
DwfTriggerSlopeRise = c_int(0)
DwfTriggerSlopeFall = c_int(1)
DwfTriggerSlopeEither = c_int(2)

# trigger length condition
triglenLess = c_int(0)
triglenTimeout = c_int(1)
triglenMore = c_int(2)

# error codes for the functions:
dwfercNoErc = c_int(0)  #  No error occurred
dwfercUnknownError = c_int(1)  #  API waiting on pending API timed out
dwfercApiLockTimeout = c_int(2)  #  API waiting on pending API timed out
dwfercAlreadyOpened = c_int(3)  #  Device already opened
dwfercNotSupported = c_int(4)  #  Device not supported
dwfercInvalidParameter0 = c_int(16)  #  Invalid parameter sent in API call
dwfercInvalidParameter1 = c_int(17)  #  Invalid parameter sent in API call
dwfercInvalidParameter2 = c_int(18)  #  Invalid parameter sent in API call
dwfercInvalidParameter3 = c_int(19)  #  Invalid parameter sent in API call
dwfercInvalidParameter4 = c_int(20)  #  Invalid parameter sent in API call

# analog out signal types
funcDC = c_ubyte(0)
funcSine = c_ubyte(1)
funcSquare = c_ubyte(2)
funcTriangle = c_ubyte(3)
funcRampUp = c_ubyte(4)
funcRampDown = c_ubyte(5)
funcNoise = c_ubyte(6)
funcPulse = c_ubyte(7)
funcTrapezium = c_ubyte(8)
funcSinePower = c_ubyte(9)
funcSineNA = c_ubyte(10)
funcCustomPattern = c_ubyte(28)
funcPlayPattern = c_ubyte(29)
funcCustom = c_ubyte(30)
funcPlay = c_ubyte(31)

# analog io channel node types
analogioEnable = c_ubyte(1)
analogioVoltage = c_ubyte(2)
analogioCurrent = c_ubyte(3)
analogioPower = c_ubyte(4)
analogioTemperature = c_ubyte(5)
analogioDmm = c_ubyte(6)
analogioRange = c_ubyte(7)
analogioMeasure = c_ubyte(8)
analogioTime = c_ubyte(9)
analogioFrequency = c_ubyte(10)
analogioResistance = c_ubyte(11)
analogioSlew = c_ubyte(12)

DwfDmmResistance = c_double(1)
DwfDmmContinuity = c_double(2)
DwfDmmDiode = c_double(3)
DwfDmmDCVoltage = c_double(4)
DwfDmmACVoltage = c_double(5)
DwfDmmDCCurrent = c_double(6)
DwfDmmACCurrent = c_double(7)
DwfDmmDCLowCurrent = c_double(8)
DwfDmmACLowCurrent = c_double(9)
DwfDmmTemperature = c_double(10)

AnalogOutNodeCarrier = c_int(0)
AnalogOutNodeFM = c_int(1)
AnalogOutNodeAM = c_int(2)

DwfAnalogOutIdleDisable = c_int(0)
DwfAnalogOutIdleOffset = c_int(1)
DwfAnalogOutIdleInitial = c_int(2)
DwfAnalogOutIdleHold = c_int(3)

DwfDigitalInClockSourceInternal = c_int(0)
DwfDigitalInClockSourceExternal = c_int(1)

DwfDigitalInSampleModeSimple = c_int(0)
# alternate samples: noise|sample|noise|sample|...
# where noise is more than 1 transition between 2 samples
DwfDigitalInSampleModeNoise = c_int(1)

DwfDigitalOutOutputPushPull = c_int(0)
DwfDigitalOutOutputOpenDrain = c_int(1)
DwfDigitalOutOutputOpenSource = c_int(2)
DwfDigitalOutOutputThreeState = c_int(3)

DwfDigitalOutTypePulse = c_int(0)
DwfDigitalOutTypeCustom = c_int(1)
DwfDigitalOutTypeRandom = c_int(2)
DwfDigitalOutTypeROM = c_int(3)
DwfDigitalOutTypeState = c_int(4)
DwfDigitalOutTypePlay = c_int(5)

DwfDigitalOutIdleInit = c_int(0)
DwfDigitalOutIdleLow = c_int(1)
DwfDigitalOutIdleHigh = c_int(2)
DwfDigitalOutIdleZet = c_int(3)

DwfAnalogImpedanceImpedance = c_int(0)
DwfAnalogImpedanceImpedancePhase = c_int(1)
DwfAnalogImpedanceResistance = c_int(2)
DwfAnalogImpedanceReactance = c_int(3)
DwfAnalogImpedanceAdmittance = c_int(4)
DwfAnalogImpedanceAdmittancePhase = c_int(5)
DwfAnalogImpedanceConductance = c_int(6)
DwfAnalogImpedanceSusceptance = c_int(7)
DwfAnalogImpedanceSeriesCapacitance = c_int(8)
DwfAnalogImpedanceParallelCapacitance = c_int(9)
DwfAnalogImpedanceSeriesInductance = c_int(10)
DwfAnalogImpedanceParallelInductance = c_int(11)
DwfAnalogImpedanceDissipation = c_int(12)
DwfAnalogImpedanceQuality = c_int(13)
DwfAnalogImpedanceVrms = c_int(14)
DwfAnalogImpedanceVreal = c_int(15)
DwfAnalogImpedanceVimag = c_int(16)
DwfAnalogImpedanceIrms = c_int(17)
DwfAnalogImpedanceIreal = c_int(18)
DwfAnalogImpedanceIimag = c_int(19)

DwfParamUsbPower = c_int(
    2
)  # 1 keep the USB power enabled even when AUX is connected, Analog Discovery 2
DwfParamLedBrightness = c_int(3)  # LED brightness 0 ... 100%, Digital Discovery
DwfParamOnClose = c_int(4)  # 0 continue, 1 stop, 2 shutdown
DwfParamAudioOut = c_int(5)  # 0 disable / 1 enable audio output, Analog Discovery 1, 2
DwfParamUsbLimit = c_int(
    6
)  # 0..1000 mA USB power limit, -1 no limit, Analog Discovery 1, 2
DwfParamAnalogOut = c_int(7)  # 0 disable / 1 enable
DwfParamFrequency = c_int(8)  # Hz
DwfParamExtFreq = c_int(9)  # Hz
DwfParamClockMode = c_int(10)  # 0 internal, 1 output, 2 input, 3 IO
DwfParamTempLimit = c_int(11)  # shutdown temperature
DwfParamFreqPhase = c_int(12)  # system clock phase in 360deg, relative to reference
DwfParamDigitalVoltage = c_int(13)  # digital IO voltage (mV)
DwfParamFreqPhaseSteps = c_int(14)  # number of phase steps, read-only


DwfWindowRectangular = c_int(0)
DwfWindowTriangular = c_int(1)
DwfWindowHamming = c_int(2)
DwfWindowHann = c_int(3)
DwfWindowCosine = c_int(4)
DwfWindowBlackmanHarris = c_int(5)
DwfWindowFlatTop = c_int(6)
DwfWindowKaiser = c_int(7)
DwfWindowBlackman = c_int(8)
DwfWindowFlatTopM = c_int(9)

DwfAnalogCouplingDC = c_int(0)
DwfAnalogCouplingAC = c_int(1)

DwfFiirWindow = c_int(0)
DwfFiirFir = c_int(1)
DwfFiirIirButterworth = c_int(2)
DwfFiirIirChebyshev = c_int(3)

DwfFiirLowPass = c_int(0)
DwfFiirHighPass = c_int(1)
DwfFiirBandPass = c_int(2)
DwfFiirBandStop = c_int(3)

DwfFiirRaw = c_int(0)
DwfFiirDecimate = c_int(1)
DwfFiirAverage = c_int(2)


# obsolete
# STS
stsRdy = c_ubyte(0)
stsArm = c_ubyte(1)
stsDone = c_ubyte(2)
stsTrig = c_ubyte(3)
stsCfg = c_ubyte(4)
stsPrefill = c_ubyte(5)
stsNotDone = c_ubyte(6)
stsTrigDly = c_ubyte(7)
stsError = c_ubyte(8)
stsBusy = c_ubyte(9)
stsStop = c_ubyte(10)

# TRIGCOND
trigcondRisingPositive = c_int(0)
trigcondFallingNegative = c_int(1)

# use device id
enumfilterEExplorer = c_int(1)
enumfilterDiscovery = c_int(2)
enumfilterDiscovery2 = c_int(3)
enumfilterDDiscovery = c_int(4)
