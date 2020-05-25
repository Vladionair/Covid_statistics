from collections import defaultdict
import csv
import unittest
import matplotlib

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
        return sum(self.parced[key]) / (len(self.parced[key]))

    def sample_variance(self, key):
        return sum([(self.parced[key][i] - (sum(self.parced[key])) / len(self.parced[key])) ** 2 for i in range(len(self.parced[key]))]) / len(self.parced[key])

    def quantile(self, key, k):
        return sorted(self.parced[key])[int((len(self.parced[key])-1) * k)]

    def emp_distr_func(self, key):
        return [self.parced[key].count(i) / len(set(self.parced[key])) for i in self.parced[key]]

    def histogram(self, key, n):
        steps = [(max(self.parced[key])-min(self.parced[key]))*(col/(n-1)) for col in range(1, n)]
        limit = 0
        result = []
        for i in range(len(steps)):
            for j in range(limit, len(self.parced[key])):
                if self.parced[key][j] > steps[i]:
                    result.append(self.parced[key][limit:j])
                    limit = j
                    break
        result.append(self.parced[key][limit:])
        return [len(result[i])/len(self.parced[key]) for i in range(len(result))]

#test = Covid_Statistics()
#test.parcer(r'C:\Users\HP\Desktop\covid_stat.csv', 'RUS')

class Test_Covid_Statistics(unittest.TestCase):

    def test_sample_mean(self):
        self.assertEqual(test.sample_mean(list), 3)

    def test_sample_variance(self):
        self.assertEqual(test.sample_variance(list), 2)

    def test_quantile(self):
        self.assertEqual(test.quantile(list, 0.5), 3)

    def test_emp_distr_func(self):
        self.assertEqual(test.emp_distr_func(list), [0.2, 0.2, 0.2, 0.2, 0.2])

    def test_histogram(self):
        self.assertEqual(test.histogram(list, 5), [0.2, 0.2, 0.2, 0.2, 0.2])

if __name__ == '__main__':
    test = Covid_Statistics()
    test.parced[list].extend([1, 2, 3, 4, 5])
    unittest.main(verbosity=2)

