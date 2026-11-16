import argparse

from . import SECTORS, Warehouse, __version__


def main(argv=None):
    parser = argparse.ArgumentParser(prog="leblanc", description="Generate synthetic sector datasets")
    parser.add_argument("sector", choices=sorted(SECTORS) + ["warehouse"])
    parser.add_argument("-n", "--records", type=int, default=1000)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--locale", default="en_US")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--start-date")
    parser.add_argument("--missing", nargs="*")
    parser.add_argument("--missing-rate", type=float, default=0.05)
    parser.add_argument("--outliers", nargs="*")
    parser.add_argument("--duplicates", type=float, default=0.0)
    parser.add_argument("--no-seasonality", action="store_true")
    parser.add_argument("--version", action="version", version=f"leblanc {__version__}")
    args = parser.parse_args(argv)

    try:
        if args.sector == "warehouse":
            warehouse = Warehouse(
                num_customers=args.records, locale=args.locale, seed=args.seed,
                start_date=args.start_date, verbose=False, seasonality=not args.no_seasonality,
            )
            tables = warehouse.build()
            paths = warehouse.export(tables, args.output)
            print(f"{len(paths)} tables written to {args.output}")
            return
        generator = SECTORS[args.sector](
            num_records=args.records,
            locale=args.locale,
            seed=args.seed,
            start_date=args.start_date,
            verbose=False,
            seasonality=not args.no_seasonality,
        )
        df = generator.build(
            missing_data_cols=args.missing,
            missing_rate=args.missing_rate,
            outlier_cols=args.outliers,
            duplicate_rate=args.duplicates,
        )
        generator.export(df, args.output)
    except ValueError as error:
        parser.error(str(error))

    print(f"{len(df)} rows written to {args.output}")


if __name__ == "__main__":
    main()
