from utilities import get_engine, read_data, post_data


if __name__ == "__main__":
    engine = get_engine()
    geo_dataframe = read_data()
    post_data(data=geo_dataframe, engine_=engine)
    print("done")
