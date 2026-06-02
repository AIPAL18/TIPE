#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

/*
We assume that both are the same length.
For now, we're working with inner data, therefore very limited in terms of size
so we allow ourselves to iterate through it all.
*/

void encode(uint8_t t1[], uint8_t t2[], size_t length) {
    for (size_t i = 0; i < length; ++i) {
        if (t1[i] != t2[i]) {
            printf("%02zu| %02x - %02x\n", i, t1[i], t2[i]);
        }
    }
}

int main(int argc, char** argv) {
    (void)argc;
    (void)argv;
    // if (argc <= 1) {
    //     printf("usage:\n");
    // }

    // uint8_t t1[] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x01};
    // uint8_t t2[] = {0x10, 0x11, 0x12, 0x03, 0x04, 0x05, 0x06, 0x17, 0x01};

    // encode(t1, t2, sizeof(t1)/sizeof(uint8_t));

    FILE* f = fopen("./libc.so.5", "r");
    if (f == NULL) {
        printf("error\n");
        return 0;
    }
    size_t i = 0;
    unsigned char word = 1;
    while (i < 10 && word != '\0') {
        fread(&word, sizeof(unsigned char), 1, f);
        printf("%d\n", word);
    }

    fclose(f);
    
    return 0;
}