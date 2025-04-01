# The Error Handling Benchmark

This is a micro-benchmark seeking to compare exception handling
and value-based error handling. It utilizes heavy use of code
generation in order to generate a large amount of functions
to simulate deep call stacks.

Here, we compare value-based error handling, where the error
is communicated in the return value (or result) of a function.
(hereinafter "result handling") Result handling is claimed
to achieve higher performance, reliability, and code reasoning
when compared to exception handling. Result handling comes
from the ML family of languages, where results are represented
as discriminated unions of types. In particular, the language
Rust has popularized the concept of result handling in
the programming community.

Exception handling on the other hand, has been the predominant
form of error handling in many langauges. It is particularly
ubiquitous in C++, but is also seen in Java, Python, Javascript,
and C#.

Due to the rising popularity of Rust and its associated ML
language concepts, a debate has arose surrounding result
versus exception based error handling. The debates discuss
various aspects of each such as reliability, ergonomics,
performance, and the such. However, there has been a startling
lack of rigor when discussing the performance characteristics
of either exception handling regime. For that reason, I
have written a benchmark comparing exception handling
and result handling.

## Dependencies

Requires python3 and meson to build. All other dependencies
are included in the project as single-file headers.

## Methodology

Functions are generated with varying amounts of parameters ranging
from 1 parameter to 6 parameters. A varying amount of stack is
allocated in the form of an array from 0 to 24 bytes. Everything
is forced to be spilled onto stack via the use of inline assembly.
This is done to reduce the amount of work done in each function call
in order to reduce the overhead of each function call.

In this, we study three different error handling cases. The first is
the null case, where no error handling is present. The second case
is the case of result-based error handling, where errors are represented
using a discriminated union. The third type is exception based error
handling, where errors are signaled by throwing exceptions.

In the no error case, all the function does is return the sum of the
arguments passed. The operation is done in order create a data
dependency in order to prevent the cpu from pipelining the operations.
(See [Dr. Poss's work on this](https://dr-knz.net/measuring-errors-vs-exceptions-in-go-and-cpp.html))

The generated functions are called one after another, passing the parameters
along. They are called at call depths ranging from 1 intermediate function
to 100 intermediate functions. For each test iteration, the functions are
called a varying amount of times, ranging from once to 1000 times. Only
the first invocation results in an error, simulating cases where errors
are expected to be very rare.

## Discussion

See the [data file](results/x86-linux-gcc.txt) for the raw data. This was done
on a IdeaPad 3 15ITL6, where the cpu was an intel i5-1135G7. More testing
on different platforms is needed.

The data is shown in tabular format. The benchmark name indicates error
handling type (none, result, exceptions), call stack depth (d1 indicating 1
intermediate function), and number of work iterations (i1 indicating 1 time).

As expected, result handling adds overhead in comparison to no
error handling. Surprisingly, at small call depths, the overhead is almost
within the margin of error. This could be because the cpu is able to defeat
the benchmark, which is purposefully very light on memory operations. (Poss, 2020)
At deeper call depths, the constant overhead is much more significant.

Notably, exception handling overhead rises with call depth. This is similar to
result handling, which also rises with call depth. This is because the exception
handling library must unwind the call stack similarly to how result handling must
go through every single funciton. Because of this, exceptions do not outperform
result handling even in very deep call stacks.

Notably however, in very high call depth cases, and in very high iteration counts,
exceptions can sometimes outperform result types. This is probably because the locality
of the exception unwinding mechanism at such high call stacks is greater than the
locality of result handling.

## Conclusions

Given current implementations, exceptions are almost never faster than result handling
for control flow purposes. Assuming you care about the performance in the error
path (not a given for most applications), result types are almost always faster.

This study does not attempt to research the ergonomic, reliability, or other
charactersitics of each error handling mechanism. Such things have been discussed
significantly already and is not the focus of this study. 

Moreover, this study is a study on microbenchmarking the error handling mechanisms.
Real code does work in their functions, unlike the synthetic functions generated here.
Because of that, the additional pressure on the branch predictor, increased
code size, among other factors may make result handling worse for performance overall.

Rather, this study attempts to elucidate the current state of exception handling runtimes.
The author believes that there are many missed optimization opportunities in the exception
handling regime, and has written a benchmark to compare them.
