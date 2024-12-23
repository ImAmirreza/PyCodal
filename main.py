import monthly_income
import plotting

def main():
    symbols = ["تجلی"]
    for symbol in symbols:
        try:
            monthly_income.main(symbol)
        except NotImplementedError as e:
            return
        plotting.main(symbol)
main()