import pandas as pd
import openpyxl
from sklearn.metrics.pairwise import cosine_similarity
import csv

def csv_to_excel (filename = "<csv_file_location>"):

    data_list = []

    with open(filename, "r")as f:

        data = csv.reader(f, delimiter=";")
        i = 0

        for line in data:
            if i != 0:
                data = {
                    "customer_id" : str(line[-6].replace("-", ".")),
                    "quantity" : int(line[-8]),
                    "goods" : line[-3]
                }
                data_list.append(data)
            i +=1

        df = pd.DataFrame(data_list, columns=[
            "customer_id",
            "goods",
            "quantity"
        ])

        return df

def data_preporation(data = "<data after func csv to excel>"):

    customer_item_matrix = data.pivot_table(
        index='customer_id',
        columns='goods',
        values='quantity',
        aggfunc='sum'
    )

    customer_item_matrix = customer_item_matrix.applymap(lambda x: 1 if x > 0 else 0)

    return customer_item_matrix


def calloborate_filter(data = "<df matrix>"):

    user_user_sim_matrix = pd.DataFrame(
        cosine_similarity(data)
    )
    user_user_sim_matrix.columns = data.index
    user_user_sim_matrix['customer_id'] = data.index
    user_user_sim_matrix = user_user_sim_matrix.set_index('customer_id')

    print(user_user_sim_matrix.loc["55574848.48495057545270"].sort_values(ascending=False))

    items_bought_by_A = set(data.loc["55574848.52575748515375"].iloc[
                                data.loc["55574848.52575748515375"].to_numpy().nonzero()
                            ].index)

    items_bought_by_B = set(data.loc["55574850.49555549495373"].iloc[
                                data.loc["55574850.49555549495373"].to_numpy().nonzero()
                            ].index)

    items_to_recommend_to_B = items_bought_by_A - items_bought_by_B

    print(items_to_recommend_to_B)

if __name__ == "__main__":
    global file

    file = "path to csv dataset"

    data = csv_to_excel(file)

    data_preporation = data_preporation(data)

    calloborate_filter = calloborate_filter(data_preporation)

