import numpy as np
from itertools import takewhile


def compute_gate(value: int, gates: list[int]) -> int:
    # todo: ditch numpy alltogether
    # we could sort it by highest and then do next([x for x in keys if x <= minutes_played])
    gates = np.array(gates)
    lesser_gates = gates[gates <= value]
    if len(lesser_gates) == 0:
        return None
    current_gate = lesser_gates.max()
    return current_gate


def compute_next_gate(value: int, gates: list[int]) -> int:
    # todo: ditch numpy alltogether
    # we could sort it by highest and then do next([x for x in keys if x <= minutes_played])
    gates = np.array(gates)
    lesser_gates = gates[gates > value]
    if len(lesser_gates) == 0:
        return None
    next_gate = lesser_gates.min()
    return next_gate


def compute_gate_text(value: int, gates: dict[str, str]) -> tuple[int, str]:
    gates_keys = list(gates.keys())
    gates_thresholds = list([int(key) for key in gates_keys if key.isnumeric()])
    current_gate = compute_gate(value, gates_thresholds)
    gate_txt = gates.get(str(current_gate), None)
    return (current_gate, gate_txt)


def compute_next_gate_text(value: int, gates: dict[str, str]) -> tuple[int, str]:
    gates_keys = list(gates.keys())
    gates_thresholds = list([int(key) for key in gates_keys if key.isnumeric()])
    next_gate = compute_next_gate(value, gates_thresholds)
    gate_txt = gates.get(str(next_gate), None)
    return (next_gate, gate_txt)


def compute_time_txt(minutes: int):
    is_less_than_hour = minutes < 60
    unit = "mins" if is_less_than_hour else "hours"
    time = minutes if is_less_than_hour else round(minutes / 60, 1)
    if time == 1:
        unit = unit.rstrip("s")
    time_without_floating_zero = str(time).rstrip(".0")
    time_comp = f"{time_without_floating_zero} {unit}"
    return time_comp


def slice_text_array_at_total_length(max: int, texts: list[str]) -> list[list[str]]:
    temp_list = list(texts)
    new_list = []
    cursor = 0

    def get_str_len_sum(str_list: list[str]):
        return sum(len(s) for s in str_list)

    def calculate_added_sum(curr_chunk: list[str], new_str: str):
        chunk_sum = get_str_len_sum(chunk)
        new_sum = chunk_sum + len(new_str)
        return new_sum

    while len(temp_list) > cursor:
        chunk = []
        for item in takewhile(
            lambda x: calculate_added_sum(chunk, x) <= max, texts[cursor:]
        ):
            chunk.append(item)
        cursor += len(chunk)
        new_list.append(chunk)
    return new_list
