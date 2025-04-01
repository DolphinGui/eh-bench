project(
    'eh-bench',
    'cpp',
    version: '0.1',
    default_options: ['warning_level=3', 'cpp_std=c++14'],
)

exe = executable(
    'eh-bench',
    'main.cpp',
    'nanobench.cpp',
    'no_error.cpp',
    'clobber.cpp','result.cpp',
)

test('basic', exe)
