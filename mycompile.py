import os
from distutils.core import setup
py_files = [] # 用来存储所有的py文件路径
for root, dirs, files in os.walk('./'):
    for file in files:
        if file.endswith('.py') and file != '__init__.py':
            py_files.append(os.path.join(root, file).replace('./', ''))
            #py_files.append(os.path.abspath(os.path.join(root, file)))
from setuptools import Extension
from Cython.Build import cythonize
commands = [] # 用来存储所有的编译命令
for py_file in py_files:
    print(py_file)
    module_name = py_file.replace("\\", ".").replace("/", ".").replace(".py", "")
    ext = Extension(module_name, [py_file])
    #ext_modules=cythonize(ext, language_level=3)
    setup(ext_modules=cythonize(ext, language_level=3,options={"build_ext": {"suffix": ".so"}}))
# with open('compile_commands.txt', 'w') as f:
#     for command in commands:
#         f.write(command + '\n')
'''

'''


import os
py_files = [] # 用来存储所有的py文件路径
for root, dirs, files in os.walk('./'):
    for file in files:
        if file.endswith('.py') and file != '__init__.py':
            py_files.append(os.path.join(root, file).replace('./', ''))

env_path = 'D:\\ProgramData\\anaconda3\\envs\\pytorch13\\include\\' # 您的虚拟环境路径
commands = [] # 用来存储所有的编译命令
for py_file in py_files:
    module_name = py_file.replace('.py', '')
    command = """
#rm {module_name}.so
cython {py_file}
gcc -c -fPIC -I {env_path} {module_name}.c
gcc -shared {module_name}.o -o {module_name}.so
#rm {py_file} {module_name}.o {module_name}.c
""".format(module_name=module_name, py_file=py_file, env_path='${env_path}')
    commands.append(command)

with open('compile_commands.txt', 'w') as f:
    for command in commands:
        f.write(command + '\n')
'''

'''

# import os
# from distutils.core import setup
# from distutils.extension import Extension
# from Cython.Build import cythonize
#
# # Recursively find all .py files in the current directory and its subdirectories
# def find_py_files():
#     py_files = []
#     for root, dirs, files in os.walk('.'):
#         for file in files:
#             if file.endswith('.py'):
#                 py_files.append(os.path.join(root, file))
#     return py_files
#
# # Compile each .py file into a .so file
# for py_file in find_py_files():
#     module_name = os.path.splitext(py_file)[0].replace(os.sep, '.')
#     extensions = [Extension(module_name, [py_file])]
#     setup(ext_modules=cythonize(extensions))