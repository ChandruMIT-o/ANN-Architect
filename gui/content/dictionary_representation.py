class CONSTANTS:
    def __init__(self) -> None:
        self.LAYER_INFO = {
            "DENSE_LAYER": {
                "basic": {
                    "units": {
                        "type": "integer_input",
                        "structure": "linear",
                        "options": ["NXN", "NXNXN", "N"]  # where n is a natural number
                    },
                    "activation": {
                        "type": "dropdown",
                        "structure": "linear",
                        "options": ["linear(default)", "ReLu", "Sigmoid", "tanh", "softmax", "softplus", "softsign", "selu", "elu", "exponential"]
                    },
                    "kernel_initializer": {
                        "type": "dropdown",
                        "structure": "linear",
                        "options": ["zeros(default)", "ones", "glorot_uniform", "glorot_normal", "he_normal", "he_uniform", "random_uniform", "random_normal", "truncated_normal", "orthogonal", "identity", "lecun_normal", "lecun_uniform", "variance_scaling"]
                    },
                    "kernel_regularizer": {
                        "type": "dropdown",
                        "structure": "nested",
                        "options" : {
                            "l1" : {
                                "lambda" : "float_input",
                            },
                            "l2" : {
                                "lambda" : "float_input",
                            },
                            "l1 & l2" : {
                                "lambda1" : "float_input",
                                "lambda2" : "float_input",
                            }
                        }
                    }
                },
                "advanced": {
                    "use_bias": {
                        "type": "toggle",
                        "structure": "linear",
                        "options": [True, False]
                    },
                    "bias_initializer": {
                        "type": "dropdown",
                        "structure": "linear",
                        "options": ["zeros(default)", "ones", "glorot_uniform", "glorot_normal", "he_normal", "he_uniform", "random_uniform", "random_normal", "truncated_normal", "lecun_normal", "lecun_uniform", "constant"]
                    },
                    "bias_regularizer": {
                        "type": "dropdown_float_input",
                        "structure": "nested",
                        "options": [
                            ["l1", ["lambda"]],
                            ["l2", ["lambda"]],
                            ["l1&l2", ["lambda1", "lambda2"]]
                        ]
                    },
                    "kernel_constraint": {
                        "type": "dropdown_float_input",
                        "structure": "nested",
                        "options": [
                            ["non_neg", []],
                            ["unit_norm", []],
                            ["identity", []],
                            ["max_norm", ["value"]],
                            ["min_max_norm", ["value1", "value2"]]
                        ]
                    },
                    "bias_constraint": {
                        "type": "dropdown_float_input",
                        "structure": "nested",
                        "options": [
                            ["non_neg", []],
                            ["unit_norm", []],
                            ["identity", []],
                            ["max_norm", ["value"]],
                            ["min_max_norm", ["value1", "value2"]]
                        ]
                    },
                    "activity_regularizer": {
                        "type": "dropdown_float_input",
                        "structure": "nested",
                        "options": [
                            ["l1", ["lambda"]],
                            ["l2", ["lambda"]],
                            ["l1&l2", ["lambda1", "lambda2"]]
                        ]
                    }
                }
            },
            "otherwise": dict()
        }