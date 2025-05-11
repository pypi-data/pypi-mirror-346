# Neural Network Engine

This neural network is built from scratch in C++ and trained using gradient descent and backpropagation. It consists of multiple dense layers, each with learnable weights and biases. The model learns to recognize patterns in data: from basic logic operations like AND/XOR to visual features like curves and edges. Over time, it builds up more complex representations. After training, it can solve problems like the XOR function or classify handwritten digits from the MNIST dataset.

---

### Datasets

- **XOR**: Simple binary classification problem to validate learning and non-linear decision boundaries.
- **MNIST**: Handwritten digit classification using 28×28 grayscale images and 10 output classes.

---

### How to Reproduce

#### Build

You can either build natively or in Docker. Note the provided Dockerfile runs valgrind, so adjust as needed to run the correct binary.

**Native Build (Mac/Linux):**

```bash
make
./NN-ab-ovo
```

**Docker (x86_64 emulation on Apple Silicon):**

```bash
docker build -t nn-ab-ovo .
docker run --rm nn-ab-ovo
```

> Make sure the MNIST dataset files (`train-images.idx3-ubyte`, `train-labels.idx1-ubyte`, etc.) are in the project root or mounted into the Docker container.

---

### Optimizations

Optimization experiments are documented in [optimizations.md](tests/optimizations.md), including but not limited to:

- Naive vs. blocked matrix multiplication
- Compiler flag benchmarking
- Cache performance profiling via Valgrind
- Timing analysis with `std::chrono`

These experiments help evaluate system-level performance and guide improvements for training/inference in C++.

---

### Project Structure

- `Matrix.hpp / Matrix.cpp`: Core matrix operations and linear algebra utilities.
- `DenseLayer.hpp / DenseLayer.cpp`: Fully connected layer with forward and backward pass.
- `Activation.hpp / Activation.cpp`: Modular support for activation functions (e.g., ReLU, LeakyReLU, Sigmoid).
- `Loss.hpp`: Interface for loss functions (e.g., MSE, CrossEntropy).
- `Sequential.hpp / Sequential.cpp`: High-level container for layer sequencing and model training.
- `tests`: Directory containing runnable code on specific datasets.

The engine is modular: activation functions, loss functions, and layers are easily swappable for flexibility and experimentation.

---

### Future Work

- [ ] Switch Design Pattern for Activation + Loss
- [ ] Switch Matrix class to use size_t + Refactor
- [ ] Better Softmax Implementation
- [ ] Continue with optimizations
- [ ] Add support for convolutional layers
- [ ] Implement GPU acceleration (Metal or CUDA)
- [ ] LLVMs?
- [ ] Add unit tests and CI/CD pipeline

---

### License

MIT License
