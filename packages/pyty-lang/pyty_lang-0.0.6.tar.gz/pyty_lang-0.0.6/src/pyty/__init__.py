import sys
from pyty.exception import IncorrectArgumentsError


def pyty():
    def parse_args(args: list[str]) -> dict:
        joined_args = []
        for i in range(len(args)):
            arg = args[i]
            if arg.startswith("-"):
                joined_args.append(arg)
            else:
                if joined_args and len(joined_args[-1].split(" ")) <= 1:
                    joined_args[-1] += " " + arg
                else:
                    offset = len(" ".join(args[:i+1])) - len(arg)
                    raise IncorrectArgumentsError(" ".join(args), offset, len(arg))

        res = {}
        for i in range(len(joined_args)):
            arg = joined_args[i].split()
            key = arg[0]
            while key.startswith("-"):
                key = key[1:]

            if key not in CONFIG.keys():
                offset = len(" ".join(joined_args[:i+1])) - len(" ".join(arg))
                raise IncorrectArgumentsError(" ".join(joined_args), offset, len(" ".join(arg)))

            converter = CONFIG[key]
            try:
                val = arg[1]
            except IndexError:
                if converter is None:
                    val = None
                else:
                    offset = len(" ".join(joined_args[:i + 1])) - len(" ".join(arg))
                    _types = {
                        str: "string",
                        int: "integer",
                        float: "float",
                        bool: "boolean"
                    }
                    raise IncorrectArgumentsError(" ".join(joined_args), offset, len(" ".join(arg)),
                                                  f"Expected a {_types[converter]} argument but flag found")

            try:
                val = converter(val)
            except:
                offset = len(" ".join(joined_args[:i + 1])) - len(" ".join(arg))
                _types = {
                    str: "string",
                    int: "integer",
                    float: "float",
                    bool: "boolean",
                    None: "flag"
                }
                raise IncorrectArgumentsError(" ".join(joined_args), offset, len(" ".join(arg)),
                                              f"Expected a {_types[converter]} argument but it wasn't provided")

            res[key] = val
        return res

    CONFIG = {
        "outDir": str
    }
    ARGUMENTS = parse_args(sys.argv[1:])
