# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2025 mrv96
#
# SPDX-License-Identifier: MIT
"""
`ilps28qsw`
================================================================================

CircuitPython module for the ILPS28QSW absolute digital output barometer.

This is a pure-Python porting of:

* `ST's C driver
  <https://github.com/STMicroelectronics/ilps28qsw-pid>`_
* `ST's C examples
  <https://github.com/STMicroelectronics/STMems_Standard_C_drivers/tree/master/ilps28qsw_STdC/examples>`_


* Author(s): mrv96

Implementation Notes
--------------------

**Hardware:**

* STMicroelectronics `ILPS28QSW absolute digital output barometer
  <https://www.st.com/en/mems-and-sensors/ilps28qsw.html>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

# imports

__version__ = "0.2.0"
__repo__ = "https://github.com/mrv96/CircuitPython_ILPS28QSW.git"


from ctypes import Structure, c_float, c_int16, c_int32, c_uint8, c_uint16, sizeof
from enum import IntEnum

from adafruit_bus_device.i2c_device import I2CDevice
from busio import I2C
from micropython import const

DRV_BYTE_ORDER = "little"

if DRV_BYTE_ORDER == "little":
    from ctypes import LittleEndianStructure as EndianStructure
else:
    from ctypes import BigEndianStructure as EndianStructure


# TODO: to be ported?
# typedef struct
# {
# #if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
#   uint8_t bit0       : 1;
#   uint8_t bit1       : 1;
#   uint8_t bit2       : 1;
#   uint8_t bit3       : 1;
#   uint8_t bit4       : 1;
#   uint8_t bit5       : 1;
#   uint8_t bit6       : 1;
#   uint8_t bit7       : 1;
# #elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
#   uint8_t bit7       : 1;
#   uint8_t bit6       : 1;
#   uint8_t bit5       : 1;
#   uint8_t bit4       : 1;
#   uint8_t bit3       : 1;
#   uint8_t bit2       : 1;
#   uint8_t bit1       : 1;
#   uint8_t bit0       : 1;
# #endif /* DRV_BYTE_ORDER */
# } bitwise_t;


_PROPERTY_DISABLE = 0
_PROPERTY_ENABLE = 1


# TODO: to be ported?
# typedef int32_t (*stmdev_write_ptr)(void *, uint8_t, const uint8_t *, uint16_t);
# typedef int32_t (*stmdev_read_ptr)(void *, uint8_t, uint8_t *, uint16_t);
# typedef void (*stmdev_mdelay_ptr)(uint32_t millisec);

# typedef struct
# {
#   /** Component mandatory fields **/
#   stmdev_write_ptr  write_reg;
#   stmdev_read_ptr   read_reg;
#   /** Component optional fields **/
#   stmdev_mdelay_ptr   mdelay;
#   /** Customizable optional pointer **/
#   void *handle;
# } stmdev_ctx_t;

# /** @defgroup    Generic address-data structure definition
#   * @brief       This structure is useful to load a predefined configuration
#   *              of a sensor.
#   *              You can create a sensor configuration by your own or using
#   *              Unico / Unicleo tools available on STMicroelectronics
#   *              web site.
#   *
#   * @{
#   *
#   */

# typedef struct
# {
#   uint8_t address;
#   uint8_t data;
# } ucf_line_t;


I2C_ADD = const(0x5C)  # I2C Device Address 7 bit format
ID = const(0xB4)  # Device Identification (Who am I)


INTERRUPT_CFG = const(0x0B)


class InterruptCfg(EndianStructure):
    _fields_ = [
        ("phe", c_uint8, 1),
        ("ple", c_uint8, 1),
        ("lir", c_uint8, 1),
        ("not_used_01", c_uint8, 1),
        ("reset_az", c_uint8, 1),
        ("autozero", c_uint8, 1),
        ("reset_arp", c_uint8, 1),
        ("autorefp", c_uint8, 1),
    ]


THS_P_L = const(0x0C)


# TODO: this may be a normal class
class ThsPL(Structure):
    _fields_ = [
        ("ths", c_uint8, 8),
    ]


THS_P_H = const(0x0D)


class ThsPH(EndianStructure):
    _fields_ = [
        ("ths", c_uint8, 7),
        ("not_used_01", c_uint8, 1),
    ]


IF_CTRL = const(0x0E)


class IfCtrl(EndianStructure):
    _fields_ = [
        ("not_used_01", c_uint8, 4),
        ("sda_pu_en", c_uint8, 1),
        ("not_used_02", c_uint8, 3),
    ]


WHO_AM_I = const(0x0F)
CTRL_REG1 = const(0x10)


class CtrlReg1(EndianStructure):
    _fields_ = [
        ("avg", c_uint8, 3),
        ("odr", c_uint8, 4),
        ("not_used_01", c_uint8, 1),
    ]


CTRL_REG2 = const(0x11)


class CtrlReg2(EndianStructure):
    _fields_ = [
        ("oneshot", c_uint8, 1),
        ("not_used_01", c_uint8, 1),
        ("swreset", c_uint8, 1),
        ("bdu", c_uint8, 1),
        ("en_lpfp", c_uint8, 1),
        ("lfpf_cfg", c_uint8, 1),
        ("fs_mode", c_uint8, 1),
        ("boot", c_uint8, 1),
    ]


CTRL_REG3 = const(0x12)


class CtrlReg3(EndianStructure):
    _fields_ = [
        ("if_add_inc", c_uint8, 1),
        ("not_used_01", c_uint8, 4),
        ("ah_qvar_p_auto_en", c_uint8, 1),
        ("not_used_02", c_uint8, 1),
        ("ah_qvar_en", c_uint8, 1),
    ]


FIFO_CTRL = const(0x14)


class FifoCtrl(EndianStructure):
    _fields_ = [
        ("f_mode", c_uint8, 2),
        ("trig_modes", c_uint8, 1),
        ("stop_on_wtm", c_uint8, 1),
        ("ah_qvar_p_fifo_en", c_uint8, 1),
        ("not_used_01", c_uint8, 3),
    ]


FIFO_WTM = const(0x15)


class FifoWtm(EndianStructure):
    _fields_ = [
        ("wtm", c_uint8, 7),
        ("not_used_01", c_uint8, 1),
    ]


REF_P_L = const(0x16)
# TODO: to be ported?
# typedef struct
# {
#   uint8_t refp             : 8;
# } ilps28qsw_ref_p_l_t;

# #define ILPS28QSW_REF_P_H                 0x17U
# typedef struct
# {
#   uint8_t refp             : 8;
# } ilps28qsw_ref_p_h_t;


I3C_IF_CTRL = const(0x19)


class I3CIfCtrl(EndianStructure):
    _fields_ = [
        ("I3C_Bus_Avb_Sel", c_uint8, 2),
        ("not_used_02", c_uint8, 3),
        ("asf_on", c_uint8, 1),
        ("not_used_01", c_uint8, 2),
    ]


RPDS_L = const(0x1A)
RPDS_H = const(0x1B)
INT_SOURCE = const(0x24)


class IntSource(EndianStructure):
    _fields_ = [
        ("ph", c_uint8, 1),
        ("pl", c_uint8, 1),
        ("ia", c_uint8, 1),
        ("not_used_01", c_uint8, 4),
        ("boot_on", c_uint8, 1),
    ]


FIFO_STATUS1 = const(0x25)


# TODO: this may be a normal class
class FifoStatus1(Structure):
    _fields_ = [
        ("fss", c_uint8, 8),
    ]


FIFO_STATUS2 = const(0x26)


class FifoStatus2(EndianStructure):
    _fields_ = [
        ("not_used_01", c_uint8, 5),
        ("fifo_full_ia", c_uint8, 1),
        ("fifo_ovr_ia", c_uint8, 1),
        ("fifo_wtm_ia", c_uint8, 1),
    ]


STATUS = const(0x27)


class Status(EndianStructure):
    _fields_ = [
        ("p_da", c_uint8, 1),
        ("t_da", c_uint8, 1),
        ("not_used_01", c_uint8, 2),
        ("p_or", c_uint8, 1),
        ("t_or", c_uint8, 1),
        ("not_used_02", c_uint8, 2),
    ]


PRESS_OUT_XL = const(0x28)
PRESS_OUT_L = const(0x29)
PRESS_OUT_H = const(0x2A)
TEMP_OUT_L = const(0x2B)
TEMP_OUT_H = const(0x2C)

FIFO_DATA_OUT_PRESS_XL = const(0x78)
FIFO_DATA_OUT_PRESS_L = const(0x79)
FIFO_DATA_OUT_PRESS_H = const(0x7A)


# TODO: to be ported?
# /**
#   * @defgroup ILPS28QSW_Register_Union
#   * @brief    This union group all the registers that has a bitfield
#   *           description.
#   *           This union is useful but not need by the driver.
#   *
#   *           REMOVING this union you are compliant with:
#   *           MISRA-C 2012 [Rule 19.2] -> " Union are not allowed "
#   *
#   * @{
#   *
#   */

# typedef union
# {
#   ilps28qsw_interrupt_cfg_t    interrupt_cfg;
#   ilps28qsw_ths_p_l_t          ths_p_l;
#   ilps28qsw_ths_p_h_t          ths_p_h;
#   ilps28qsw_if_ctrl_t          if_ctrl;
#   ilps28qsw_ctrl_reg1_t        ctrl_reg1;
#   ilps28qsw_ctrl_reg2_t        ctrl_reg2;
#   ilps28qsw_ctrl_reg3_t        ctrl_reg3;
#   ilps28qsw_fifo_ctrl_t        fifo_ctrl;
#   ilps28qsw_fifo_wtm_t         fifo_wtm;
#   ilps28qsw_ref_p_l_t          ref_p_l;
#   ilps28qsw_ref_p_h_t          ref_p_h;
#   ilps28qsw_i3c_if_ctrl_t      i3c_if_ctrl;
#   ilps28qsw_int_source_t       int_source;
#   ilps28qsw_fifo_status1_t     fifo_status1;
#   ilps28qsw_fifo_status2_t     fifo_status2;
#   ilps28qsw_status_t           status;
#   bitwise_t                  bitwise;
#   uint8_t                    byte;
# } ilps28qsw_reg_t;
# TODO: this may be a normal class


class ID(Structure):
    _fields_ = [
        ("whoami", c_uint8),
    ]


class Filter(IntEnum):
    AUTO = 0x00  # anti-spike filters managed by protocol
    ALWAYS_ON = 0x01  # anti-spike filters always on


class BusAvbTime(IntEnum):
    BUS_AVB_TIME_50us = 0x00  # bus available time equal to 50 us
    BUS_AVB_TIME_2us = 0x01  # bus available time equal to 2 us
    BUS_AVB_TIME_1ms = 0x02  # bus available time equal to 1 ms
    BUS_AVB_TIME_25ms = 0x03  # bus available time equal to 25 ms


# TODO: this may be a normal class
class BusMode(Structure):
    _fields_ = [
        ("filter", c_uint8),
        ("bus_avb_time", c_uint8),
    ]


class Init(IntEnum):
    DRV_RDY = 0x00  # Initialize the device for driver usage
    BOOT = 0x01  # Restore calib. param. ( it takes 10ms )
    RESET = 0x02  # Reset configuration registers


class Stat(Structure):
    _fields_ = [
        ("sw_reset", c_uint8, 1),  # Restoring configuration registers.
        ("boot", c_uint8, 1),  # Restoring calibration parameters.
        ("drdy_pres", c_uint8, 1),  # Pressure data ready.
        ("drdy_temp", c_uint8, 1),  # Temperature data ready.
        ("ovr_pres", c_uint8, 1),  # Pressure data overrun.
        ("ovr_temp", c_uint8, 1),  # Temperature data overrun.
        ("end_meas", c_uint8, 1),  # Single measurement is finished.
        ("ref_done", c_uint8, 1),  # Auto-Zero value is set.
    ]


# TODO: this may be a normal class
class PinConf(Structure):
    _fields_ = [
        ("sda_pull_up", c_uint8, 1),  # 1 = pull-up always disabled
    ]


# TODO: this may be a normal class
class AllSources(Structure):
    _fields_ = [
        ("drdy_pres", c_uint8, 1),  # Pressure data ready
        ("drdy_temp", c_uint8, 1),  # Temperature data ready
        ("over_pres", c_uint8, 1),  # Over pressure event
        ("under_pres", c_uint8, 1),  # Under pressure event
        ("thrsld_pres", c_uint8, 1),  # Over/Under pressure event
        ("fifo_full", c_uint8, 1),  # FIFO full
        ("fifo_ovr", c_uint8, 1),  # FIFO overrun
        ("fifo_th", c_uint8, 1),  # FIFO threshold reached
    ]


class Fs(IntEnum):
    ILPS28QSW_1260hPa = (0x00,)
    ILPS28QSW_4060hPa = (0x01,)


class Odr(IntEnum):
    ILPS28QSW_ONE_SHOT = (0x00,)  # Device in power down till software trigger
    ILPS28QSW_1Hz = (0x01,)
    ILPS28QSW_4Hz = (0x02,)
    ILPS28QSW_10Hz = (0x03,)
    ILPS28QSW_25Hz = (0x04,)
    ILPS28QSW_50Hz = (0x05,)
    ILPS28QSW_75Hz = (0x06,)
    ILPS28QSW_100Hz = (0x07,)
    ILPS28QSW_200Hz = (0x08,)


class Avg(IntEnum):
    ILPS28QSW_4_AVG = (0,)
    ILPS28QSW_8_AVG = (1,)
    ILPS28QSW_16_AVG = (2,)
    ILPS28QSW_32_AVG = (3,)
    ILPS28QSW_64_AVG = (4,)
    ILPS28QSW_128_AVG = (5,)
    ILPS28QSW_256_AVG = (6,)
    ILPS28QSW_512_AVG = (7,)


class Lpf(IntEnum):
    LPF_DISABLE = (0,)
    LPF_ODR_DIV_4 = (1,)
    LPF_ODR_DIV_9 = (3,)


# TODO: this may be a normal class
class Md(Structure):
    _fields_ = [
        ("fs", c_uint8),
        ("odr", c_uint8),
        ("avg", c_uint8),
        ("lpf", c_uint8),
        ("interleaved_mode", c_uint8),
    ]


# TODO: this may be a normal class
class _Pressure(Structure):
    _fields_ = [
        ("hpa", c_float),
        ("raw", c_int32),  # 32 bit signed-left algned  format left
    ]


# TODO: this may be a normal class
class _Heat(Structure):
    _fields_ = [
        ("deg_c", c_float),
        ("raw", c_int16),
    ]


# TODO: this may be a normal class
class _AhQvar(Structure):
    _fields_ = [
        ("lsb", c_int32),  # 24 bit properly right aligned
    ]


# TODO: this may be a normal class
class Data(Structure):
    _fields_ = [
        ("pressure", _Pressure),
        ("heat", _Heat),
        ("ah_qvar", _AhQvar),
    ]


# TODO: this may be a normal class
class AhQvarData(Structure):
    _fields_ = [
        ("mv", c_float),  # value converted in mV
        ("lsb", c_int32),  # 24 bit properly right aligned
        ("raw", c_int32),  # 32 bit signed-left algned  format left
    ]


class Operation(IntEnum):
    BYPASS = (0,)
    FIFO = (1,)
    STREAM = (2,)
    STREAM_TO_FIFO = (7,)  # Dynamic-Stream, FIFO on Trigger
    BYPASS_TO_STREAM = (6,)  # Bypass, Dynamic-Stream on Trigger
    BYPASS_TO_FIFO = (5,)  # Bypass, FIFO on Trigger


# TODO: this may be a normal class
class FifoMd(Structure):
    _fields_ = [
        ("operation", c_uint8),
        ("watermark", c_uint8, 7),  # (0 disable) max 128.
    ]


# TODO: this may be a normal class
class FifoData(Structure):
    _fields_ = [
        ("hpa", c_float),
        ("lsb", c_int32),  # 24 bit properly right aligned
        ("raw", c_int32),
    ]


# TODO: this may be a normal class
class IntMode(Structure):
    _fields_ = [
        ("int_latched", c_uint8, 1),
    ]


class IntThMd(Structure):
    _fields_ = [
        ("threshold", c_uint16),  # Threshold in hPa * 16 (@1260hPa)
        # Threshold in hPa * 8  (@4060hPa)
        ("over_th", c_uint8, 1),  # Pressure data over threshold event
        ("under_th", c_uint8, 1),  # Pressure data under threshold event
    ]


class ApplyRef(IntEnum):
    OUT_AND_INTERRUPT = 0
    ONLY_INTERRUPT = 1
    RST_REFS = 2


class RefMd(Structure):
    _fields_ = [
        ("apply_ref", c_uint8),
        ("get_ref", c_uint8, 1),  # Use current pressure value as reference
    ]


class ILPS28QSW:
    def __init__(self, i2c: I2C, address: int = I2C_ADD, probe: bool=True) -> None:
        self.device = I2CDevice(i2c, address, probe)

    def _read_reg(self, reg: int, data: bytearray) -> None:
        """
        Read a generic device register.

        Args:
            reg (int): Register to read.
            data: Buffer that stores the data read.
        """
        with self.device as i2c:
            i2c.write_then_readinto(reg.to_bytes(1, 'big'), data)

    def _write_reg(self, reg: int, data: bytes) -> None:
        """
        Write a generic device register.

        Args:
            reg (int): Register to write.
            data: Data to write into the register.
        """
        with self.device as i2c:
            i2c.write(reg.to_bytes(1, 'big') + data)

    @staticmethod
    def from_fs1260_to_hPa(lsb: int) -> float:
        return lsb / 1048576.0  # 4096.0f * 256

    @staticmethod
    def from_fs4060_to_hPa(lsb: int) -> float:
        return lsb / 524288.0  # 2048.0 * 256

    @staticmethod
    def from_lsb_to_celsius(lsb: int) -> float:
        return lsb / 100.0

    @staticmethod
    def from_lsb_to_mv(lsb: int) -> float:
        return lsb / 426000.0

    def get_id(self) -> ID:
        """
        Get device "Who am I" information.

        Returns:
            ID: Read ID.
        """
        reg = bytearray(1)
        val = ID.from_buffer(reg)
        self._read_reg(WHO_AM_I, reg)
        return val

    def set_bus_mode(self, val: BusMode) -> None:
        """
        Configure the bus operating mode.

        Args:
            val: Bus operating mode configuration.
        """
        i3c_if_ctrl_buf = bytearray(sizeof(I3CIfCtrl))
        i3c_if_ctrl = I3CIfCtrl.from_buffer(i3c_if_ctrl_buf)
        self._read_reg(I3C_IF_CTRL, i3c_if_ctrl_buf)

        i3c_if_ctrl.asf_on = val.filter & 0x01
        i3c_if_ctrl.I3C_Bus_Avb_Sel = val.bus_avb_time & 0x03
        self._write_reg(I3C_IF_CTRL, i3c_if_ctrl)

    def get_bus_mode(self) -> BusMode:
        """
        Get the current bus operating mode.

        Returns:
            BusMode: Configuration for the bus operating mode.
        """
        i3c_if_ctrl_buf = bytearray(sizeof(I3CIfCtrl))
        i3c_if_ctrl = I3CIfCtrl.from_buffer(i3c_if_ctrl_buf)
        self._read_reg(I3C_IF_CTRL, i3c_if_ctrl_buf)
        val = BusMode()

        try:
            val.filter = Filter(i3c_if_ctrl.asf_on)
        except ValueError:
            val.filter = Filter.AUTO

        try:
            val.bus_avb_time = BusAvbTime(i3c_if_ctrl.I3C_Bus_Avb_Sel)
        except ValueError:
            val.bus_avb_time = BusAvbTime.BUS_AVB_TIME_50us

        return val

    def set_init(self, val: Init) -> None:
        reg = bytearray(2)
        ctrl_reg2 = CtrlReg2.from_buffer(reg)
        ctrl_reg3 = CtrlReg3.from_buffer(reg, 1)

        self._read_reg(CTRL_REG2, reg)

        if val == Init.BOOT:
            ctrl_reg2.boot = _PROPERTY_ENABLE
            self._write_reg(CTRL_REG2, ctrl_reg2)
        elif val == Init.RESET:
            ctrl_reg2.swreset = _PROPERTY_ENABLE
            self._write_reg(CTRL_REG2, ctrl_reg2)
        elif val == Init.DRV_RDY:
            ctrl_reg2.bdu = _PROPERTY_ENABLE
            ctrl_reg3.if_add_inc = _PROPERTY_ENABLE
            self._write_reg(CTRL_REG2, reg)
        else:
            ctrl_reg2.swreset = _PROPERTY_ENABLE
            self._write_reg(CTRL_REG2, ctrl_reg2)

    def get_status(self) -> Status:
        """
        Get the status of the device.

        Returns:
            Stat: Read value.
        """
        interrupt_cfg_buf = bytearray(sizeof(InterruptCfg))
        int_source_buf = bytearray(sizeof(IntSource))
        ctrl_reg2_buf = bytearray(sizeof(CtrlReg2))
        status_buf = bytearray(sizeof(Status))
        interrupt_cfg = InterruptCfg.from_buffer(interrupt_cfg_buf)
        int_source = IntSource.from_buffer(int_source_buf)
        ctrl_reg2 = CtrlReg2.from_buffer(ctrl_reg2_buf)
        status = Status.from_buffer(status_buf)

        self._read_reg(CTRL_REG2, ctrl_reg2_buf)
        self._read_reg(INT_SOURCE, int_source_buf)
        self._read_reg(STATUS, status_buf)
        self._read_reg(INTERRUPT_CFG, interrupt_cfg_buf)

        return Stat(
            sw_reset=ctrl_reg2.swreset,
            boot=int_source.boot_on,
            drdy_pres=status.p_da,
            drdy_temp=status.t_da,
            ovr_pres=status.p_or,
            ovr_temp=status.t_or,
            end_meas=~ctrl_reg2.oneshot,
            ref_done=~interrupt_cfg.autozero,
        )

    def set_pin_conf(self, val: PinConf) -> None:
        """
        Set the electrical pin configuration.

        Args:
            val: settings for the configurable pins.
        """
        if_ctrl_buf = bytearray(sizeof(IfCtrl))
        if_ctrl = IfCtrl.from_buffer(if_ctrl_buf)

        self._read_reg(IF_CTRL, if_ctrl_buf)

        if_ctrl.sda_pu_en = val.sda_pull_up
        self._write_reg(IF_CTRL, if_ctrl)

    def get_pin_conf(self) -> PinConf:
        """
        Get the electrical pin configuration.

        Returns:
            PinConf: Read electrical settings for the configurable pins.
        """
        if_ctrl_buf = bytearray(sizeof(IfCtrl))
        if_ctrl = IfCtrl.from_buffer(if_ctrl_buf)

        self._read_reg(IF_CTRL, if_ctrl_buf)

        return PinConf(
            sda_pull_up=if_ctrl.sda_pu_en,
        )

    def get_all_sources(self) -> AllSources:
        """
        Get the status of all the interrupt sources.

        Returns:
            AllSources: Read status of all the interrupt sources.
        """
        fifo_status2_buf = bytearray(sizeof(FifoStatus2))
        int_source_buf = bytearray(sizeof(IntSource))
        status_buf = bytearray(sizeof(Status))
        fifo_status2 = FifoStatus2.from_buffer(fifo_status2_buf)
        int_source = IntSource.from_buffer(int_source_buf)
        status = Status.from_buffer(status_buf)

        self._read_reg(STATUS, status_buf)
        self._read_reg(INT_SOURCE, int_source_buf)
        self._read_reg(FIFO_STATUS2, fifo_status2_buf)

        return AllSources(
            drdy_pres=status.p_da,
            drdy_temp=status.t_da,
            over_pres=int_source.ph,
            under_pres=int_source.pl,
            thrsld_pres=int_source.ia,
            fifo_full=fifo_status2.fifo_full_ia,
            fifo_ovr=fifo_status2.fifo_ovr_ia,
            fifo_th=fifo_status2.fifo_wtm_ia,
        )

    def set_mode(self, val: Md) -> None:
        """
        Set the sensor conversion parameters.

        Args:
            val: Conversion parameters to set.
        """
        reg = bytearray(3)
        ctrl_reg1 = CtrlReg1.from_buffer(reg)
        ctrl_reg2 = CtrlReg2.from_buffer(reg, 1)
        ctrl_reg3 = CtrlReg3.from_buffer(reg, 2)
        fifo_ctrl_buf = bytearray(sizeof(FifoCtrl))
        fifo_ctrl = FifoCtrl.from_buffer(fifo_ctrl_buf)
        odr_save = 0
        ah_qvar_en_save = 0

        self._read_reg(CTRL_REG1, reg)

        # handle interleaved mode setting
        if ctrl_reg1.odr != 0x0:
            # power-down
            odr_save = ctrl_reg1.odr
            ctrl_reg1.odr = 0x0
            self._write_reg(CTRL_REG1, ctrl_reg1)

        if ctrl_reg3.ah_qvar_en != 0:
            # disable QVAR
            ah_qvar_en_save = ctrl_reg3.ah_qvar_en
            ctrl_reg3.ah_qvar_en = 0
            self._write_reg(CTRL_REG3, ctrl_reg3)

        # set interleaved mode (0 or 1)
        ctrl_reg3.ah_qvar_p_auto_en = val.interleaved_mode
        self._write_reg(CTRL_REG3, ctrl_reg3)

        # set FIFO interleaved mode (0 or 1)
        self._read_reg(FIFO_CTRL, fifo_ctrl_buf)
        fifo_ctrl.ah_qvar_p_fifo_en = val.interleaved_mode
        self._write_reg(FIFO_CTRL, fifo_ctrl)

        if ah_qvar_en_save != 0:
            # restore ah_qvar_en back to previous setting
            ctrl_reg3.ah_qvar_en = ah_qvar_en_save

        if odr_save != 0:
            # restore odr back to previous setting
            ctrl_reg1.odr = odr_save

        ctrl_reg1.odr = val.odr
        ctrl_reg1.avg = val.avg
        ctrl_reg2.en_lpfp = val.lpf & 0x01
        ctrl_reg2.lfpf_cfg = (val.lpf & 0x02) >> 1
        ctrl_reg2.fs_mode = val.fs

        self._write_reg(CTRL_REG1, reg)

    def get_mode(self) -> Md:
        """
        Get the sensor conversion parameters.

        Returns:
            Md: Read sensor conversion parameters.
        """
        reg = bytearray(3)
        ctrl_reg1 = CtrlReg1.from_buffer(reg)
        ctrl_reg2 = CtrlReg2.from_buffer(reg, 1)
        ctrl_reg3 = CtrlReg3.from_buffer(reg, 2)
        val = Md()

        self._read_reg(CTRL_REG1, reg)

        try:
            val.fs = Fs(ctrl_reg2.fs_mode)
        except ValueError:
            val.fs = Fs.ILPS28QSW_1260hPa

        try:
            val.odr = Odr(ctrl_reg1.odr)
        except ValueError:
            val.odr = Odr.ILPS28QSW_ONE_SHOT

        try:
            val.avg = Avg(ctrl_reg1.avg)
        except ValueError:
            val.avg = Avg.ILPS28QSW_4_AVG

        try:
            val.lpf = Lpf((ctrl_reg2.lfpf_cfg << 2) | ctrl_reg2.en_lpfp)
        except ValueError:
            val.lpf = Lpf.LPF_DISABLE

        val.interleaved_mode = ctrl_reg3.ah_qvar_p_auto_en
        return val

    def trigger_sw(self, md: Md) -> None:
        """
        Ssoftware trigger for One-Shot.

        Args:
            ctx: Communication interface handler (pointer).
            md: Sensor conversion parameters.
        """
        ctrl_reg2_buf = bytearray(sizeof(CtrlReg2))
        ctrl_reg2 = CtrlReg2.from_buffer(ctrl_reg2_buf)

        if md.odr == Odr.ILPS28QSW_ONE_SHOT:
            self._read_reg(CTRL_REG2, ctrl_reg2_buf)
            ctrl_reg2.oneshot = _PROPERTY_ENABLE
            self._write_reg(CTRL_REG2, ctrl_reg2)

    def set_ah_qvar_en(self, val: int) -> None:
        """
        Enable or disable the AH/QVAR function.

        Args:
            val: Value to set for `ah_qvar_en` in register `CTRL_REG3`.

        Returns:
            int: Interface status (MANDATORY: return 0 -> no Error).
        """
        ctrl_reg3_buf = bytearray(sizeof(CtrlReg3))
        ctrl_reg3 = CtrlReg3.from_buffer(ctrl_reg3_buf)
        self._read_reg(CTRL_REG3, ctrl_reg3_buf)
        ctrl_reg3.ah_qvar_en = val
        self._write_reg(CTRL_REG3, ctrl_reg3)

    def get_ah_qvar_en(self) -> int:
        """
        Get the status of the AH/QVAR function enable setting.

        Returns:
            uint8: Read value of `ah_qvar_en` from register `CTRL_REG3`.
        """
        ctrl_reg3_buf = bytearray(sizeof(CtrlReg3))
        ctrl_reg3 = CtrlReg3.from_buffer(ctrl_reg3_buf)
        self._read_reg(CTRL_REG3, ctrl_reg3_buf)
        return ctrl_reg3.ah_qvar_en

    def get_data(self, md: Md) -> Data:
        """
        Retrieve sensor data.

        Returns:
            Data: Data retrieved from the sensor.
        """
        buff = bytearray(5)
        data = Data()

        self._read_reg(PRESS_OUT_XL, buff)

        # pressure conversion
        data.pressure.raw = int.from_bytes(buff, byteorder="little", signed=True) << 8

        if md.interleaved_mode == 1:
            if (buff[0] & 0x1) == 0:
                # data is a pressure sample
                if md.fs == Fs.ILPS28QSW_1260hPa:
                    data.pressure.hpa = self.from_fs1260_to_hPa(data.pressure.raw)
                elif md.fs == Fs.ILPS28QSW_4060hPa:
                    data.pressure.hpa = self.from_fs4060_to_hPa(data.pressure.raw)
                else:
                    data.pressure.hpa = 0
                data.ah_qvar.lsb = 0
            else:
                # data is a AH_QVAR sample
                data.ah_qvar.lsb = data.pressure.raw >> 8
                data.pressure.hpa = 0
        else:
            if md.fs == Fs.ILPS28QSW_1260hPa:
                data.pressure.hpa = self.from_fs1260_to_hPa(data.pressure.raw)
            elif md.fs == Fs.ILPS28QSW_4060hPa:
                data.pressure.hpa = self.from_fs4060_to_hPa(data.pressure.raw)
            else:
                data.pressure.hpa = 0
            data.ah_qvar.lsb = 0

        # temperature conversion
        data.heat.raw = buff[4]
        data.heat.raw = (data.heat.raw << 8) + buff[3]
        data.heat.deg_c = self.from_lsb_to_celsius(data.heat.raw)

        return data

    def get_pressure_raw(self) -> int:
        """
        Get the pressure output value.

        Returns:
            uint32: Read data.
        """
        reg = bytearray(3)
        self._read_reg(PRESS_OUT_XL, reg)
        return int.from_bytes(reg, byteorder="little", signed=False) << 8

    def get_temperature_raw(self) -> int:
        """
        Get the temperature output value.

        Returns:
            int16: Read data.
        """
        reg = bytearray(2)
        self._read_reg(TEMP_OUT_L, reg)
        return int.from_bytes(reg, byteorder="little", signed=True)

    def get_ah_qvar_data(self) -> AhQvarData:
        """
        Read AH/QVAR data from the sensor.

        Returns:
            AhQvarData: Data retrieved from the sensor.
        """
        buff = bytearray(3)
        data = AhQvarData()

        self._read_reg(PRESS_OUT_XL, buff)

        # QVAR conversion
        data.raw = int.from_bytes(buff, byteorder="little", signed=True) << 8
        data.lsb = data.raw >> 8

        data.mv = self.from_lsb_to_mv(data.lsb)

        return data

    def set_fifo_mode(self, val: FifoMd):
        """
        Set the FIFO operation mode.

        Args:
            val: FIFO operation mode to set.
        """
        reg = bytearray(2)
        fifo_ctrl = FifoCtrl.from_buffer(reg)
        fifo_wtm = FifoWtm.from_buffer(reg, 1)

        self._read_reg(FIFO_CTRL, reg)

        fifo_ctrl.f_mode = val.operation & 0x03
        fifo_ctrl.trig_modes = (val.operation & 0x04) >> 2

        if val.watermark != 0x00:
            fifo_ctrl.stop_on_wtm = _PROPERTY_ENABLE
        else:
            fifo_ctrl.stop_on_wtm = _PROPERTY_DISABLE

        fifo_wtm.wtm = val.watermark

        self._write_reg(FIFO_CTRL, reg)

    def get_fifo_mode(self) -> FifoMd:
        """
        Get the FIFO operation mode.

        Returns:
            FifoMd: Read FIFO operation mode.
        """
        reg = bytearray(2)
        fifo_ctrl = FifoCtrl.from_buffer(reg)
        fifo_wtm = FifoWtm.from_buffer(reg, 1)
        val = FifoMd()

        self._read_reg(FIFO_CTRL, reg)

        tmp = (fifo_ctrl.trig_modes << 2) | fifo_ctrl.f_mode
        if tmp == Operation.BYPASS:
            val.operation = Operation.BYPASS
        if tmp == Operation.FIFO:
            val.operation = Operation.FIFO
        if tmp == Operation.STREAM:
            val.operation = Operation.STREAM
        if tmp == Operation.STREAM_TO_FIFO:
            val.operation = Operation.STREAM_TO_FIFO
        if tmp == Operation.BYPASS_TO_STREAM:
            val.operation = Operation.BYPASS_TO_STREAM
        if tmp == Operation.BYPASS_TO_FIFO:
            val.operation = Operation.BYPASS_TO_FIFO
        else:
            val.operation = Operation.BYPASS
        val.watermark = fifo_wtm.wtm

        return val

    def get_fifo_level(self) -> int:
        """
        Get the number of samples stored in FIFO.

        Returns:
            uint8: Read number of samples stored in FIFO.
        """
        fifo_status1_buf = bytearray(sizeof(FifoStatus1))
        fifo_status1 = FifoStatus1.from_buffer(fifo_status1_buf)
        self._read_reg(FIFO_STATUS1, fifo_status1_buf)
        return fifo_status1.fss

    def get_fifo_data(self, samp: int, md: Md) -> FifoData:
        """
        Get the software trigger for One-Shot mode.

        Args:
            samp: Number of samples stored in FIFO.
            md: Sensor conversion parameter.

        Returns:
            FifoData: Data retrieved from FIFO.
        """
        fifo_data = bytearray(3)
        md = Md()
        data = (FifoData * samp)()

        for i in range(samp):
            self._read_reg(FIFO_DATA_OUT_PRESS_XL, fifo_data)
            data[i].raw = int.from_bytes(fifo_data, byteorder="little", signed=True) << 8

        for i in range(samp):
            self._read_reg(FIFO_DATA_OUT_PRESS_XL, fifo_data)
            data[i].raw = int.from_bytes(fifo_data, byteorder="little", signed=True) << 8

            if md.interleaved_mode == 1:
                if (fifo_data[0] & 1) == 0:
                    # data is a pressure sample
                    if md.fs == Fs.ILPS28QSW_1260hPa:
                        data[i].hpa = self.from_fs1260_to_hPa(data[i].raw)
                    elif md.fs == Fs.ILPS28QSW_4060hPa:
                        data[i].hpa = self.from_fs4060_to_hPa(data[i].raw)
                    else:
                        data[i].hpa = 0
                    data[i].lsb = 0
                else:
                    # data is a AH_QVAR sample
                    data[i].lsb = data[i].raw << 8
                    data[i].hpa = 0
            else:
                if md.fs == Fs.ILPS28QSW_1260hPa:
                    data[i].hpa = self.from_fs1260_to_hPa(data[i].raw)
                elif md.fs == Fs.ILPS28QSW_4060hPa:
                    data[i].hpa = self.from_fs4060_to_hPa(data[i].raw)
                else:
                    data[i].hpa = 0
                data[i].lsb = 0

    def set_interrupt_mode(self, val: IntMode) -> None:
        """
        Set the interrupt pins hardware signal configuration.

        Args:
            ctx: Communication interface handler (pointer).
            val: Interrupt pins hardware signal settings.
        """
        interrupt_cfg_buf = bytearray(sizeof(InterruptCfg))
        interrupt_cfg = InterruptCfg.from_buffer(interrupt_cfg_buf)

        self._read_reg(INTERRUPT_CFG, interrupt_cfg_buf)
        interrupt_cfg.lir = val.int_latched
        self._write_reg(INTERRUPT_CFG, interrupt_cfg)

    def get_interrupt_mode(self) -> IntMode:
        """
        Get the interrupt pins hardware signal configuration.

        Returns:
            IntMode: Read interrupt pins hardware signal settings.
        """
        interrupt_cfg_buf = bytearray(sizeof(InterruptCfg))
        interrupt_cfg = InterruptCfg.from_buffer(interrupt_cfg_buf)
        self._read_reg(INTERRUPT_CFG, interrupt_cfg_buf)
        return IntMode(
            int_latched=interrupt_cfg.lir,
        )

    def set_int_on_threshold_mode(self, val: IntThMd) -> None:
        """
        Set the Wake-up and Wake-up to Sleep configuration.

        Args:
            val: Configuration parameters.
        """
        reg = bytearray(3)
        interrupt_cfg = InterruptCfg.from_buffer(reg)
        ths_p_l = ThsPL.from_buffer(reg, 1)
        ths_p_h = ThsPH.from_buffer(reg, 2)
        self._read_reg(INTERRUPT_CFG, reg)

        interrupt_cfg.phe = val.over_th
        interrupt_cfg.ple = val.under_th
        ths_p_h.ths = val.threshold >> 8
        ths_p_l.ths = val.threshold - (ths_p_h.ths << 8)

        self._write_reg(INTERRUPT_CFG, reg)

    def get_int_on_threshold_mode(self) -> IntThMd:
        """
        Get the Wake-up and Wake-up to Sleep configuration.

        Returns:
            IntThMd: Read configuration parameters.
        """
        reg = bytearray(3)
        interrupt_cfg = InterruptCfg.from_buffer(reg)
        ths_p_l = ThsPL.from_buffer(reg, 1)
        ths_p_h = ThsPH.from_buffer(reg, 2)
        val = IntThMd()

        self._read_reg(INTERRUPT_CFG, reg)

        val.over_th = interrupt_cfg.phe
        val.under_th = interrupt_cfg.ple
        val.threshold = (ths_p_h.ths << 8) | ths_p_l.ths
        return val

    def set_reference_mode(self, val: RefMd) -> None:
        """
        Configure Wake-up and Wake-up to Sleep.

        Args:
            val: Configuration parameters.
        """
        interrupt_cfg_buf = bytearray(sizeof(InterruptCfg))
        interrupt_cfg = InterruptCfg.from_buffer(interrupt_cfg_buf)

        self._read_reg(INTERRUPT_CFG, interrupt_cfg_buf)

        interrupt_cfg.autozero = val.get_ref
        interrupt_cfg.autorefp = val.apply_ref & 0x01

        interrupt_cfg.reset_az = (val.apply_ref & 0x02) >> 1
        interrupt_cfg.reset_arp = (val.apply_ref & 0x02) >> 1

        self._write_reg(INTERRUPT_CFG, interrupt_cfg)

    def get_reference_mode(self) -> RefMd:
        """
        Get the Wake-up and Wake-up to Sleep configuration.

        Returns:
            RefMd: Read configuration parameters.
        """
        interrupt_cfg_buf = bytearray(sizeof(InterruptCfg))
        interrupt_cfg = InterruptCfg.from_buffer(interrupt_cfg_buf)
        val = RefMd()

        self._read_reg(INTERRUPT_CFG, interrupt_cfg_buf)

        tmp = (interrupt_cfg.reset_az << 1) | interrupt_cfg.autorefp
        if tmp == ApplyRef.OUT_AND_INTERRUPT:
            val.apply_ref = ApplyRef.OUT_AND_INTERRUPT
        elif tmp == ApplyRef.ONLY_INTERRUPT:
            val.apply_ref = ApplyRef.ONLY_INTERRUPT
        else:
            val.apply_ref = ApplyRef.RST_REFS

        val.get_ref = interrupt_cfg.autozero

        return val

    def get_refp(self) -> int:
        """
        Get the reference pressure LSB data.

        Returns:
            int16: Read parameters of configuration.
        """
        reg = bytearray(2)
        self._read_reg(REF_P_L, reg)
        return int.from_bytes(reg, byteorder="little", signed=True)

    def set_opc(self, val: int) -> None:
        """
        Configure Wake-up and Wake-up to Sleep.

        Args:
            val: Configuration parameters.
        """
        reg = bytearray(val.to_bytes(2, byteorder="little", signed=True))
        self._write_reg(RPDS_L, reg)

    def get_opc(self) -> int:
        """
        Configure Wake-up and Wake-up to Sleep.

        Returns:
            int16: Read value.
        """
        reg = bytearray(2)
        self._read_reg(RPDS_L, reg)
        return int.from_bytes(reg, byteorder="little", signed=True)
