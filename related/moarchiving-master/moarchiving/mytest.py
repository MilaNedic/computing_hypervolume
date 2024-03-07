""" 
A collection of self-made test for testing the working of the Biobjective nondominated sorted list class
"""

from moarchiving import BiobjectiveNondominatedSortedList
mylist = [[1, 0.9], [0, 1], [0, 2]]
a1 = BiobjectiveNondominatedSortedList(mylist)
print(a1)
a1.add([0,1])
print(a1) #doesn't change anything


mylist2 = [[-0.749, -1.188], [-0.557, 1.1076], [0.2454, 0.4724], [-1.146, -0.110]]
a2 = BiobjectiveNondominatedSortedList(mylist2)
print(a2)

a1._asserts() # consistency asserts
a2._asserts()

nda = BiobjectiveNondominatedSortedList([[2, 3]])
f_pair = [1, 2]
assert [2, 3] in nda and f_pair not in nda
if f_pair in nda:
    nda.remove(f_pair)    
print(nda)

nda = BiobjectiveNondominatedSortedList._random_archive(p_ref_point=1)
for t in [None, float]:
    if t:
        nda.hypervolume_final_float_type = t
        nda.hypervolume_computation_float_type = t
    for pair in list(nda):
        len_ = len(nda)
        state = nda._state()
        nda.remove(pair)
        assert len(nda) == len_ - 1
        if 100 * pair[0] - int(100 * pair[0]) < 0.7:
            res = nda.add(pair)
            assert all(state[i] == nda._state()[i] for i in (
               [0, 3] if nda.hypervolume_final_float_type is float else [0, 2, 3]))
print(nda)

mylist3 = [[1, 5], [2, 4], [4, 2], [5, 1], [4.5, 2.5], [2.5, 4.5]]
a3 = BiobjectiveNondominatedSortedList(mylist3, [6,6])
print(a3)
print(a3.reference_point)
print(a3.hypervolume) 
print(abs(a3.hypervolume - a3.compute_hypervolume(a3.reference_point)))

a3.add([2, 2])
print(a3)
print(a3.hypervolume) 
print(a3.compute_hypervolume(a3.reference_point))