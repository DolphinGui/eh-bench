#include "functions.h"

[[gnu::noinline]]
ResultType result_final(int a, int b, int c, int d, int e, int f, int g,
                        int h) {
  ResultType r;
  int stack[21];
  asm volatile(""
               : "+m"(a), "+m"(b), "+m"(c), "+m"(d), "+m"(e), "+m"(f), "+m"(g),
                 "+m"(h), "=m"(stack)::"memory");
  if ((a & b) | (c ^ d + f) / (g - h)) {
    r.is_some = 0;
    r.result = -1;
  } else {
    r.is_some = 1;
    r.result = a;
  }
  return r;
}

[[gnu::noinline]]
ResultType result_error(int a, int b, int c, int d, int e, int f, int g,
                        int h) {
  int stack[4];
  asm volatile(""
               : "+m"(a), "+m"(b), "+m"(c), "+m"(d), "+m"(e), "+m"(f), "+m"(g),
                 "+m"(h), "=m"(stack)::"memory");

  auto n = result_final(a, b, c, d, e, f, g, h);
  if (!n.is_some) {
    return n;
  }
  return ResultType{0, -12};
}
