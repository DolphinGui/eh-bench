#include "functions.h"

NOINLINE
int final_exception(int a, int b, int c, int d, int e, int f, int g, int h) {
  int stack[21];
  asm volatile(""
               : "+m"(a), "+m"(b), "+m"(c), "+m"(d), "+m"(e), "+m"(f),
                 "=m"(stack)::"memory");
  start_timing();
  throw ExceptionB(12);
}
