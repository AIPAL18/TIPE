#include <stdio.h>
#include <elf.h>
#include <assert.h>

#ifndef __linux__
printf("This compiler only supports Linux architectures\n");
assert(false);
#else
printf("OS: Ok\n");
#endif

#ifndef __x86_64__
printf("This compiler only supports x86_64 architectures\n");
assert(false);
#endif



int main(void) {

    return 0;
}
