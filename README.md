# MicroPython Generic Application for ESP32
This project integrates several different skills into one application. The target for this application is a ESP32 microcontroller. The programming language used is micropython. The system is devided in:
- driver layer
- support and protocol modules
- application skills

## The driver layer includes handling for:
- user boot and main encapsulation
- parameter handling
- bluethooth driver
- application information handling
- trace message and debug logging interface

## The support and protocol modules include:
- github over the air firmware updates
- mqtt abstraction handling including subscriber and publisher modules
- skill manager for starting, executing and stopping the skills

## Application Skills
- single relay handling controlled via MQTT
- DHT22 temperature and humidity publishing
- temt6000 light sensor 
- PIR polled based motion detection
- single neopixel control via MQTT
- MIJA bluethooth temperature and humidity sensor reading 

## Setup & Preparations

### Used development environment
- IDE: ATOM with extension Pymakr
- MicroPython interpreter: esp32-idf3-20200902-v1.13.bin

### Interpreter setup on OSx

get actual interface
```
ls /dev/cu.*
```

erase actual target
```
esptool.py --port /dev/cu.SLAB_USBtoUART erase_flash
```

load the micropython interpreter executable (binary file) to the target
```
esptool.py --chip esp32 --port /dev/cu.SLAB_USBtoUART --baud 460800 write_flash -z 0x1000 PATH_TO_FOLDER/esp32-idf3-20200902-v1.13.bin  
```

upload a script to micropython
```
ampy --port /dev/cu.SLAB_USBtoUART run test.py
```

replace / put a file on the target
```
ampy --port /dev/cu.SLAB_USBtoUART put test.py /main.py
```
