import math

#--------- Mean -----------
def mean(values):
    values = list(values)
    return sum(values) / len(values) if values else 0  # return mean if not empty else 0


#--------- Median ----------
def median(values):
    values = sorted(values)
    length = len(values)

    if length == 0:
        return 0
    
    mid = length // 2
    if length % 2 == 1:  # length is odd number 
        return values[mid]
    else:
        return (values[mid - 1 ] + values[mid]) / 2
    

#--------- Variance ---------
def variance(values):
    values = list(values)
    if len(values) == 0:
        return 0

    m = mean(values)   
    squared_diffs = map(lambda v: (v - m) ** 2, values)
    return sum(squared_diffs) / len(values)

#----------- Summaries ---------
def summaries(records, fields):
    extract_values = lambda field: list(
        map(float,
            filter(lambda v: v not in ("", None),
                   map(lambda r: r.get(field), records)))
    )
# records = [
#     {"Price": 10, "Quantity": 3},
#     {"Price": 15, "Quantity": 5},
#     {"Price": "", "Quantity": 2},
# ]
# list(map(lambda r: r.get("Price"), records))
# # Output: [10, 15, '']
# Output: [10.0, 15.0]

    compute_summary = lambda field: {
        "mean": mean(extract_values(field)),
        "median": median(extract_values(field)),
        "variance": variance(extract_values(field))
    }

    return dict(map(lambda f: (f, compute_summary(f)), fields)) # build dictionary for all fields 




#----------- Correlation ---------
def correlation(values_x, values_y):
    x = list(values_x)
    y = list(values_y)

    if not x or len(x) != len(y):
        return 0
    
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)

    # numerator: sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    numerator = sum(map(lambda pair: (pair[0] - mean_x) * (pair[1] - mean_y),
                        zip(x, y)))
    # denominator: sqrt(sum((xi - mean_x)^2) * sum((yi - mean_y)^2))
    sum_sq_x = sum(map(lambda xi: (xi - mean_x) ** 2, x))
    sum_sq_y = sum(map(lambda yi: (yi - mean_y) ** 2, y))
    denominator = math.sqrt(sum_sq_x * sum_sq_y)

    return numerator / denominator if denominator != 0 else 0

#----- trend analysis -----------------
def compute_trend(values):
    values = list(values)
    if len(values) < 2:
        return []

    # Zip each value with its previous value
    pairs = zip(values[:-1], values[1:]) # all value except the last , all value except the first

    # [15, 20, 33 ] -> (10, 20) -> (20-15)/15 = 0.33 , then complete the list : 0.33 , 0.65,....
    return list(map(lambda pair: (pair[1] - pair[0]) / pair[0] if pair[0] != 0 else 0, pairs))



