import numpy

from architecture_utils import initializer


class AHP:

    @initializer
    def __init__(self, method, precision, alternatives, criteria, sub_criteria, matrix, log=False):
        self.global_priorities = []

    @staticmethod
    def approach(matrix, precision):
        columns_sum = matrix.sum(axis=0)
        normalized_matrix = numpy.divide(matrix, columns_sum)
        line_medium = normalized_matrix.mean(axis=1)

        return line_medium.round(precision)

    @staticmethod
    def geometric(matrix, precision):
        medium = [numpy.prod(line ** (1 / len(line))) for line in matrix]
        normalized_medium = medium / sum(medium)

        return normalized_medium.round(precision)

    @staticmethod
    def high_value(matrix, precision, iteration=100, before_autovector=None):
        square_matrix = numpy.linalg.matrix_power(matrix, 2)
        lines_sum = numpy.sum(square_matrix, axis=1)
        columns_sum = numpy.sum(lines_sum, axis=0)
        actual_autovector = numpy.divide(lines_sum, columns_sum)

        if before_autovector is None:
            before_autovector = numpy.zeros(matrix.shape[0])
        
        difference = numpy.subtract(actual_autovector, before_autovector).round(precision)

        if not numpy.any(difference):
            return actual_autovector.round(precision)
        
        iteration -= 1

        if iteration > 0:
            return AHP.high_value(square_matrix, precision, iteration, actual_autovector)
        else:
            return actual_autovector.round(precision)
    
    @staticmethod
    def consistency(matrix):
        if matrix.shape[0] and matrix.shape[1] > 2:
            lambda_max = numpy.real(numpy.linalg.eigvals(matrix).max())
            consistency_index = (lambda_max - len(matrix)) / (len(matrix) - 1)
            random_indexes = {3: 0.52, 4: 0.89, 5: 1.11,
                              6: 1.25, 7: 1.35, 8: 1.40,
                              9: 1.45, 10: 1.49, 11: 1.52,
                              1: 1.54, 13: 1.56, 14: 1.58,
                              15: 1.59}
            consistency_ratio = consistency_index / random_indexes[(len(matrix))]

        else:
            lambda_max = 0
            consistency_index = 0
            consistency_ratio = 0
        
        return lambda_max, consistency_index, consistency_ratio
    
    def local_priorities(self):
        local_priorities_vector = {}

        for criteria in self.matrix:
            new_matrix = numpy.array(self.matrix[criteria])

            if self.method == 'approach':
                local_priorities = self.approach(new_matrix, self.precision)

            elif self.method == 'geometric':
                local_priorities = self.geometric(new_matrix, self.precision)

            else:
                if new_matrix.shape[0] and new_matrix.shape[1] >= 2:
                    local_priorities = self.high_value(new_matrix, self.precision)
                else:
                    local_priorities = self.approach(new_matrix, self.precision)
            
            local_priorities_vector[criteria] = local_priorities
            lambda_max, consistency_index, consistency_ratio = self.consistency(new_matrix)

            if self.log:
                print(f'\nPrioridades locais do criterio {criteria}: {local_priorities}')        
                print('Soma: ', numpy.round(numpy.sum(local_priorities), self.precision))
                print('Lambda max: ', lambda_max)
                print(f'Indice de consistencia {criteria} = {round(consistency_index, self.precision)}')
                print(f'Razão de consistencia {criteria} = {round(consistency_ratio, 2)}')

if __name__ == "__main__":
    matrix = [[1, 6, 3],
              [1/6, 1, 1/2],
              [1/3, 2, 1]]
    matrix = numpy.array(matrix)
    precision = 2

    print('Aproximado: ', AHP.approach(matrix, precision))
    print('Geometrico:', AHP.geometric(matrix, precision))
    print('Auto valor: ', AHP.high_value(matrix, precision))
    print('Consistencia: ', AHP.consistency(matrix))
