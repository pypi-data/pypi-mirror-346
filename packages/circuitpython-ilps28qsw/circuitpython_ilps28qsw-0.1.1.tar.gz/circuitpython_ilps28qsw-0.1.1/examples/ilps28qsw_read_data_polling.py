#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2025 mrv96
#
# SPDX-License-Identifier: Unlicense

# TESTED WITH FT232H
# import os
# os.environ['BLINKA_FT232H'] = '1'

import board

import ilps28qsw as ilps
from ilps28qsw import ILPS28QSW

if __name__ == "__main__":
    i2c = board.I2C()
    sensor = ILPS28QSW(i2c)

    # Device ID
    print("I am:", hex(sensor.get_id().whoami))

    # Restore default configuration
    sensor.set_init(ilps.Init.RESET)
    while sensor.get_status().sw_reset:
        pass

    # Disable AH/QVAR to save power consumption
    # Set bdu and if_inc recommended for driver usage
    sensor.set_init(ilps.Init.DRV_RDY)
    sensor.set_bus_mode(ilps.BusMode(filter=ilps.Filter.AUTO))

    # Select bus interface
    # Set Output Data Rate
    md = ilps.Md(
        odr=ilps.Odr.ILPS28QSW_4Hz,
        avg=ilps.Avg.ILPS28QSW_16_AVG,
        lpf=ilps.Lpf.LPF_ODR_DIV_4,
        fs=ilps.Fs.ILPS28QSW_1260hPa,
    )
    sensor.set_mode(md)

    # Read samples in polling mode (no int)
    for _ in range(10):
        all_sources = sensor.get_all_sources()
        if all_sources.drdy_pres | all_sources.drdy_temp:
            data = sensor.get_data(md)
            print(
                f"pressure [hPa]:{data.pressure.hpa:6.2f} temperature [degC]:{data.heat.deg_c:6.2f}"
            )

    i2c.deinit()
