#include "functions.h"

NOINLINE
int final_exception(int a, int b, int c, int d, int e, int f) {
  start_timing();
  throw ExceptionB(12);
}
