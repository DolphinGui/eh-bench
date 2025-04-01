#pragma once

struct ResultType {
  bool is_some;
  int result;
};

// As the name suggests, does literally no error
// handling.
int final_noerror(int = 0, int = 1, int = 2, int = 3, int = 4, int = 5, int = 6,
                  int = 7);

// result_error represents ML style error handling, where errors
// are just types. This requires checking the return value
// every single time.
ResultType final_result(int = 0, int = 1, int = 2, int = 3, int = 4, int = 5,
                        int = 6, int = 7);

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

int final_exception(int = 0, int = 1, int = 2, int = 3, int = 4, int = 5,
                    int = 6, int = 7);

int final_exception_success(int = 0, int = 0, int = 0, int = 0, int = 0,
                            int = 0, int = 0, int = 0);
