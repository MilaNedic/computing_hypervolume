from hv_plus import restart_base_setup_z_and_closest, DLNode, one_contribution_3d
from hv_plus import setup_cdllist_new, print_cdllist, cdllist_preprocessing
from hv_plus import hv3dplus, free_cdllist

def main():
    # Provided dataset, converted into a Python list of tuples
    data = [
        10, 20, 30,
        20, 18, 29,
        30, 16, 28,
        40, 14, 27,
        50, 12, 26,
        60, 10, 25,
        70, 8, 24,
        80, 6, 23,
        90, 4, 22,
        100, 2, 21

    ]
    ref = [101, 21, 31]
    naloc = 12  # Including space for sentinel nodes
    n = 10
    d = 3

    # Initialize nodes and setup circular doubly linked list
    head = setup_cdllist_new(data, naloc, n, d, ref)
    #cdllist_preprocessing(head, d-1, n+2)

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
