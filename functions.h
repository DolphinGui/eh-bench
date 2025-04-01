#pragma once

struct ResultType {
  bool is_some;
  int result;
};

// literally does nothing, exists to inhibit compiler optimization;
void clobber(int *, int *, int *, int *, int *, int *, int *);

// As the name suggests, does literally no error
// handling.
int no_error(int, int, int, int, int, int, int, int);

// result_error represents ML style error handling, where errors
// are just types. This requires checking the return value
// every single time.
ResultType result_error(int, int, int, int, int, int, int, int);

struct ExceptionBase {};

struct ExceptionA : ExceptionBase {
  int type;
};

struct ExceptionB : ExceptionBase {
  int message;
};

struct ExceptionC : ExceptionBase {
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
int exception_error(int, int, int, int, int, int, int, int);
