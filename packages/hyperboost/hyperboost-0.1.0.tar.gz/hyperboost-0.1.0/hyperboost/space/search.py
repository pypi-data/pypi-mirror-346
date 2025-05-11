import numpy as np

class SearchSpace:
    def __init__(self, space_dict):
        self.space_dict = space_dict
        self.param_names = list(space_dict.keys())
        self.param_objs = list(space_dict.values())

    def sample(self, n=1):
        samples = []
        for _ in range(n):
            point = {}
            for name, param in zip(self.param_names, self.param_objs):
                point[name] = param.sample()[0]
            samples.append(point)
        return samples

    def transform(self, params):
        vec = []
        for name in self.param_names:
            val = params[name]
            param_obj = self.space_dict[name]
            vec.append(param_obj.transform(val))
        return np.array(vec)

    def inverse_transform(self, vector):
        params = {}
        for i, name in enumerate(self.param_names):
            param_obj = self.space_dict[name]
            params[name] = param_obj.inverse_transform(vector[i])
        return params