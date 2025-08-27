#include "functions.h"

ResultType::~ResultType() = default;

NOINLINE
ResultType final_result(int a, int b, int c, int d, int e, int f) {
  ResultType r;
  r.is_some = false;
  return r;
}
