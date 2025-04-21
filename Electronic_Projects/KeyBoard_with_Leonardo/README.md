# KeyBoard with Arduino Leonardo

This project aims to make a "keyboard" with Arduino Leonardo, this has the function of acting as a Rubber Duck. It contains two relatively simple codes, the first in extension (. ino) for Arduino IDE and the second in (. C) to use with PlatformIO or another compiler.


## Arduino Leonardo and HID Technology

The Arduino Leonardo stands out for its ATmega32u4 microcontroller, which features native USB communication. This capability allows it to emulate Human Interface Devices (HID) such as keyboards, mice, and joysticks. Unlike other Arduino boards that rely on a separate UART-to-USB converter chip, the Leonardo can be recognized directly by a computer as an input device, enabling:

- Keyboard emulation for typing text or executing commands

- Mouse emulation for cursor control

- Joystick emulation for gaming applications

- MIDI device implementation for musical applications

## Similar HID-capable boards

- Arduino Micro

- SparkFun Pro Micro

- Adafruit Feather 32u4

- Teensy LC/4.0

## Applications such as Rubber Ducky

The HID capabilities of these boards enable the development of tools similar to the well-known "USB Rubber Ducky." Such applications include:

- Penetration testing: Automating social engineering attacks by emulating trusted input devices to execute predefined commands.

- Task automation: Creating physical macros to run complex sequences of commands simply by connecting the device.

- Restriction bypassing: Circumventing restrictions on systems where executables are blocked but standard input devices are allowed.

- Security auditing: Assessing security policies and raising awareness about vulnerabilities related to unauthorized input devices.

- Pranks and harmless actions: Executing unexpected actions such as changing wallpapers or displaying surprise messages.

- Rapid system configuration: Quickly deploying settings across new installations or testing environments without manual intervention.