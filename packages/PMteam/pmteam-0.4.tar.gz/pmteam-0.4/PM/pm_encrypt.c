#include <stdlib.h>
#include <string.h>
#include "pm_encrypt.h"

#define BLOCK_SIZE 16

void xor_and_reverse(unsigned char *data, const unsigned char *key, size_t len) {
    for (size_t i = 0; i < len; i++)
        data[i] ^= key[i % BLOCK_SIZE];

    for (size_t i = 0; i < len / 2; i++) {
        unsigned char temp = data[i];
        data[i] = data[len - i - 1];
        data[len - i - 1] = temp;
    }
}

void Encrypt(unsigned char *data, const unsigned char *key, size_t len) {
    for (int i = 0; i < 4; i++)
        xor_and_reverse(data, key, len);
}

void Decrypt(unsigned char *data, const unsigned char *key, size_t len) {
    for (int i = 0; i < 4; i++) {
        for (size_t j = 0; j < len / 2; j++) {
            unsigned char temp = data[j];
            data[j] = data[len - j - 1];
            data[len - j - 1] = temp;
        }

        for (size_t j = 0; j < len; j++)
            data[j] ^= key[j % BLOCK_SIZE];
    }
}
