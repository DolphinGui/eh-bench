#include "functions.h"
#include "picobench.hpp"

picobench::state *global_timer = nullptr;

void start_timing() { global_timer->start_timer(); }