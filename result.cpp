#include "functions.h"

NOINLINE
ResultType final_result(int a, int b, int c, int d, int e, int f, int g,
                        int h) {
  ResultType r;
  int stack[21];
  clobber(stack, a, b, c, d, e, f, g, h);
  if (!(a + b + c + d + e + f + g + h)) {
    r.is_some = 0;
    r.result = -1;
  } else {
    r.is_some = 1;
    r.result = a;
  }
  return r;
}
