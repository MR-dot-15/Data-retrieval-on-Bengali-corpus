import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as st

root = r"C:\Users\rmukh\OneDrive\Desktop\Summer 21\summer_internship_21\Bengali-data"

# plain query
result_base_1 = "search_res_raw" 
# with prefix match clustering
result_base_2 = "search_res" 
# co-occurrence filtering
result_base_3 = "search_res_coocc" 
# some random changes in bm
result_base_4 = "search_res_custom_bm_2"
# new model, with linear weight on bm25
result_base_5 = "search_res_ultimate_1"
# new model with no weight on bm25
result_base_6 = "search_res_ultimate_2"
# new model with exp weight
result_base_7 = "search_res_ultimate_3"

lis = [result_base_1, result_base_2, result_base_3, result_base_6, result_base_5, result_base_7]
#lis = [result_base_1, result_base_2, result_base_3]
ap = [np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([])]
p10 = [np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([])]
index = 0
for i in lis:
    path = root + "\\eval_result\\" + "eval_" + i

    with open(path, 'rb') as f:
        dic = pickle.load(f)

    #print(dic)

    _sum = 0
    for j in dic.keys():
        ap[index] = np.append(ap[index], dic[j][2])
        ap[index] = np.append(ap[index], dic[j][1])
        _sum += dic[j][2]

    #print("MAP for ", i, _sum/49) 
    index += 1

title = [
    "Query terms with no processing",
    "With prefix match clustering",
    "Filtered variants using co-occurrence",
    "Proposed system, BM25 ranking",
    "Proposed system, BM25 and linear booster",
    "Proposed system, BM25 and exp booster"
]
""" x_ax = np.linspace(0.9, 1.1)
for i in range(1, 7):
    plt.subplot(1,6,i)
    plt.scatter(np.ones_like(ap[0]), ap[i-1], alpha = 0.5)
    plt.errorbar(1, ap[i-1].mean(), yerr = ap[0].std(), ecolor = 'k', capsize=10, barsabove=True)
    plt.plot(x_ax, ap[i-1].mean() * np.ones_like(x_ax), '--y', alpha = 0.5, label = 'mean')
    plt.xticks([])
    plt.xlim(0.9, 1.1)
    if i != 1:
        plt.yticks([])
    if i == 6:
        plt.legend()

    plt.ylabel(title[i-1])


plt.suptitle("Average Precision")
plt.grid(True, alpha = 0.3)
plt.show() """

x = st.ttest_rel(ap[0], ap[3])
print(x)