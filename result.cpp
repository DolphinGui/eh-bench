#include "functions.h"

ResultType::~ResultType() = default;

[[gnu::noinline]]
ResultType final_result(int a, int b, int c, int d, int e, int f, int g,
                        int h) {
  ResultType r;
  int stack[21];
  asm volatile(""
               : "+m"(a), "+m"(b), "+m"(c), "+m"(d), "+m"(e), "+m"(f), "+m"(g),
                 "+m"(h), "=m"(stack)::"memory");
  r.is_some = false;
  start_timing();
  return r;
}
