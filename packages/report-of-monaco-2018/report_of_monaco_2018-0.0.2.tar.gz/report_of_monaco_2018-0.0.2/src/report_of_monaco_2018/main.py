import argparse

from report_of_monaco_2018.racing import RaceData


def main() -> None:
    """
    Read data from cli and pass it to print_report
    :return: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="path to data file")
    parser.add_argument("--driver", type=str, help="driver name to filter")

    group = parser.add_mutually_exclusive_group()

    group.add_argument("--asc", action="store_true", help="sort ascending")
    group.add_argument("--desc", action="store_true", help="sort descending")

    args = parser.parse_args()
    sort_order = "desc" if args.desc else "asc"
    race = RaceData()
    try:
        if args.driver:
            race.print_report(file=args.file, driver=args.driver)
        else:
            race.print_report(file=args.file, driver=args.driver, sort_order=sort_order)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"\n[ERROR] {e}\n")

    except ValueError as e:
        raise ValueError(f"\n[ERROR] {e}\n")


if __name__ == "__main__":
    main()
