import datetime as dt
import os
import csv


class IndexModel:
    def __init__(self) -> None:
        self.index_data = [["Date", "index_level"]]
    def calc_index_level(self, start_date: dt.date, end_date: dt.date) -> None:
        # Read stock price data into memory
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        dir = dir.replace('index_model', 'data_sources')
        os.chdir(dir)
        with open("stock_prices.csv", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            stock_data = [row for row in reader]
        # Initialize values
        initial_index_value = 100
        initial_portfolio_value = 0
        index_univ = []
        portfolio = []
        try:
            for i in range(len(stock_data)):
                trading_day = dt.datetime.strptime(stock_data[i][0], '%d/%m/%Y').date()
                # Find the start date
                if trading_day < start_date:
                    continue
                elif trading_day == start_date:
                    # add start date and index level
                    self.index_data.append([stock_data[i][0], initial_index_value])
                    # find the previous month end
                    lme_row_number = i
                    while dt.datetime.strptime(stock_data[lme_row_number][0], '%d/%m/%Y').date().month == trading_day.month:
                        lme_row_number = lme_row_number - 1
                    for j in range(1, len(stock_data[lme_row_number])):
                        index_univ.append(float(stock_data[lme_row_number][j]))
                    selected_stocks = sorted(range(len(index_univ)), key=lambda k: index_univ[k], reverse=True)[:3]
                    for stock in selected_stocks:
                        portfolio.append(stock)
                    # Calculate initial portfolio value
                    initial_portfolio_value = float(stock_data[i][portfolio[0] + 1]) * 0.5 + float(stock_data[i][portfolio[1] + 1]) * 0.25 + float(stock_data[i][portfolio[2] + 1]) * 0.25
                elif trading_day > start_date and trading_day <= end_date:
                    # Update portfolio at beginning of the month
                    if dt.datetime.strptime(stock_data[i - 1][0], '%d/%m/%Y').date().month != trading_day.month:
                        daily_portfolio_value = float(stock_data[i][portfolio[0] + 1]) * 0.5 + float(stock_data[i][portfolio[1] + 1]) * 0.25 + float(stock_data[i][portfolio[2] + 1]) * 0.25
                        daily_index_value = initial_index_value / initial_portfolio_value * daily_portfolio_value
                        self.index_data.append([stock_data[i][0], daily_index_value])
                        index_univ.clear()
                        for j in range(1, len(stock_data[i - 1])):
                            index_univ.append(float(stock_data[i - 1][j]))
                        selected_stocks = sorted(range(len(index_univ)), key=lambda k: index_univ[k], reverse=True)[:3]
                        portfolio.clear()
                        for stock in selected_stocks:
                            portfolio.append(stock)
                        initial_portfolio_value = float(stock_data[i][portfolio[0] + 1]) * 0.5 + float(stock_data[i][portfolio[1] + 1]) * 0.25 + float(stock_data[i][portfolio[2] + 1]) * 0.25
                        initial_index_value = daily_index_value
                    else:
                        daily_portfolio_value = float(stock_data[i][portfolio[0] + 1]) * 0.5 + float(stock_data[i][portfolio[1] + 1]) * 0.25 + float(stock_data[i][portfolio[2] + 1]) * 0.25
                        daily_index_value = initial_index_value / initial_portfolio_value * daily_portfolio_value
                        self.index_data.append([stock_data[i][0], daily_index_value])
                        initial_portfolio_value = daily_portfolio_value
                        initial_index_value = daily_index_value
        except IndexError:
            print("Input value out of range.")
        except ValueError:
            print("Invalid input value.")
            
    def export_values(self, file_name: str) -> None:
        path = os.getcwd()
        parent = os.path.dirname(path)
        os.chdir(parent)
        with open(file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for item in self.index_data:
                writer.writerow(item)
