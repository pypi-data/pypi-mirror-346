from concurrent.futures import ThreadPoolExecutor


def eval(func, points):
    try:
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(func, points))
        return results
    except AttributeError:
        raise "Your model dont have a parallel mode"
