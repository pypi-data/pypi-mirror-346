from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
import os
import glob
import platform
import sys

sources = ["pybind/bindings.cpp"] + glob.glob("src/nn/*.cpp") + glob.glob("src/nn/activation/*.cpp") + glob.glob("src/nn/loss/*.cpp") + glob.glob("src/nn/matmul/*.cpp") + glob.glob("src/nn/quantization/*.cpp")

# Set compiler flags based on the platform
extra_compile_args = ["-std=c++17"]  # Always use C++17
extra_link_args = []
define_macros = []

# Remove multi-architecture flags that cause issues
extra_compile_args.append("-arch")
if platform.machine() == 'arm64':
    extra_compile_args.append("arm64")
else:
    extra_compile_args.append("x86_64")

# Detect CPU architecture
is_arm = platform.machine() == 'arm64'
# Better ARM detection for macOS
if is_arm:
    if platform.system() == "Darwin":  # macOS ARM
        define_macros.append(('USE_ARM_NEON', '1'))
        # No need for float-abi flag on macOS
    elif platform.system() == "Linux":  # Linux ARM
        define_macros.append(('USE_ARM_NEON', '1'))
        extra_compile_args.append("-mfloat-abi=hard")  # Only on Linux ARM
else:
    # Disable NEON for x86
    define_macros.append(('NO_ARM_NEON', '1'))

# macOS specific settings
if platform.system() == "Darwin":  # macOS
    # Check if using Homebrew LLVM/Clang
    homebrew_prefix = "/opt/homebrew" if os.path.exists("/opt/homebrew") else "/usr/local"
    llvm_path = os.path.join(homebrew_prefix, "opt/llvm")
    libomp_path = os.path.join(homebrew_prefix, "opt/libomp")
    
    if os.path.exists(libomp_path):
        # Add OpenMP support
        extra_compile_args.extend([
            "-Xpreprocessor", 
            "-fopenmp", 
            f"-I{libomp_path}/include"
        ])
        extra_link_args.extend([
            f"-L{libomp_path}/lib", 
            "-lomp"
        ])
    else:
        # Fallback: disable OpenMP if libomp not available
        define_macros.append(('NO_OPENMP', '1'))
        print("WARNING: libomp not found. Building without OpenMP support.")
        print("To enable OpenMP, install libomp: brew install libomp")
elif platform.system() == "Linux":
    # Linux settings
    extra_compile_args.append("-fopenmp")
    extra_link_args.append("-fopenmp")
elif platform.system() == "Windows":
    # Windows settings (assuming MSVC compiler)
    extra_compile_args = ["/std:c++17", "/openmp"]
    extra_link_args = []

abovo_ext = Pybind11Extension(
    "_abovo",
    sources=sources,
    include_dirs=["include"],
    define_macros=define_macros,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args
)

setup(
    name="abovo",
    version="0.1.0",
    description="A C++ neural network engine with Python bindings, designed for educational performance optimization.",
    long_description=open("README-pypi.md").read(),
    long_description_content_type="text/markdown",
    ext_modules=[abovo_ext],
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C++",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=["abovo"],
    include_package_data=True,
)