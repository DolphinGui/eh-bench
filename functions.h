#pragma once

#include "nanobench.h"

#ifdef _MSC_VER
#define NOINLINE [[msvc::noinline]]
#define FORCEINLINE [[msvc::flatten]]
#else
#define NOINLINE [[gnu::noinline]]
#define FORCEINLINE [[gnu::always_inline]]
#endif


template <typename T> FORCEINLINE void clobber(T &&a) {
  ankerl::nanobench::doNotOptimizeAway(a);
}

template <typename T, typename... Ts> FORCEINLINE void clobber(T &&t, Ts &&...ts) {
  clobber(t);
  clobber(ts...);
}

struct ResultType {
  bool is_some;
  int result;
};

// As the name suggests, does literally no error
// handling.
int final_noerror(int = 0, int = 0, int = 0, int = 0, int = 0, int = 0, int = 0,
                  int = 0);

// result_error represents ML style error handling, where errors
// are just types. This requires checking the return value
// every single time.
ResultType final_result(int = 0, int = 0, int = 0, int = 0, int = 0, int = 0,
                        int = 0, int = 0);

struct ExceptionBase {};

struct ExceptionA : ExceptionBase {
  ExceptionA(int t) : type(t) {}
  int type;
};

struct ExceptionB : ExceptionBase {
  ExceptionB(int m) : message(m) {}
  int message;
};

struct ExceptionC : ExceptionBase {
  ExceptionC(int s) : stuff(s) {}
  int stuff;
};

// exception_error throws, semirandomly,
// one of the above exception structs.
// C++ codebases typically have a large
// amount of exception types that
// inherent from std::exception.
// In order to avoid the string allocation
// in std::exception, we define our own
// exception type which contains barely any

int final_exception(int = 0, int = 0, int = 0, int = 0, int = 0, int = 0,
                    int = 0, int = 0);
