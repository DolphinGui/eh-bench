project(
    'eh-bench',
    'cpp',
    version: '0.1',
    default_options: ['warning_level=3', 'cpp_std=c++17'],
)

py = find_program('python3')

test_data = custom_target(
    command: [py, '@INPUT@', '@OUTPUT0@', '@OUTPUT1@', '@OUTPUT2@'],
    input: 'gen_functions.py',
    output: ['branches.cpp', 'branches.h', 'main.cpp'],
)

gbench = dependency('benchmark-main')

exe = executable(
    'eh-bench',
    'no_error.cpp',
    'result.cpp',
    'exception.cpp',
    'trivial.cpp',
    test_data,
    cpp_args: ['-ffunction-sections', '-fdata-sections'],
    link_args: ['-Xlinker', '-Map=output.map'],
    dependencies: [gbench]
)

test('benchmark', exe)