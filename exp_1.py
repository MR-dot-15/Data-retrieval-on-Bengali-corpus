import relevant_func as rf
import numpy as np
import matplotlib.pyplot as plt
import pickle

with open('term_database_dict', 'rb') as inf:
    term_db = pickle.load(inf)

words = list(term_db.keys())
term = 'মিনা'
lis = []
co_occ = np.array([])

for word in words:
    (intersect, value) = rf.find_intersect(term, word, prefix_length = 0)
    
    if value == 1:
        lis = np.append(lis, word)
        co_occ_val, occ_val, tot = rf.coocc_val(term, word, term_db)

        try:
            relative = len(term_db[intersect][:,0])/tot
            booster = np.tanh(relative-1) + 1
        except:
            booster = 0

        #val = 1000*(co_occ_val**2/(occ_val * tot)) * booster * len(intersect)
        val = (co_occ_val**2/(occ_val * tot))

        co_occ = np.append(co_occ, val)

# index of words in lis
index_array = np.arange(len(co_occ))
# co occurrence values > 0
co_occ_g0 = co_occ[co_occ>0]
# index of words having >0 coocc
index_g0 = index_array[co_occ>0]

if len(index_g0) <= 5:
    print([lis[i] for i in index_g0])

# sort_index of co_occ_g0
ind = np.argsort(co_occ_g0)
co_occ_g0_sorted = co_occ_g0[ind][:-1]
index_g0_sorted = index_g0[ind][:-1]

lim = co_occ_g0_sorted[-1]
x = np.linspace(0, lim)

y_mean = np.mean(co_occ_g0_sorted)
y_var = np.std(co_occ_g0_sorted)

y_mod = np.tanh((co_occ_g0_sorted - y_mean)/y_var)
ref_lis = []

classified_ind = index_g0_sorted[abs(y_mod-1)<0.3]
for i in classified_ind:
    ref_lis.append(lis[int(i)])

func = np.tanh((x - y_mean)/y_var)

print(ref_lis[-5:])

plt.grid(True, alpha = 0.3)
plt.scatter(co_occ_g0_sorted, np.zeros_like(co_occ_g0_sorted), label = "ρ value with booster")
plt.plot(x, func, '--c', alpha = 0.5, label = "clustering function")
plt.plot(x, 0.7 * np.ones_like(x), '--r', alpha = 0.4, label = "threshold")
plt.scatter(co_occ_g0_sorted, y_mod, label = "ρ times booster clustered")
plt.ylim(-1.2, 1.2)
plt.legend(loc = 'lower right')
plt.show()
