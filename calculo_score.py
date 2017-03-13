import numpy as np
import csv
import math


reader = csv.reader(open("Base de Datos 1/tic_training_modified.csv"))
x = list(reader)
insurance_data = np.array(x).astype("float")

# Distribution of our data
Y = insurance_data[:, 85]
X = insurance_data[:, 0:85]

# Compute Nc = 1, Nc = 0
Nc1 = np.count_nonzero(Y == 1)
Nc0 = np.count_nonzero(Y == 0)

# Obtain the MAP categorical parameters
insurance_parameters = []
for feature in range(85):
    insurance_parameters.append({x: [] for x in np.unique(X.T[feature, :]).tolist()})

# First and second value in value list correspond to C = 1 and C = 0 respectively
counter_0 = 0
counter_1 = 0

for dictionary in insurance_parameters:
    for key, value in dictionary.items():
        for element in range(X.T.shape[1]):
            if X.T[insurance_parameters.index(dictionary), element] == key and Y[element] == 1:
                counter_1 += 1
            elif X.T[insurance_parameters.index(dictionary), element] == key and Y[element] == 0:
                counter_0 += 1
        value.append(counter_1 / Nc1)
        value.append(counter_0 / Nc0)
        counter_1 = 0
        counter_0 = 0

# Create the test matrix (X1)
reader1 = csv.reader(open("Base de Datos 1/tic_test_modified.csv"))
x1 = list(reader1)
insurance_data_test = np.array(x1).astype("float")

X1 = insurance_data_test[:, 0:85]

# Calculate score
score = []
score_bin = []

counter = 0
score_Num = 1
score_den = 1

for row in X1:
    for element in row:
        if element in insurance_parameters[counter]:
            value1, value2 = insurance_parameters[counter][element]
        else:
            value1, value2 = 0, 0
        score_Num *= value1
        score_den *= value2
        counter += 1
    if score_den == 0 and score_Num != 0:
        score.append(15)
    elif score_Num == 0 and score_den != 0:
        score.append(-15)
    elif score_den == 0 and score_Num == 0:
        score.append(0)
    else:
        score.append(math.log(score_Num/score_den))
    counter = 0
    score_den = 1
    score_Num = 1

print(score)

for x in score:
    if x == 'Error':
        score_bin.append(0)
    elif x > 0:
        score_bin.append(1)
    else:
        score_bin.append(0)

print(score_bin)

Y1 = insurance_data_test[:, 85]

success = 0
success0 = 0
success1 = 0

for x in range(4000):
    if score_bin[x] == Y1[x]:
        success += 1
        if score_bin[x] == 1:
            success1 += 1
        else:
            success0 += 1

# Number of ones and zeroes in Y
ones = 0
zeroes = 0

for x in Y1:
    if x == 1:
        ones += 1
    else:
        zeroes += 1

print('Numero Aciertos: ', success)
print('Porcertaje Aciertos: ', success / 4000)
print('Aciertos Unos: ', success1 / ones)
print('Aciertos Ceros: ', success0 / zeroes)

np.savetxt('resultado_bin.txt', np.array(score_bin))
np.savetxt('resultado.txt', np.array(score))





