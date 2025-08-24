#include "functions.h"

ResultType::~ResultType() = default;

NOINLINE
ResultType final_result(int a, int b, int c, int d, int e, int f, int g,
                        int h) {
  ResultType r;
  r.is_some = false;
  start_timing();
  return r;
}
