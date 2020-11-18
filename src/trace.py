
################################################################################
# filename: trace.py
# date: 16. Nov. 2020
# username: winkste
# name: Stephan Wink
# description: This module supports the trace debugging functionality
################################################################################

################################################################################
# Imports
import sys

################################################################################
# Variables

CRITICAL = 50
ERROR    = 40
WARNING  = 30
INFO     = 20
DEBUG    = 10
NOTSET   = 0

_level_dict = {
    CRITICAL: "CRIT",
    ERROR: "ERROR",
    WARNING: "WARN",
    INFO: "INFO",
    DEBUG: "DEBUG",
}

_level_color = {
    CRITICAL: "\033[1;31m",
    ERROR: "\033[0;31m",
    WARNING: "\033[0;33m",
    INFO: "\033[0m",
    DEBUG: "\033[0;32m",
}

_stream = sys.stderr
_level = DEBUG
_tracer = {}

################################################################################
# Functions

################################################################################
# @brief    get the tracer object based on name
# @param    name    name of the tracer object, or default = 'root'
# @return   returns the found tracer object or the default
################################################################################
def getTracer(name='root'):
    global _tracer

    if name in _tracer:
        return _tracer[name]
    t = Trace(name)
    _tracer[name] = t
    return t

################################################################################
# @brief    set debug trace message to 'root'
# @param    msg     trace message
# @return   *args   variable argument list
################################################################################
def debug(msg, *args):
    getTracer().debug(msg, *args)

################################################################################
# @brief    set info trace message to 'root'
# @param    msg     trace message
# @return   *args   variable argument list
################################################################################
def info(msg, *args):
    getTracer().info(msg, *args)

################################################################################
# @brief    set warning trace message to 'root'
# @param    msg     trace message
# @return   *args   variable argument list
################################################################################
def warning(msg, *args):
    getTracer().warning(msg, *args)

################################################################################
# @brief    set error trace message to 'root'
# @param    msg     trace message
# @return   *args   variable argument list
################################################################################
def error(msg, *args):
    getTracer().error(msg, *args)

################################################################################
# @brief    set a trace message in the corresponding tracer
# @param    tracer  tracer name identification
# @param    level   criticality of message
# @param    msg     trace message
# @return   *args   variable argument list
################################################################################
def trace(tracer, level, msg, *args):
    getTracer(tracer).trace(level, msg, *args)

################################################################################
# @brief    configures a tracer
# @param    tracer  tracer name identification
# @param    level   minimum criticality of message
################################################################################
def configure(tracer, level=INFO):
    getTracer(tracer).set_Level(level)

################################################################################
# Classes

################################################################################
# @brief    This is the trace class.
################################################################################
class Trace:

    ############################################################################
    # Member Attributes
    level = NOTSET

    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    constructor of the Trace class
    # @param    any_para    description
    # @param    tag_name    name of the trace class
    # @return   none
    ############################################################################
    def __init__(self, name):
        self.name = name

    ############################################################################
    # @brief    get the level string
    # @param    level    level identifier
    # @return   level string according to level identifier or defaut level
    ############################################################################
    def _get_level_str(self, level):
        l = _level_dict.get(level)
        if l is not None:
            return l
        return "LVL%s" % level

    ############################################################################
    # @brief    get the level color code
    # @param    level    level identifier
    # @return   level color code
    ############################################################################
    def _get_level_color(self, level):
        l = _level_color.get(level)
        if l is not None:
            return l
        return "\033[0;35m"

    ############################################################################
    # @brief    set the trace level
    # @param    level    level identifier
    # @return   none
    ############################################################################
    def set_Level(self, level):
        self.level = level

    ############################################################################
    # @brief    compares a given level with the configured level
    # @param    level    level identifier
    # @return   True if the given level is higher or equal the configured level
    ############################################################################
    def is_enabled_for(self, level):
        global _level
        return level >= (self.level or _level)

    ############################################################################
    # @brief    main function to set a trace message
    # @param    level    level identifier
    # @param    msg trace message
    # @param    argument list of message
    # @return   none
    ############################################################################
    def trace(self, level, msg, *args):
        if self.is_enabled_for(level):
            levelname = self._get_level_str(level)
            levelcolor = self._get_level_color(level)
            if args:
                msg = msg % args

            print(levelcolor, levelname, ":", self.name, ":", msg, "\033[0m", sep="", file=_stream)

    ############################################################################
    # @brief    set a debug trace message
    # @param    msg trace message
    # @param    argument list of message
    # @return   none
    ############################################################################
    def debug(self, msg, *args):
        self.trace(DEBUG, msg, *args)

    ############################################################################
    # @brief    set a info trace message
    # @param    msg trace message
    # @param    argument list of message
    # @return   none
    ############################################################################
    def info(self, msg, *args):
        self.trace(INFO, msg, *args)

    ############################################################################
    # @brief    set a warning trace message
    # @param    msg trace message
    # @param    argument list of message
    # @return   none
    ############################################################################
    def warning(self, msg, *args):
        self.trace(WARNING, msg, *args)

    ############################################################################
    # @brief    set an error trace message
    # @param    msg trace message
    # @param    argument list of message
    # @return   none
    ############################################################################
    def error(self, msg, *args):
        self.trace(ERROR, msg, *args)

################################################################################
# Scripts
if __name__ == "__main__":
    print("--- trace test script ---")
    print('--- trace test script ---')
    info("This is an information.")
    debug("This is a debug message.")
    warning("This is a warning.")
    error("This is an error.")
    trace('TRACE', DEBUG, 'This is a message in trace')
    #sets the criticality level for 'TRACE' to default = INFO
    configure('TRACE')
    #not displayed because of the criticality level configuration
    trace('TRACE', DEBUG, 'This is trace DEBUG')
    trace('TRACE', INFO, 'This is trace INFO')
    mytuple = ("apple", "banana", "cherry")
    print('tuple test:' + mytuple)
