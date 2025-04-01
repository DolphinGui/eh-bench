#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN

#include "functions.h"
#include <doctest.h>
#include <nanobench.h>

TEST_CASE("no_error") {
  ankerl::nanobench::Bench().run("no error",
                                 [&] { no_error(1, 2, 3, 4, 5, 6, 7, 8); });
}

TEST_CASE("result type error") {
  ankerl::nanobench::Bench().run("result",
                                 [&] { result_error(1, 2, 3, 4, 5, 6, 7, 8); });
}

