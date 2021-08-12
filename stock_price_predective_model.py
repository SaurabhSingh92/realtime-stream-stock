import yfinance as yf

if __name__ == '__main__':
    print("Starting the model creation")
    df = yf.download("INFY.NS", period="max")
    df.reset_index(inplace=True)
    train = df.sample(frac=0.9)
    test = df.drop(train.index)
