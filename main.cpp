#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#define ANKERL_NANOBENCH_IMPLEMENT
#include "nanobench.h"
#include "functions.h"


TEST_CASE("testing") {

  double d = 1.0;
  ankerl::nanobench::Bench().run("some double ops", [&] {
    d += 1.0 / d;
    if (d > 5.0) {
      d -= 5.0;
    }
    ankerl::nanobench::doNotOptimizeAway(d);
  });
}
