#!/bin/python3

import sys
import random

argument_names = ["a", "b", "c" ,"d", "e", "f", "g"]
arguments = ["int a = 0", "int b = 0","int c = 0","int d = 0","int e = 0","int f = 0","int g = 0"]

cpp = open(sys.argv[1], "w")

cpp.write("#include \"branches.h\"\n")

hpp = open(sys.argv[2], "w")

hpp.write("#pragma once\n#include \"functions.h\"\n")

main = open(sys.argv[3], "w")

main.write("""
#include "benchmark/benchmark.h"

#include "functions.h"
#include "branches.h"

""")

testcase_templ = """
static void {name}_d{depth}(benchmark::State& s) {{
  int i = 0;
  for (auto _ : s) {{ 
  {pre}
  {basefunction}({args}); 
  {post}
  i += 1;
  }}
}}
BENCHMARK({name}_d{depth});
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

functions = []

def generate(depth, template, name, rettype):
  prev_argnum = 0
  for i in reversed(range(depth)):
    if i == 0:
      argnum = 6
    else:
      argnum = random.randint(1, 6)
    hpp.write("extern \"C\" {} {}_d{}_{}({});\n".format(rettype, name, depth, i, ", ".join(arguments[0:argnum])))

    if i != depth - 1:
      ret = "{}_d{}_{}({})".format(name, depth, i + 1, ", ".join(argument_names[0:min(argnum, prev_argnum)]))
    else:
      args = ", ".join(argument_names[0:min(argnum, 6)])
      ret = "final_{}({})".format(name, args)
   
    prev_argnum = argnum

    args = ", ".join(["int " + x for x in argument_names[0:argnum]])
    functions.append(template.format(name=name, depth=depth, num = i, args = args, ret = ret))

noerror = """NOINLINE\nint \n{name}_d{depth}_{num}({args}){{
  return {ret};
}}\n\n"""

result_type = """NOINLINE\nResultType \n{name}_d{depth}_{num}({args}){{
  auto r = {ret};
  if(!r.is_some){{
    return r;
  }}
  return r;
}}\n\n"""

trivial = """NOINLINE\nTrivialResult \n{name}_d{depth}_{num}({args}){{
  auto r = {ret};
  if(!r.is_some){{
    return r;
  }}
  return r;
}}\n\n"""

depths = [2, 25, 50, 100, 200]

for depth in depths:
  generate(depth, noerror, "noerror", "int")

for depth in depths:
  generate(depth, result_type, "result", "ResultType")

for depth in depths:
  generate(depth, trivial, "trivial", "TrivialResult")

for depth in depths:
  generate(depth, noerror, "exception", "int")

random.shuffle(functions)

for f in functions:
  cpp.write(f)

for depth in depths:
  call_main(depth, "noerror")
  call_main(depth, "result")
  call_main(depth, "trivial")
  call_main(depth, "exception")
