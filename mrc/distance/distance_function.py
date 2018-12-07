

def distance_function_with_params(x, a, b, c, d):
    return a * x ** 4 + b * x ** 3 + c * x ** 2 + d * x
    # return a * x ** 4 + b * x ** 3 + c * x ** 2 + (np.pi / 2 - a - b - c) * x


def get_distance_function(coef):
    def distance_function(x):
        return distance_function_with_params(x, *coef)
    return distance_function
