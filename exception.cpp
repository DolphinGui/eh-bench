#include "functions.h"

NOINLINE
int final_exception(int a) {
  int stack[21];
  asm volatile("" : "=m"(stack)::"memory");
  start_timing();
  throw ExceptionB(12);
}
