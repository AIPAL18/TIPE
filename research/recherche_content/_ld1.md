# ld.so : the everything

```txt
user runs program
    ↓
kernel loads ELF executable
    ↓
kernel notices PT_INTERP
    ↓
kernel maps ld.so into memory
    ↓
kernel jumps into ld.so entry point
    ↓
ld.so loads dependencies
    ↓
ld.so relocates everything
    ↓
ld.so calls constructors
    ↓
ld.so jumps to executable entry point
    ↓
eventually main()
```

```cmd
readelf -Ws ld.so
```

```cmd
nm -D (--defined-only) ld.so
```

```cmd
objdump -T ld.so
```
