import random
import numpy
import functions.pre_proc as pre_proc
import functions.sdTempMask as sdTemMask
import functions.fod_gen as fod_gen
import functions.fba as fba
import functions.id_bottle as id_bottle
import functions.stream_gen as stream_gen
import functions.scripts as scripts

title = "sample"

f = open("main/log.txt", "a")
f.write("\n\nNew Runtime [" + title + "] -----")
f.close()

id_bottle.action(title)
