# SPDX-License-Identifier: MIT
#
# Copyright 2024 Cisco Systems, Inc. and its affiliates
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import json
import sys
import numpy as np    

f = open("symbol-store.json","r")
symbols = json.load(f)
f.close()
l = [int(x,16) for x in symbols.keys()]
nl = np.array(l, dtype=np.uint64) 
addresses = np.sort(nl)
last_addr = 0
last_found = 0

def findSymbol(addr):
    global last_addr
    global last_found
    #high chance that next instruction belongs to the same function
    # this "prediction" can fail in certain situations
    # but it's inconsequential and greatly speeds things up
    if abs(addr-last_addr) < 16: #my approx. at a longest instruction
        found = last_found
    else:
        try:
            found = addresses[addresses<=addr][-1]
        except:
            return None, None
    last_found = found
    last_addr = addr
    return found,symbols["0x%.16x"%found]
    #input()

def symbolize(address):
    addr , name = findSymbol(address)
    if not addr:
        return hex(address)
    offset =  (address -  addr)
    if offset > 0:
        name = "%s+0x%x"%(name,offset)
    return name

if __name__ == '__main__':
    trace = open(sys.argv[1],"r")
    of = open(sys.argv[2],"w")
    for l in trace.readlines():
        of.write(symbolize(int(l.strip(),16))+"\n")
    of.close()
