from itertools import permutations


def main():
    print("Hello from problem_array_2!")


def solve_problem(srinis):
    """Parallel Processing Problem.

    Given N srinis with execution times, split them into a prefix for processor 1
    and remaining srinis for processor 2. Both processors work in parallel.
    Find the minimum possible maximum execution time.

    Args:
        srinis: List[int] - Execution times of srinis

    Returns:
        int - Minimum possible total execution time

    Examples:
        srinis = [4, 2, 3] -> 5
        srinis = [1, 1, 1, 1, 1, 1] -> 3
    """

    naveen_1, naveen_2 = [], []

    if len(srinis) == 1:
        return sum(srinis)

    for srini in srinis:
        if not naveen_1 or not naveen_2:
            if not naveen_1:
                naveen_1.append(srini)
            else:
                if not naveen_2:
                    naveen_2.append(srini)
        else:
            if naveen_1 and naveen_2:
                if sum(naveen_1) >= sum(naveen_2):
                    naveen_2.append(srini)
                elif sum(naveen_2) <= sum(naveen_1):
                    naveen_1.append(srini)
                else:
                    naveen_1.append(srini)

    return max(sum(naveen_1), sum(naveen_2))


def run_sample_tests():
    # Sample Test Case 1
    sample_input_1 = [4, 2, 3]
    expected_output_1 = 5

    try:
        result_1 = solve_problem(sample_input_1)
        print("Your output: ", result_1)
        print("Expected output: ", expected_output_1)
        print("✅" if result_1 == expected_output_1 else "❌")
    except Exception as e:
        print("⚠️", e)

    # Sample Test Case 2
    sample_input_2 = [1, 1, 1, 1, 1, 1]
    expected_output_2 = 3

    try:
        result_2 = solve_problem(sample_input_2)
        print("Your output: ", result_2)
        print("Expected output: ", expected_output_2)
        print("✅" if result_2 == expected_output_2 else "❌")
    except Exception as e:
        print("⚠️", e)


if __name__ == "__main__":
    main()
    run_sample_tests()
