#!/bin/python3

import sys
import random

argument_names = ["a", "b", "c" ,"d", "e", "f", "g"]
arguments = ["int a = 0", "int b = 1","int c = 2","int d = 3","int e = 4","int f = 5","int g = 6"]

cpp = open(sys.argv[1], "w")

cpp.write("#include \"functions.h\"\n")

hpp = open(sys.argv[2], "w")

hpp.write("#pragma once\n")

main = open(sys.argv[3], "w")

main.write("""
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN

#include "functions.h"
#include "branches.h"
#include <doctest.h>
#include <nanobench.h>

""")

testcase_templ = """
TEST_CASE("{name}") {{
  ankerl::nanobench::Bench().run("{name}",
                                 [] {{ {pre} {basefunction}({args}); {post} }});
}}\n\n
"""

except_fail = True

def test_format(name, depth, i, argnum):
  if "exception" in name:
    pre = "try{"
    post = """
} catch(ExceptionBase const&){}
    """
  else:
    pre = ""
    post = ""

  args = ", ".join(map(str, range(argnum)))

  return testcase_templ.format(
    name=name,
    basefunction = "{}_d{}_{}".format(name, depth, i), 
    args = args,
    pre = pre,
    post = post
    )

def generate(depth, template, name, rettype):
  prev_argnum = 0
  for i in reversed(range(depth)):
    argnum = random.randint(1, 6)
    arrsize = random.randint(0, 24)
    clobber = ["\"+m\"({})".format(r) for r in argument_names[0:argnum]]
    if arrsize > 0:
      arr = "char stack[{}]".format(arrsize)
      clobber.append("\"=m\"(stack)")
    else:
      arr = ""
    clobber = ", ".join(clobber) 

    if i != depth - 1:
      ret = "{}_d{}_{}({})".format(name, depth, i + 1, ", ".join(argument_names[0:min(argnum, prev_argnum)]))
      if i == 0:
        hpp.write("{} {}_d{}_{}({});\n".format(rettype, name, depth, i, ", ".join(arguments[0:argnum])))
        main.write(test_format(name, depth, i, argnum))
    else:
      if except_fail:
        args = ", ".join(argument_names[0:min(argnum, 6)])
      else:
        args = ", ".join(["0"] * argnum)
      ret = "final_{}({})".format(name, args)
   
    prev_argnum = argnum

    cpp.write(template.format(name=name, depth=depth, num = i, args = ", ".join(arguments[0:argnum]), stack = arr, asm = clobber, ret = ret))

noerror = """[[gnu::noinline]]int \n{name}_d{depth}_{num}({args}){{
  {stack};
  asm volatile("" : {asm} :: "memory");
  return {ret};
}}\n\n"""

result_type = """[[gnu::noinline]]ResultType \n{name}_d{depth}_{num}({args}){{
  {stack};
  asm volatile("" : {asm} :: "memory");
  auto r = {ret};
  if(!r.is_some){{
    return r;
  }}
  asm volatile("" : "=m"(r) :: "memory");
  return r;
}}\n\n"""


generate(1, noerror, "noerror", "int")

for depth in range(25, 225, 25):
  generate(depth, noerror, "noerror", "int")

generate(1, result_type, "result", "ResultType")

for depth in range(25, 225, 25):
  generate(depth, result_type, "result", "ResultType")

generate(1, noerror, "exception", "int")

for depth in range(25, 225, 25):
  generate(depth, noerror, "exception", "int")

except_fail = False

generate(1, noerror, "exception_success", "int")

for depth in range(25, 225, 25):
  generate(depth, noerror, "exception_success", "int")