#ifndef LOSS_HPP
#define LOSS_HPP

#include "Matrix.hpp"

namespace nn {

enum class LossType {
    MSE,
    CROSS_ENTROPY,
};

class Loss {
public:
    double loss(const Matrix& y_pred, const Matrix& y_true, LossType type) const;
    Matrix loss_derivative(const Matrix& y_pred, const Matrix& y_true, LossType type) const;
};

}
#endif