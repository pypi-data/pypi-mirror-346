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
            val = arg[1]

            try:
                val = float(val)
            except:
                ...

            try:
                val = int(val)
            except:
                ...

            if isinstance(val, str):
                if val.lower() == 'true':
                    val = True
                elif val.lower() == 'false':
                    val = False

            res[key] = val
        return res


    ARGUMENTS = parse_args(sys.argv[1:])
    print(ARGUMENTS)
