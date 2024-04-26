# SPDX-License-Identifier: MIT
#
# Copyright 2024 Cisco Systems, Inc. and its affiliates
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import lldb
import json
symbols = {}

"""
(lldb) image lookup -a 0xffffff801172277f
      Address: kernel[0xffffff800031277f] (kernel.__TEXT.__text + 989055)
      Summary: kernel`vm_fault_deactivate_behind + 15 at vm_fault.c:501
"""
def parseLookup(lookup):
    summary = lookup.split("\n")[1].strip()
    print(summary)
    name = summary.split(" ")[1].split("`")[1].split("(")[0]
    print(name)
    return name

def parseDump(dump,debugger):
    result1 = lldb.SBCommandReturnObject()
    ci = debugger.GetCommandInterpreter()
    for line in dump.split("\n"):
        if line.startswith("["):
                parts = line.split()
                if parts[0] == '[':
                    parts.pop(0)
                if parts[3] == "Invalid":
                    continue
                if len(parts) < 9:
                    continue
                file_addr = parts[4]
                load_addr = parts[5]
                size = parts[6]
                print(parts)
                name = parts[8].split("(")[0]
                if "___lldb_unnamed_symbol" in name:
                    ci.HandleCommand("image lookup -a " + load_addr,result1)
                    name = None
                    if result1.Succeeded():
                        name = parseLookup(result1.GetOutput())
                    if name == None:
                        continue
                print("%s @ %s"%(name,load_addr))
                symbols[load_addr] = name


def dumpSymbols(debugger, command, result, dict):
    result1 = lldb.SBCommandReturnObject()
    ci = debugger.GetCommandInterpreter()
    ci.HandleCommand(command,result1)  
    if result1.Succeeded():
        parseDump(result1.GetOutput(),debugger)
    f = open("symbol-store.json","w")
    json.dump(symbols,f)
    f.close()

def __lldb_init_module (debugger, dict):
  debugger.HandleCommand('command script add -f dump_symbols.dumpSymbols dumpSymbols')
