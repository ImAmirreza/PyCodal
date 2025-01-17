import monthly_income
import plotting
import argparse

def main():
    parser = argparse.ArgumentParser(description="Process monthly income and plot data for given symbols.")

    parser.add_argument("symbols", nargs='+', help="List of symbols to process.")
    parser.add_argument("-u", "--update", action="store_true", help="Update the data.")
    parser.add_argument("-p", "--plot", action="store_true", help="Plot the data.")

    args = parser.parse_args()

    for symbol in args.symbols:
        try:
            monthly_income.main(symbol, update=args.update)
        except NotImplementedError as e:
            print(f"Error processing symbol {symbol}: {e}")
            # You can choose to continue or return based on your needs
            # return

    if args.plot:
        for symbol in args.symbols:
            plotting.main(symbol)

if __name__ == "__main__":
    main()
