/* SPDX-License-Identifier: MIT

  Copyright 2024 Cisco Systems, Inc. and its affiliates

  Use of this source code is governed by an MIT-style
  license that can be found in the LICENSE file or at
  https://opensource.org/licenses/MIT.
 */

#include "backend.h"
#include "targets.h"
#include <fmt/format.h>
//ping6 fe80::817:b01e:899b:45b2%en0 -c 1 -p 41 -s 1016 -b 1064
namespace fs = std::filesystem;

namespace IPv6_Input {

constexpr bool LoggingOn = true;

template <typename... Args_t>
void DebugPrint(const char *Format, const Args_t &...args) {
  if constexpr (LoggingOn) {
    fmt::print("IPv6_Input: ");
    fmt::print(Format, args...);
  }
}


bool InsertTestcase(const uint8_t *Buffer, const size_t BufferSize) {

if (BufferSize < 40) return true; // mutated data too short

  Gva_t ipv6_header = Gva_t(0xffffff80644206d8);
  if(!g_Backend->VirtWriteDirty(ipv6_header,Buffer,40)){
    DebugPrint("VirtWriteDirtys failed\n");
  }

  Gva_t icmp6_data = Gva_t(0xffffff8064401000);
  if(!g_Backend->VirtWriteDirty(icmp6_data,Buffer+40,BufferSize-40)){
    DebugPrint("VirtWriteDirtys failed\n");
  }

  return true;
}

bool Init(const Options_t &Opts, const CpuState_t &) {


  const Gva_t Rip = Gva_t(g_Backend->Rip());


Gva_t exception_triage = Gva_t(0xffffff8011d63acd);
  if (!g_Backend->SetBreakpoint(exception_triage, [](Backend_t *Backend) {
   
        const Gva_t rdi =  Gva_t(g_Backend->Rdi());
        const Gva_t rsi =  Gva_t(g_Backend->Rdi());
        const Gva_t rsp =  Gva_t(g_Backend->Rdi());
        const Gva_t saved_rip = rsp+Gva_t(0x20);
        const uint64_t rip =  g_Backend->VirtRead8(saved_rip);
        const uint64_t fault_address = g_Backend->VirtRead8(rsi+Gva_t(8));
        const std::string Filename = fmt::format(
            "crash-{:#x}-{:#x}-{:#x}", rdi, rip, fault_address);
        DebugPrint("Crash: {}\n", Filename);
        Backend->Stop(Crash_t(Filename));
 
      })) {
    return false;
  }
   
   Gva_t retq = Gva_t(0xffffff801278fcb9);
if (!g_Backend->SetBreakpoint(retq, [](Backend_t *Backend) {
      Backend->Stop(Ok_t());
    })) {
  return false;
}

// patch icmp6 checksum check

retq = Gva_t(0xffffff801275acbe); //397
  if (!g_Backend->SetBreakpoint(retq, [](Backend_t *Backend) {
  g_Backend->Rax(0);
      })) {
    return false;
  }

  //patch tcp_checksum check
 retq = Gva_t(0xffffff80125fbe57); //
  if (!g_Backend->SetBreakpoint(retq, [](Backend_t *Backend) {
  
     g_Backend->Rax(0);
      })) {
    return false;
  }

  return true;
}

bool Restore() { return true; }

//
// Register the target.
//

Target_t IPv6_Input("IPv6_Input", Init, InsertTestcase, Restore);

} // namespace Hevd
