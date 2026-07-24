from itertools import groupby

total_length_constrain, total_num_of_input = map(int, input("Enter the input: ").strip().split())
initial_string = input("Enter inital string: ")

def itentify_the_sub_string(string_data: str):
    """group by sub string"""
    sub_string =  {
        len(list(g)): k
        for k, g in groupby(string_data)
    }

    fetch_max_key = max(list(sub_string.keys()))

    return str(fetch_max_key)



def handle_sub_string(total_length_constrain: int, total_num_of_input: int, initial_string: str):
    "handle consective substring"

    total_consective_substring = []

    if total_length_constrain < len(initial_string):
        raise ValueError("Exceeding the expected string length")

    total_consective_substring.append(itentify_the_sub_string(initial_string))

    for _ in range(total_num_of_input):
        recurring_string = input("Enter the string: ")
        initial_string = initial_string+recurring_string

        total_consective_substring.append(itentify_the_sub_string(initial_string))

    return ' '.join(total_consective_substring)

final_data = handle_sub_string(total_length_constrain, total_num_of_input, initial_string)

print(final_data)