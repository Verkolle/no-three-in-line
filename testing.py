import time
from main import solve_problem


def run_test(test_n, test_k):
    print("________________________________")
    start = time.time()
    solve_problem(test_n, test_k)
    end = time.time()
    print("Solution found in {:0.2f} seconds".format(end-start))


def testing_list():
    # Pārbaudām nepiederošos ievaddatus
    run_test("a", 4)
    run_test(0, 4)
    run_test(2, 5)
    run_test(5.1, 3.2)

    # Pārbaudām, ka spēj apstrādāt patvaļīgus k
    run_test(4, 4)
    run_test(4, 8)
    run_test(4, 16)
    run_test(5, 8)
    run_test(5, 10)
    run_test(5, 15)

    # Pārbaudām patvaļīgus n
    # Parasti atrisina perfekti līdz n=8
    # Pie n = 9, 10, 11 bieži vien kļūdās
    # Pāris reizes ir atrisinājis arī n = 12, 13
    # Pēc tam gan novērojis ka atrisina perfekti
    for n in range(2, 16):
        run_test(n, 2*n)

    # Patestēju lielākus n
    run_test(30, 60)
    run_test(50, 100)


testing_list()
