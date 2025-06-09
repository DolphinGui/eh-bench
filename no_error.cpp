#include "branches.h"
#include "functions.h"

NOINLINE
int final_noerror(int a) {
  int stack[21];
  asm volatile("" : "=m"(stack)::"memory");
  start_timing();
  return 1;
}