#include "branches.h"
#include "functions.h"
#include "nanobench.h"


NOINLINE
int final_noerror(int a, int b, int c, int d, int e, int f, int g, int h) {
  int stack[21];
  clobber(a, b, c, d, e, f, g, h, stack);
  return (a + b + c + d + e + f + g + h);
}