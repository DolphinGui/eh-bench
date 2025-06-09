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
#define PICOBENCH_IMPLEMENT_WITH_MAIN
#include "picobench.hpp"

#include "functions.h"
#include "branches.h"

""")

testcase_templ = """
static void {name}_d{depth}(picobench::state& s) {{
  global_timer = &s;
  int i = 0;
  for (auto _ : s) {{ 
  {pre}
  {basefunction}({args}); 
  {post}
  s.stop_timer();
  i += 1;
  }}
  global_timer = nullptr;
}}
PICOBENCH({name}_d{depth});
"""

def test_format(name, depth):
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
    depth = depth
    )

def call_main(depth, name):
  main.write(test_format(name, depth))

def generate(depth, template, name, rettype):
  hpp.write("{} {}_d{}_{}({});\n".format(rettype, name, depth, 0, ", ".join(arguments[0:6])))
  for i in reversed(range(depth)):
    if i == 0:
      argnum = 6
    else:
      argnum = random.randint(1, 6)
    arrsize = random.randint(0, 24)
    if arrsize > 0:
      arr = "char stack[{}]".format(arrsize)
      clobber = """"=m"(stack)"""
    else:
      arr = ""
      clobber = ""

    if i != depth - 1:
      ret = "{}_d{}_{}()".format(name, depth, i + 1)
    else:
      ret = "final_{}()".format(name)
   
    args = ", ".join(arguments[0:argnum])

    cpp.write(template.format(name=name, depth=depth, num = i, args = args, stack = arr, ret = ret, clobber = clobber))

noerror = """NOINLINE\nint \n{name}_d{depth}_{num}({args}){{
  {stack};
  asm volatile("" : {clobber} :: "memory");
  return {ret};
}}\n\n"""

result_type = """NOINLINE\nResultType \n{name}_d{depth}_{num}({args}){{
  {stack};
  asm volatile("" : {clobber} :: "memory");
  auto r = {ret};
  if(!r.is_some){{
    return r;
  }}
  asm volatile("" : "+m"(r) :: "memory");
  return r;
}}\n\n"""

depths = [2]

for depth in depths:
  generate(depth, noerror, "noerror", "int")

for depth in depths:
  generate(depth, result_type, "result", "ResultType")

for depth in depths:
  generate(depth, noerror, "exception", "int")

for depth in depths:
  main.write(f'PICOBENCH_SUITE("Depth {depth}");\n')
  call_main(depth, "noerror")
  call_main(depth, "result")
  call_main(depth, "exception")