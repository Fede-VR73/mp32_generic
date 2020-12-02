# mp32_generic
This project integrates several different skills into one application. The target for this application is a ESP32 microcontroller. The programming language used is micropython. The system is devided in:
- driver layer
- support and protocol modules
- application skills

# The driver layer includes handling for:
- user boot and main encapsulation
- parameter handling
- bluethooth driver
- application information handling
- trace message and debug logging interface

# The support and protocol modules include:
- github over the air firmware updates
- mqtt abstraction handling including subscriber and publisher modules
- skill manager for starting, executing and stopping the skills

# Application Skills
- single relay handling controlled via MQTT
- DHT22 temperature and humidity publishing
- temt6000 light sensor 
- PIR polled based motion detection
- single neopixel control via MQTT
- MIJA bluethooth temperature and humidity sensor reading 
