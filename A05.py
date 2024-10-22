def run_A05():

    import numpy as np

    import pandas as pd

    from datetime import datetime



    # Clear console (optional, for better readability)

    print("\033c", end="")



    # Lot number calculation

    lot_number = round((datetime.now() - datetime(2024, 9, 2)).total_seconds())

    print(f'Lot number L{lot_number}')



    # User inputs

    boxes = int(input('Number of boxes to sample from? '))

    tests = int(input('Number of tests per box (one "test" is weight n = 4 pastries)? '))



    N_in_box = 3 * 4 * 3

    if (tests * 4) > N_in_box:

        raise ValueError(f'Too many tests for one box, limit is {N_in_box} pastries per box')



    # Randomly select box numbers

    box_number = np.random.permutation(125)[:boxes]



    N = 4

    m = 97 + (np.random.rand() - 0.5) * 12

    np.random.seed()  # Shuffle the random number generator based on current time

    boxes_e = (np.random.rand(boxes) - 0.5) / 6

    tests_e = (np.random.rand(boxes, tests) - 0.5) / 4



    c = 0

    X = np.zeros((boxes * tests, N))  # Preallocate X with the right shape

    box_list = []

    test_list = []



    for b in range(boxes):

        for t in range(tests):

            for n in range(N):

                X[c, n] = m + boxes_e[b] + tests_e[b, t]

            box_list.append(box_number[b])

            test_list.append(t + 1)  # Test numbers start from 1

            c += 1



    # Add randomness to X

    X += (np.random.rand(*X.shape) - 0.5) / 4

    X = np.round(X * 100) / 100



    # Prepare data for CSV

    f = f'L{lot_number}'

    header = f'Box, Test, n1, n2, n3, n4, -> Weight (g), Lotnumber, {f}'

    data = np.hstack((np.array(box_list).reshape(-1, 1), 

                      np.array(test_list).reshape(-1, 1), 

                      X))



    # Create a DataFrame

    df = pd.DataFrame(data, columns=['Box', 'Test', 'n1', 'n2', 'n3', 'n4'])

    df['Lotnumber'] = lot_number



    # Save to CSV

    df.to_csv(f'{f}.csv', index=False, header=True)