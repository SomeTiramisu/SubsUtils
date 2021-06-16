#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

inline void byte_encode(uint8_t*);
void uuencode(FILE*);

void byte_encode(uint8_t* buf) {
    uint32_t x = (buf[0]<<16)+(buf[1]<<8)+buf[2];
    uint8_t y1 = ((x>>18)&63)+33;
    uint8_t y2 = ((x>>12)&63)+33;
    uint8_t y3 = ((x>>6)&63)+33;
    uint8_t y4 = (x&63)+33;
    putchar(y1);
    putchar(y2);
    putchar(y3);
    putchar(y4);
}

void uuencode(FILE* file) {
  uint8_t* xbuf = calloc(3, sizeof(uint8_t));
  size_t n;
  size_t k;
  while(n = fread(xbuf, sizeof(uint8_t), 3, file) == 3) {
    byte_encode(xbuf);
    k += 4;
    if(k%80==0 && k!=0) {
        putchar('\n');
    }
  }
  if(n==1) {
    xbuf[1] = 0;
    xbuf[2] = 0;
    byte_encode(xbuf);
  }
  if(n==2) {
    xbuf[2] = 0;
    byte_encode(xbuf);
  }
  free(xbuf);
}

void main(int argc, char* argv[]) {
  //FILE* file = fopen("/home/guillaume/Documents/subtitle_extract/v5r/todoroki.ass", "rb");
  FILE* file = fopen(argv[1], "rb");
  uuencode(file);
  fclose(file);
}
