#pragma once

#ifdef _MSC_VER
#define NOINLINE [[msvc::noinline]]
#define FORCEINLINE [[msvc::flatten]]
#else
#define NOINLINE [[gnu::noinline]]
#define FORCEINLINE [[gnu::always_inline]]
#endif

struct ResultType {
  bool is_some;
  int result;
  // Usually either the error or the result is non-trivial because it contains
  // a string or a nontrivial result. To emulate that, we add a non-trivial
  // destructor to force the return value to be spilled onto the stack.

  // To be clear I'm not really sure this is necessarily reflective of how other
  // languages work. It absolutely is reflective of how C++ works
  // (std::expected), but looking at toy examples in Godbolt for rust seems to
  // show that it can pass certain non-trivial objects in registers (Box). I'm
  // not sure if this is because rust doesn't follow any ABI, or because Box is
  // just special in rust. I have even less of an idea how Go code generation
  // even works.
  ~ResultType();
};

// similar to ResultType, but trivially destructable
struct TrivialResult {
  bool is_some;
  int result;
};

// As the name suggests, does literally no error
// handling.
int final_noerror(int = 0, int = 0, int = 0, int = 0, int = 0, int = 0);

// result_error represents ML style error handling, where errors
// are just types. This requires checking the return value
// every single time.
ResultType final_result(int = 0, int = 0, int = 0, int = 0, int = 0, int = 0);
TrivialResult final_trivial(int = 0, int = 0, int = 0, int = 0, int = 0, int = 0);

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

int final_exception(int = 0, int = 0, int = 0, int = 0, int = 0, int = 0);
