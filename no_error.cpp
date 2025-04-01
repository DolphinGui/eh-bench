#include "functions.h"

[[gnu::noinline]]
int final_noerror(int a, int b, int c, int d, int e, int f, int g, int h) {
  int stack[21];
  asm volatile(""
               : "+m"(a), "+m"(b), "+m"(c), "+m"(d), "+m"(e), "+m"(f),
                 "=m"(stack)::"memory");
  return ((a & b) | (c ^ d + f) / (g - h));
}

[[gnu::noinline]]
int no_error(int a, int b, int c, int d, int e, int f, int g, int h) {
  int stack[4];
  asm volatile(""
               : "+m"(a), "+m"(b), "+m"(c), "+m"(d), "+m"(e), "+m"(f), "+m"(g),
                 "+m"(h), "=m"(stack)::"memory");
  return final_noerror(a, b, c, d, e, f, g, h);
}
