#include "functions.h"

NOINLINE
int final_exception(int a, int b, int c, int d, int e, int f, int g, int h) {
  int stack[21];
  clobber(stack, a, b, c, d, e, f, g, h);
  if (!(a + b + c + d + e + f + g + h)) {
    throw ExceptionB(12);
  }
  return 12;
}
