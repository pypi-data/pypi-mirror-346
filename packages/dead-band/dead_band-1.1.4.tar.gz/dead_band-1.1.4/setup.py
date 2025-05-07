from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

extensions = [
    Extension(
        name="dead_band.cython_modules.c_deadband",
        sources=["src/dead_band/cython_modules/c_deadband.pyx"],
        extra_compile_args=["-O3"],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    )
]

setup(
    name="dead-band",
    ext_modules=cythonize(extensions, language_level="3"),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)