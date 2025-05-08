class IncorrectArgumentsError(Exception):
    def __init__(self, args: str, error_start_offset: int, error_length: int = 1):
        super().__init__(f"Incorrect run argument found")
        super().add_note(f"\t{args}\n\t{' ' * error_start_offset}{'^'*error_length}")
