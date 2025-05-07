def confirm(question: str):
    confirm_ = input(f"{question} [Yes/NO] ? ")
    if confirm_.lower() in ("y", "yes"):
        return True
    print("Canceled")
    return False


def to_bool(value: str | int | bool):
    if value is None:
        return value
    if isinstance(value, str):
        return value.lower() in ["yes", "true", "1"]
    return bool(value)
