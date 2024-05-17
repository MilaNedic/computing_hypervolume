from hv_plus import restart_base_setup_z_and_closest, DLNode, one_contribution_3d
from hv_plus import setup_cdllist_new, print_cdllist, cdllist_preprocessing
from hv_plus import hv3dplus, free_cdllist

def main():
    # Provided dataset, converted into a Python list of tuples
    data = [
        0.16, 0.86, 0.47,
        0.66, 0.37, 0.29,
        0.79, 0.79, 0.04,
        0.28, 0.99, 0.29,
        0.51, 0.37, 0.38,
        0.92, 0.62, 0.07,
        0.16, 0.53, 0.70,
        0.01, 0.98, 0.94,
        0.67, 0.17, 0.54,
        0.79, 0.72, 0.05
    ]
    ref = [1, 1, 1]
    naloc = 12  # Including space for sentinel nodes
    n = 10
    d = 3

    # Initialize nodes and setup circular doubly linked list
    head = setup_cdllist_new(data, naloc, n, d, ref)
    cdllist_preprocessing(head, d-1, n+2)

    # Assume head[3] is the first real data node
    current = head.next[d-1]
    index = 0
    while current and index < n:  # Avoid infinite loops, ensure only data nodes are processed
        contribution = one_contribution_3d(head, current)
        print(f"Volume contribution of node {index} is: {contribution}")
        current = current.next[d-1]
        index += 1
        

if __name__ == "__main__":
    main()
