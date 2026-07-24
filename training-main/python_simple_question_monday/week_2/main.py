from itertools import permutations


def main():
    print("Hello from problem_array_2!")


def solve_problem(tasks):
    """Parallel Processing Problem.

    Given N tasks with execution times, split them into a prefix for processor 1
    and remaining tasks for processor 2. Both processors work in parallel.
    Find the minimum possible maximum execution time.

    Args:
        tasks: List[int] - Execution times of tasks

    Returns:
        int - Minimum possible total execution time

    Examples:
        tasks = [4, 2, 3] -> 5
        tasks = [1, 1, 1, 1, 1, 1] -> 3
    """

    q_1, q_2 = [], []

    if len(tasks) == 1:
        return sum(tasks)

    for task in tasks:
        if not q_1 or not q_2:
            if not q_1:
                q_1.append(task)
            else:
                if not q_2:
                    q_2.append(task)
        else:
            if q_1 and q_2:
                if sum(q_1) >= sum(q_2):
                    q_2.append(task)
                elif sum(q_2) <= sum(q_1):
                    q_1.append(task)
                else:
                    q_1.append(task)

    return max(sum(q_1), sum(q_2))


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
