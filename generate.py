#!/bin/python3

import random

argument_names = ["a", "b", "c" ,"d", "e", "f", "g"]
arguments = ["int a = 0", "int b = 1","int c = 2","int d = 3","int e = 4","int f = 5","int g = 6"]

def generate_noerror(depth):
  for i in reversed(range(depth)):
    argnum = random.randint(0, 6)
    arrsize = random.randint(0, 24)
    clobber = ["\"+m\"({})".format(r) for r in argument_names[0:argnum]]
    if arrsize > 0:
      arr = "char stack[{}]".format(arrsize)
      clobber.append("\"=m\"(stack)")
    else:
      arr = ""
    clobber = ", ".join(clobber) 

    if i != depth - 1:
      ret = "return f{}()".format(i + 1);
    else:
      ret = "return final_noerror()"
   
    print("""[[gnu::noinline]]int f{num}({args}){{
    {stack};
    asm volatile(\"\" : {asm} :: "memory");
    {ret}
    }}""".format(num = i, args = ", ".join(arguments[0:argnum]), stack = arr, asm = clobber, ret = ret))


generate_noerror(20)


