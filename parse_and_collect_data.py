from collections import defaultdict


class ParseException(Exception):
    pass


def parse_and_collect_data(
    data: list[tuple[str, str]],
    api_map: defaultdict | None = None,
) -> defaultdict:
    """
    Parse and collect API data into a nested defaultdict structure.

    :param data: A list of tuples containing verb and path.
    :param api_map: A defaultdict to store the parsed data.
        If not provided, a new defaultdict will be created.

    :return: A nested defaultdict containing the parsed API data.

    :raises ParseException: If there is a conflict between two verb and path combinations.
    """
    if api_map is None:
        api_map = defaultdict(dict)

    for verb, path in data:
        parts = path.split("/")[3:]  # Отрезаем /api/v1
        curr_map = api_map  # Отслеживаем текущую позицию в словаре
        for i, part in enumerate(parts):
            if part.startswith("{"):
                continue

            if (
                i == len(parts) - 1
            ):  # Если это последний элемент, то значением будет метод
                if curr_map[part] and curr_map[part] != verb:
                    # Если уже есть значение, то проверяем, что оно совпадает
                    raise ParseException(
                        f"Conflict at path {path}: {curr_map[part]} vs {verb}"
                    )
                curr_map[part] = verb
            else:
                if part not in curr_map:  # Если нет, то создаем пустой словарь
                    curr_map[part] = defaultdict(dict)
                curr_map = curr_map[part]
    return api_map
