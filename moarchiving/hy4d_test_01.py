from hv_plus import restart_base_setup_z_and_closest, DLNode, one_contribution_3d
from hv_plus import setup_cdllist, print_cdllist, cdllist_preprocessing
from hv_plus import hv3dplus, free_cdllist, hv4dplusR

def main():
    # Provided dataset, converted into a Python list of tuples
    new_points = [
    1, 10, 20, 30,
    2, 9, 25, 29,
    3, 8, 30, 28,
    4, 7, 35, 27,
    5, 6, 40, 26,
    6, 5, 18, 35,
    7, 4, 22, 34,
    8, 5, 28, 35,
    9, 2, 16, 40,
    10, 1, 15, 45
    ]
    d = 4
    n = 10

    new_ref = [11, 11, 41, 46]

    head = setup_cdllist(new_points, n, d, new_ref)

    # Assume head[3] is the first real data node
    current = head.next[d-1]
    index = 0
    while current and index < n:  # Avoid infinite loops, ensure only data nodes are processed
        #contribution = one_contribution_3d(head, current)
        #print(f"Volume contribution of node {index} is: {contribution}")
        current = current.next[d-1]
        index += 1
    
    print("Hyperovlume in 4d:", hv4dplusR(head))  


if __name__ == "__main__":
    main()
