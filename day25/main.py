def transform_subject_number(subject_number, loop_size):
    return pow(subject_number, loop_size, 20201227)


def find_loop_size(pub_key, subject_number):
    loop_size = 1
    while transform_subject_number(subject_number, loop_size) != pub_key:
        loop_size += 1

    return loop_size


with open('input') as input_file:
    card_public_key, door_public_key = [int(l.strip()) for l in input_file]

door_loop_size = find_loop_size(door_public_key, 7)
encryption_key = transform_subject_number(card_public_key, door_loop_size)
print(f'Part 1: {encryption_key}')