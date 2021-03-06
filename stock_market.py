import datetime
import yfinance as yf
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from pyspark.sql import SparkSession
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateLocator
from matplotlib.axis import Axis


def main():
    spark = SparkSession.builder.master("local").appName("Stock").getOrCreate()
    fig, ax = plt.subplots()

    def get_data(i):
        start_date = datetime.strptime("2021-05-01", "%Y-%m-%d") + timedelta(i)
        end_date = start_date + timedelta(days=7)
        if start_date == datetime.date:
            print("Current date !! ")
            exit(0)
        data = yf.download(tickers='INFY.NS', start=start_date, end=end_date)
        ax.plot(data.index.values, data['Open'])

    ani = FuncAnimation(fig, get_data, interval=10)
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == '__main__':
    main()
