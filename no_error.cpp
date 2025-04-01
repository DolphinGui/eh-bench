#include "functions.h"
#include "branches.h"

[[gnu::noinline]]
int final_noerror(int a, int b, int c, int d, int e, int f, int g, int h) {
  int stack[21];
  asm volatile(""
               : "+m"(a), "+m"(b), "+m"(c), "+m"(d), "+m"(e), "+m"(f),
                 "=m"(stack)::"memory");
  return (a + b + c + d + e + f + g + h);
}