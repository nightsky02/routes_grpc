def validate_list_of_ids(l: list[int]) -> bool:
    for v in l:
        if v <= 0:
            return False

    return True