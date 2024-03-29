sigma='(30.18* 10 ^ -3)'
m = '(7.3* 10 ^ -3)'
l = '0.1'
f='0.43'

z = f'({m}/(4*{sigma}))*(9.8 - {f}/{m}-4*{sigma}*{l}/{m})'

n1 = f'((-k + (k ^2 - 16 * {m} * {sigma}) ^ 0.5)/ (2 * {m}))'
n2 = f'((-k - (k ^2 - 16 * {m} * {sigma}) ^ 0.5)/ (2 * {m}))'
c1 = f'({z}/({n1}/{n2}-1))'
c2 = f'({z}/({n2}/{n1} -1))'
r = f'({c1}*exp({n1}*x) + {c2}*exp({n2}*x) - {z})'
print(r)