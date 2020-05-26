from collections import defaultdict
from scipy.stats import gaussian_kde
import csv
import scipy
import unittest
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

class Covid_Statistics:

    def __init__(self):
        self.parced = defaultdict(list)

    def parcer(self, source, country):
        with open(source) as data:
            file = csv.DictReader(data)
            for line in file:
                for key in line:
                    if line[key] == country:
                        for item in line:
                            if item not in ('iso_code', 'location', 'date'):
                                if line[item] not in ('', 'inconsistent units (COVID Tracking Project)', 'people tested',
                                                      'samples tested', 'tests performed', 'units unclear'):
                                    self.parced[item].append(float(line[item]))
                            else:
                                self.parced[item].append(line[item])

    def keys(self):
        return self.parced.keys()

    def sample_mean(self, key):
        if type(self.parced[key][0]) is str:
            raise Exception('Data is string, not numbers!')
        return sum(self.parced[key]) / (len(self.parced[key]))

    def sample_variance(self, key):
        if type(self.parced[key][0]) is str:
            raise Exception('Data is string, not numbers!')
        return sum([(self.parced[key][i] - (sum(self.parced[key])) / len(self.parced[key])) ** 2 for i in range(len(self.parced[key]))]) / len(self.parced[key])


    def quantile(self, key, k):
        if type(self.parced[key][0]) is str:
            raise Exception('Data is string, not numbers!')
        return sorted(self.parced[key])[int((len(self.parced[key]) - 1) * k)]


    def emp_distr_func(self, key):
        if type(self.parced[key][0]) is str:
            raise Exception('Data is string, not numbers!')
        levels = np.linspace(0, 1, len(self.parced[key]))
        plt.title(key)
        plt.xlabel('values')
        plt.ylabel('probability')
        plt.step(sorted(self.parced[key]), levels)
        plt.show()

    def histogram(self, key):
        if type(self.parced[key][0]) is str:
            raise Exception('Data is string, not numbers!')
        plt.title(key)
        plt.xlabel('values')
        plt.ylabel('probability')
        plt.hist(self.parced[key])
        plt.show()

    def kde(self, key):
        if type(self.parced[key][0]) is str:
            raise Exception('Data is string, not numbers!')
        density = gaussian_kde(self.parced[key])
        xs = np.linspace(0, 1000, 100)
        density.covariance_factor = lambda: .25
        density._compute_covariance()
        plt.xlabel('values')
        plt.ylabel('probability')
        plt.title(key)
        plt.plot(xs, density(xs))
        plt.show()

    def confid_int(self, key, sides, percent):
        if type(self.parced[key][0]) is str:
            raise Exception('Data is string, not numbers!')
        n = len(self.parced[key])
        m = np.mean(self.parced[key])
        se = scipy.stats.sem(self.parced[key])
        h = se * scipy.stats.t.ppf((1 + percent) / 2, n - 1)
        if sides == 'left':
            return sides, percent, m - h
        if sides == 'right':
            return sides, percent, m + h
        if sides == 'both':
            return sides, percent, m - h, m + h

test = Covid_Statistics()

test.parcer(r'C:/Users/HP/Desktop/covid_statistics.csv', 'RUS')
key = 'total_deaths'
print('---keys---', test.keys())
print('---sample_mean---', test.sample_mean(key))
print('---sample_variance---', test.sample_variance(key))
print('---quantile---', test.quantile(key, 0.7))
test.emp_distr_func(key)
test.histogram(key)
test.kde(key)
print('---confid_int---', test.confid_int(key, 'both', 0.95))

class Test_Covid_Statistics(unittest.TestCase):

    def test_sample_mean(self):
        self.assertEqual(test.sample_mean('list'), 3)

    def test_sample_variance(self):
        self.assertEqual(test.sample_variance('list'), 2)

    def test_quantile(self):
        self.assertEqual(test.quantile('list', 0.5), 3)

#if __name__ == '__main__':
#    test = Covid_Statistics()
#    test.parced['list'].extend([1, 2, 3, 4, 5])
#    unittest.main(verbosity=2)
