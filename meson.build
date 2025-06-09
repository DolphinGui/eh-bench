project(
    'eh-bench',
    'cpp',
    version: '0.1',
    default_options: [
        'warning_level=3',
        'cpp_std=c++17',
        'buildtype=debugoptimized',
    ],
)

py = find_program('python3')

test_data = custom_target(
    command: [py, '@INPUT@', '@OUTPUT0@', '@OUTPUT1@', '@OUTPUT2@'],
    input: 'gen_functions.py',
    output: ['branches.cpp', 'branches.h', 'main.cpp'],
)

add_global_arguments(
    ['-save-temps=obj'],
    language: ['c', 'cpp'],
)

exe = executable(
    'eh-bench',
    'no_error.cpp',
    'result.cpp',
    'exception.cpp',
    'timing.cpp',
    test_data,
    link_args: [
        '-Wl,--gc-sections',
        '-Xlinker',
        '-Map=output.map',
    ],
)

test('benchmark', exe)