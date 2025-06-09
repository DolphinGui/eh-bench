#include "functions.h"

ResultType::~ResultType() = default;

NOINLINE
ResultType final_result(int a) {
  ResultType r;
  int stack[21];
  asm volatile("" : "=m"(stack)::"memory");
  r.is_some = false;
  start_timing();
  return r;
}
