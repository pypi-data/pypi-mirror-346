# Abovo

**Abovo** is a C++ neural network engine with Python bindings, designed as an educational library to demonstrate systems-level performance optimizations.

Built from scratch with modular layers, customizable training, and optimized execution, Abovo gives students and performance-focused developers a hands-on learning platform for matrix computation, backpropagation, and acceleration techniques.

> Note that this is meant to be used as an educational platform and has not been tested to be used as a production-grade package.

## Features

- C++ backend with pybind11 Python bindings
- Modular dense layers with activation and loss support
- Optimizations: ARM NEON SIMD, OpenMP multithreading, cache blocking
- Quantization-aware training (FP32 → INT8)
- Pythonic API via `Sequential`, `DenseLayer`, `Matrix`
- Profiling-ready (Valgrind, cache misses, instruction counts)
- And much more to come...

## Installation

```bash
pip install abovo
```

> Requires a C++17-compatible compiler and OpenMP support.

## Example (XOR)

```python
from abovo import Sequential, DenseLayer, Matrix, ActivationType, LossType

X = Matrix(4, 2)
X[0, 0] = 0; X[0, 1] = 0
X[1, 0] = 0; X[1, 1] = 1
X[2, 0] = 1; X[2, 1] = 0
X[3, 0] = 1; X[3, 1] = 1

y = Matrix(4, 1)
y[0, 0] = 0
y[1, 0] = 1
y[2, 0] = 1
y[3, 0] = 0

model = Sequential()
model.add(DenseLayer(2, 4, ActivationType.RELU))
model.add(DenseLayer(4, 1, ActivationType.SIGMOID))
model.train(X, y, epochs=100, batch_size=1, learning_rate=0.1, loss_type=LossType.MSE)
```

## Why “ab ovo”?

_"From the egg" — the library was built from the ground up, with performance and pedagogy in mind._

## Documentation

Full documentation is available at [https://nn-ab-ovo.readthedocs.io/](https://nn-ab-ovo.readthedocs.io/).

## License

MIT
