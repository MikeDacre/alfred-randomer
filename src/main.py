import sys
from pyflow import Workflow
import generators


GENERATORS = {
    "email": generators.random_email,
    "string": generators.random_string,
    "imei": generators.random_imei,
    "unit": generators.random_unit_number,
    "uuid": generators.random_uuid,
    "num": generators.random_number,
    "ipv4": generators.random_ipv4,
    "ipv6": generators.random_ipv6,
    "color": generators.random_hex_color,
    "port": generators.random_port,
    "isbn": generators.random_isbn,
    "plate": generators.random_license_plate,
    "apikey": generators.random_api_key,
    "base64": generators.random_base64,
    "hash": generators.random_hash,
    "phone": generators.random_phone_us,
    "phoneintl": generators.random_phone_international,
    "date": generators.random_date,
    "time": generators.random_time,
    "datetime": generators.random_datetime,
    "timestamp": generators.random_timestamp,
    "lorem": generators.random_lorem,
    "username": generators.random_username,
    "password": generators.random_password,
}

# Categorize generators by argument type
LENGTH_ONLY = {"string", "email", "imei", "unit", "apikey", "base64", "username", "lorem"}
RANGE_SUPPORT = {"num", "date", "time", "datetime", "timestamp"}
NO_ARGS = {"uuid", "ipv4", "ipv6", "color", "port", "isbn", "plate", "hash", "phone", "phoneintl"}
SPECIAL_PASSWORD = {"password"}


def parse_args(args):
    """Parse positional arguments for Alfred workflow"""
    if not args:
        return None, None, None, None

    generator = args[0].lower() if args else None

    if len(args) == 1:
        # Just generator name
        return generator, None, None, None
    elif len(args) == 2:
        # Generator + single argument (length or count)
        return generator, args[1], None, None
    elif len(args) == 3:
        # Generator + two arguments (range or length + special flag)
        return generator, args[1], args[2], None
    else:
        # Generator + three or more arguments (future expansion)
        return generator, args[1], args[2], args[3] if len(args) > 3 else None


def call_generator(name, arg1=None, arg2=None):
    """Call generator with appropriate arguments based on its type"""

    if name in NO_ARGS:
        # Generators that don't take arguments
        return GENERATORS[name]()

    elif name in LENGTH_ONLY:
        # Generators that only accept length
        length = int(arg1) if arg1 else 9
        return GENERATORS[name](length=length)

    elif name in RANGE_SUPPORT:
        # Generators that support both length and range
        if arg1 and arg2:
            # Range mode
            return GENERATORS[name](start=arg1, end=arg2)
        elif arg1:
            # Length mode for 'num', default mode for others
            if name == "num":
                length = int(arg1)
                return GENERATORS[name](length=length)
            else:
                # For date/time, single arg doesn't make sense, use default
                return GENERATORS[name]()
        else:
            # Default
            return GENERATORS[name]()

    elif name in SPECIAL_PASSWORD:
        # Password: arg1=length, arg2=include_special (0 or 1)
        length = int(arg1) if arg1 else 16
        include_special = bool(int(arg2)) if arg2 else False
        return GENERATORS[name](length=length, include_special=include_special)

    else:
        # Fallback
        return GENERATORS[name]()


def get_subtitle(name, arg1=None, arg2=None):
    """Generate helpful subtitle based on generator and arguments"""

    if name in NO_ARGS:
        return name
    elif name in LENGTH_ONLY:
        length = arg1 if arg1 else "9"
        return f"{name} (length={length})"
    elif name in RANGE_SUPPORT:
        if arg1 and arg2:
            return f"{name} (range: {arg1} to {arg2})"
        elif arg1:
            if name == "num":
                return f"{name} (length={arg1})"
            else:
                return f"{name} (default range)"
        else:
            return f"{name} (default)"
    elif name in SPECIAL_PASSWORD:
        length = arg1 if arg1 else "16"
        special = "with special chars" if (arg2 and int(arg2)) else "no special chars"
        return f"{name} (length={length}, {special})"
    else:
        return name


def main(workflow):
    generator, arg1, arg2, arg3 = parse_args(workflow.args)

    if generator and generator in GENERATORS:
        # Show specific generator
        items = [generator] * 5
    else:
        # Show all generators
        items = sorted(GENERATORS.keys())

    for name in items:
        try:
            # Generate 5 random values
            values = [call_generator(name, arg1, arg2) for _ in range(5)]
            subtitle = get_subtitle(name, arg1, arg2)

            workflow.new_item(
                title=values[0],
                subtitle=subtitle,
                arg="\n".join(values),
                valid=True,
            )
        except Exception as e:
            # Show error in subtitle for debugging
            workflow.new_item(
                title=f"Error in {name}",
                subtitle=str(e),
                valid=False,
            )


if __name__ == "__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
