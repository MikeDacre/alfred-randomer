import sys
import argparse
import inspect

from pyflow import Workflow

import generators


GENERATORS = {
    "email" : generators.random_email,
    "string": generators.random_string,
    "imei"  : generators.random_imei,
    "unit"  : generators.random_unit_number,
    "uuid"  : generators.random_uuid,
    "num"   : generators.random_number
}

# Generators that support the length parameter
GENERATORS_WITH_LENGTH = {"email", "string", "imei", "unit", "num"}


def parse_args(args):
    parser = argparse.ArgumentParser(description="Generate random values")
    parser.add_argument("generator", nargs="?", default=None,
                        help="Generator to use (email, string, imei, unit, uuid, num)")
    parser.add_argument("length", nargs="?", type=int, default=9,
                        help="Length of generated value (default: 9)")

    return parser.parse_args(args)


def main(workflow):
    args = parse_args(workflow.args)
    generator = args.generator.lower() if args.generator else None
    length = args.length

    if generator in GENERATORS:
        items = [generator] * 5
    else:
        items = sorted(GENERATORS.keys())

    for name in items:
        # Pass length to generators that support it
        if name in GENERATORS_WITH_LENGTH:
            values = [GENERATORS[name](length=length) for _ in range(5)]
        else:
            values = [GENERATORS[name]() for _ in range(5)]

        workflow.new_item(
            title=values[0],
            subtitle=f"{name} (length={length})" if name in GENERATORS_WITH_LENGTH else name,
            arg="\n".join(values),
            valid=True,
        )


if __name__ == "__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
