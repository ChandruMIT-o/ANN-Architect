dense_layer = {
    'basic': {
        'units': ['integer_input', ["NXN", "NXNXN", "N"]],  # where n is natural number
        'activation': ['dropdown', ["linear(default)", "ReLu", "Sigmoid", "tanh", "softmax", "softplus", "softsign", "selu", "elu", "exponential"]],
        'kernel_initializer': ['dropdown', ["zeros(default)", "ones", "glorot_uniform", "glorot_normal", "he_normal", "he_uniform", "random_uniform", "random_normal", "truncated_normal", "orthogonal","identity", "lecun_normal", "lecun_uniform", "variance_scaling"]],
        'kernel_regularizer': ['dropdown_float_input', [["l1", ["lambda"]], ["l2", ["lambda"]], ["l1&l2", ["lambda1", "lambda2"]]]]
    },
    'advanced': {
        'use_bias': ['toggle', [True, False]],
        'bias_initializer': ['dropdown', ["zeros(default)", "ones", "glorot_uniform", "glorot_normal", "he_normal", "he_uniform", "random_uniform", "random_normal", "truncated_normal", "lecun_normal", "lecun_uniform", "constant"]],
        'bias_regularizer': ['dropdown_float_input', [["l1", ["lambda"]], ["l2", ["lambda"]], ["l1&l2", ["lambda1", "lambda2"]]]],
        'kernel_constraint': [['dropdown_float_input', [["non_neg", []], ["unit_norm", []], ["identity", []], ["max_norm", ["value"]], ["min_max_norm", ["value1", "value2"]]]]],
        'bias_constraint': [['dropdown_float_input', [["non_neg", []], ["unit_norm", []], ["identity", []], ["max_norm", ["value"]], ["min_max_norm", ["value1", "value2"]]]]],
        'activity_regularizer': ['dropdown_float_input', [["l1", ["lambda"]], ["l2", ["lambda"]], ["l1&l2", ["lambda1", "lambda2"]]]]
    }
}