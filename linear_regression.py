def averages(data_points):
    x_sum = 0
    y_sum = 0
    for x, y in data_points:
        x_sum += x
        y_sum += y
    x_avg = x_sum / len(data_points)
    y_avg = y_sum / len(data_points)
    return x_avg, y_avg


def gradient(data_points, avgs=None):
    if avgs == None:
        avgs = averages(data_points)
    x_avg, y_avg = avgs
    numerator = 0
    denominator = 0
    for x, y in data_points:
        x_deviation = x - x_avg
        y_deviation = y - y_avg
        numerator += x_deviation * y_deviation
        denominator += x_deviation * x_deviation
    if denominator == 0:
        return float('+inf')
    return numerator / denominator


def y_intercept(data_points, avgs=None, grad=None):
    if avgs == None:
        avgs = averages(data_points)
    x_avg, y_avg = avgs
    if gradient == None:
        grad = gradient(data_points, avgs)
    return y_avg - grad * x_avg


def predict_function(data_points, avgs=None, grad=None, y_cept=None):
    if grad == None:
        grad = gradient(data_points, avgs)
    if y_cept == None:
        y_cept = y_intercept(data_points, avgs, grad)
    return lambda x: y_cept + grad * x


def square_error(data_points, avgs=None, grad=None, y_cept=None, predict_func=None):
    if predict_func == None:
        predict_func = predict_function(data_points, avgs, grad, y_cept)
    sum = 0
    for x, y in data_points:
        sum += (y - predict_func(x)) ** 2
    return sum
