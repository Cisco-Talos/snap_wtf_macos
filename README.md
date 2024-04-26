# WTF Snapshot fuzzing of macOS targets

Support tooling , patches and sample fuzzers. 
For a detailed usage guide, see: https://blog.talosintelligence.com/macos-snapshot-fuzzing

Contains: 
- `dump_symbols.py` - an LLDB scripts to make a JSON symbol store to use for symbolicating traces
- `symbolize.py` - turn raw memory addresses into symbolized traces (module+offset) for easier debugging
- `vmware_volatility_wtf.patch` - patch for Volatility framework to dump CPU state in format that WTF expects
- `wtf_vmware.patch` - patch that adds VMWare memory snapshot loading to WTF. 
- `targets` - sample fuzzing harness(es) 

# Usage

After applying the patches and acquiring the snapshot, you can test run the fuzzer with IPv6 target like so:

```
c:\work\codes\wtf\targets\ipv6_input>..\..\src\build\wtf.exe  run  --backend=bochscpu --name IPv6_Input --state state --input inputs\ipv6 --trace-type 1 --trace-path .
The debugger instance is loaded with 0 items
load raw mem dump1
Done
Setting debug register status to zero.
Setting debug register status to zero.
Segment with selector 0 has invalid attributes.
Segment with selector 0 has invalid attributes.
Segment with selector 8 has invalid attributes.
Segment with selector 0 has invalid attributes.
Segment with selector 10 has invalid attributes.
Segment with selector 0 has invalid attributes.
Trace file .\ipv6.trace
Running inputs\ipv6
--------------------------------------------------
Run stats:
Instructions executed: 13001 (4961 unique)
      	Dirty pages: 229376 bytes (0 MB)
  	Memory accesses: 46135 bytes (0 MB)
#1 cov: 4961 exec/s: infm lastcov: 0.0s crash: 0 timeout: 0 cr3: 0 uptime: 0.0s
 
c:\work\codes\wtf\targets\ipv6_input>
```



# License 

WTF patches and support utilities are MIT licensed as is WTF itself. Volatility patches are GPL licensed to match Volatility's license. 

# Acquire and patch volatility 

Needs to be applied to specific commit. 
```
	git clone https://github.com/volatilityfoundation/volatility
	git checkout a438e768194a9e05eb4d9ee9338b881c0fa25937
	git apply vmware_volatility_wtf.patch
```

