# FAE

After testing FAE exceptions, I can say that this has been an incredible success! FAE exceptions
about 5 times faster than DWARF exceptions! I largely suspect this is due to the speed of the
epilogue-based unwinding over interpreted unwind instructions, as well as the greatly simplified
format of FAE which results in faster decode times. At some point I'll have to develop flame graphs
for this, but for now I'll leave it as is.

## Caveats

Of course, FAE as is is very much a research project. It is not at all ready for production use due
to a variety of infirmities. For one, it currently does not support passing parameters for functions
via memory. This is because the stack manipulation there is not actually a part of the prologue, which
I didn't realize. Also, it currently does not support static chaining on x86, which is apparently used
for nested functions. It also doesn't support shared libraries yet.

More glaringly however, is the fact that it currently uses a linear search algorithm for searching the
exception tables. This means that the unwind time scales linearly with binary size, unlike DWARF exceptions
which construct a B-table and therefore scales at log time, or result handling which is constant time.
This would require modifying the linker in some way or implementing a linker plugin. Either way, it would
require more resources than I currently have.

## Space

Expectedly, the binary size for FAE exceptions are a little larger than their DWARF counterparts. FAE index
and data add up to 62kB, as opposed to 54kB. This is largely due to the fact that FAE uses 8 byte pointers
whereas DWARF uses 4 byte pointers. This means that FAE exception space should take up less space than DWARF
exceptions on 32 bit platforms, where space may bit a bit more lacking. FAE lsda sections however are 
significantly larger than their DWARF counterparts, being 15k as opposed to 9k. This is probably due to the
use of 16 bit integers as opposed to LEB128 integers, which was done due to the sloth of decoding LEB128.

## Further optimization

In order to further optimize FAE exceptions, a linker script was used to remove unnecessary indexes and reorder
the most commonly thrown functions to be searched first. This represents a hypothetical optimzation done by the
linker which would reorder and garbage collect FAE exceptions. This brings the speed of FAE exceptions up to about
3x slower than a normal function call. This implies that the bulk of the improvements is from FAE speeding up unwinding
rather than the search phase, which is to be expected given DWARF exceptions use a B-Table internally, which is about
optimal wheras FAE uses linear search, which is very much less than optimal.

Further hypothetical optimizations may include combining several unwinds together when the unwound callstack is known,
(exception information inlining, aka trampolining), the use of a static B-Table instead of linear search, cache warming,
index garbage collection, merging, amongst others. I will discuss exception inlining and merging due to their
relative novelity and lack of prior art.

Exception inlining, (something Khalil calls trampolining), is when the unwind information of multiple
functions known to always call eachother is concatenated to create one. In the case of a non-linear call-graph,
this may result in increased unwind information size due to duplication of caller unwind information.
Such an optimization in the case of FAE would result in restoring the saved registers from the various callframes
of the functions, then decrementing the stack by the sum of the stack usage of the callframes. This would increase
unwind speed due to a reduced need to search indicies.

Merging of exception information is an optimization where multiple functions with the same call frame are grouped together
such that their indicies and unwind information can be merged. This could greatly reduce space usage at the minor cost
of questionably penalizing instruction locality. This would almost certainly have to be done via a linker plugin or
in the linker itself. This increases speed by reducing index search time and increases space efficiency.
