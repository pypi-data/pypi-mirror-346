import argparse
from .converter import UnitConverter

def main():
    # Initialize the unit converter
    converter = UnitConverter()
    
    # Create the argument parser for CLI
    parser = argparse.ArgumentParser(description="Unit Converter Command Line Interface")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: convert
    convert_parser = subparsers.add_parser("convert", help="Convert a value from one unit to another")
    convert_parser.add_argument("category", type=str, help="Unit category (e.g., 'length', 'data')")
    convert_parser.add_argument("value", type=float, help="Numeric value to convert")
    convert_parser.add_argument("from_unit", type=str, help="Unit to convert from")
    convert_parser.add_argument("to_unit", type=str, help="Unit to convert to")

    # Subcommand: list_categories
    list_categories_parser = subparsers.add_parser("list_categories", help="List all available unit categories")

    # Subcommand: list_units
    list_units_parser = subparsers.add_parser("list_units", help="List basic units within a specific category")
    list_units_parser.add_argument("category", type=str, help="Unit category (e.g., 'data')")

    # Subcommand: list_aliases
    list_aliases_parser = subparsers.add_parser("list_aliases", help="List aliases for a specific unit")
    list_aliases_parser.add_argument("category", type=str, help="Unit category (e.g., 'data')")
    list_aliases_parser.add_argument("unit", type=str, help="Unit name to find aliases for")

    # Parse arguments from the command line
    args = parser.parse_args()

    # Handle each subcommand accordingly
    if args.command == "convert":
        try:
            result = converter.convert(args.category, args.value, args.from_unit, args.to_unit)
            print(f"{args.value} {args.from_unit} is equal to {result} {args.to_unit}")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "list_categories":
        categories = converter.list_categories()
        print("Available categories:", ", ".join(categories))

    elif args.command == "list_units":
        try:
            units = converter.list_units(args.category)
            print(f"Units in category '{args.category}':", ", ".join(units))
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "list_aliases":
        try:
            aliases = converter.list_unit_aliases(args.category, args.unit)
            print(f"Aliases for unit '{args.unit}' in category '{args.category}':", ", ".join(aliases))
        except ValueError as e:
            print(f"Error: {e}")

    else:
        print("Invalid command. Use --help to see available commands and usage.")

if __name__ == "__main__":
    main()
