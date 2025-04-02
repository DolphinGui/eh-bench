#!/bin/python3

import sys
import random

argument_names = ["a", "b", "c" ,"d", "e", "f", "g"]
arguments = ["int a = 0", "int b = 0","int c = 0","int d = 0","int e = 0","int f = 0","int g = 0"]

cpp = open(sys.argv[1], "w")

cpp.write("#include \"functions.h\"\n")

hpp = open(sys.argv[2], "w")

hpp.write("#pragma once\n#include \"functions.h\"\n")

main = open(sys.argv[3], "w")

main.write("""
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#define ANKERL_NANOBENCH_IMPLEMENT

#include <doctest.h>
#include <nanobench.h>
#include "functions.h"
#include "branches.h"

""")

testcase_templ = """
TEST_CASE("{name} d{depth} i{iterations}") {{
  ankerl::nanobench::Bench().run("{name} d{depth} i{iterations}",
                                 [] {{ for(int i = 0; i < {iterations}; ++i)
                                 {{ {pre} {basefunction}({args}); {post} }} }});
}}\n\n
"""

def test_format(name, depth, iterations):
  if "exception" in name:
    pre = "try{"
    post = """
} catch(ExceptionBase const&){}
    """
  else:
    pre = ""
    post = ""
  arguments = ["i"]
  arguments.extend(["0"] * 5)
  args = ", ".join(arguments)

  return testcase_templ.format(
    name=name,
    basefunction = "{}_d{}_0".format(name, depth), 
    args = args,
    pre = pre,
    post = post,
    iterations = iterations,
    depth = depth
    )

def call_main(depth, name, iterations):
  main.write(test_format(name, depth, iterations))

def generate(depth, template, name, rettype):
  prev_argnum = 0
  hpp.write("{} {}_d{}_{}({});\n".format(rettype, name, depth, 0, ", ".join(arguments[0:6])))
  for i in reversed(range(depth)):
    if i == 0:
      argnum = 6
    else:
      argnum = random.randint(1, 6)
    arrsize = random.randint(0, 24)
    clobber = argument_names[0:argnum]
    if arrsize > 0:
      arr = "char stack[{}]".format(arrsize)
      clobber.append("stack")
    else:
      arr = ""
    clobber = ", ".join(clobber) 

    if i != depth - 1:
      ret = "{}_d{}_{}({})".format(name, depth, i + 1, ", ".join(argument_names[0:min(argnum, prev_argnum)]))
    else:
      args = ", ".join(argument_names[0:min(argnum, 6)])
      ret = "final_{}({})".format(name, args)
   
    prev_argnum = argnum

    args = ", ".join(arguments[0:argnum])

    cpp.write(template.format(name=name, depth=depth, num = i, args = args, stack = arr, clobbered = clobber, ret = ret))

noerror = """NOINLINE\nint \n{name}_d{depth}_{num}({args}){{
  {stack};
  clobber({clobbered});
  return {ret};
}}\n\n"""

result_type = """NOINLINE\nResultType \n{name}_d{depth}_{num}({args}){{
  {stack};
  clobber({clobbered});
  auto r = {ret};
  if(!r.is_some){{
    return r;
  }}
  clobber(r);
  return r;
}}\n\n"""

depths = [1, 2, 25, 50, 100]
iterations = [1, 50, 200, 1000]

for depth in depths:
  generate(depth, noerror, "noerror", "int")


for depth in depths:
  generate(depth, result_type, "result", "ResultType")


for depth in depths:
  generate(depth, noerror, "exception", "int")

for i in iterations:
  for depth in depths:
    call_main(depth, "noerror", i)
    call_main(depth, "result", i)
    call_main(depth, "exception", i)