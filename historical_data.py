import requests, argparse
from datetime import datetime, timedelta
import pandas as pd
from matplotlib import pyplot as plt

def get_info(currency, number_of_days):
    
    rt_list = []
    rt_list.append(f"TP.DK.{currency}.A.YTL-0")
    rt_list.append(f"TP.DK.{currency}.S.YTL-0")
    rt_list.append(f"TP.DK.{currency}.A.EF.YTL-0")
    rt_list.append(f"TP.DK.{currency}.S.EF.YTL-0")

    num = len(rt_list)

    aggregationType = "#".join(["avg"]*num)
    formula = "#".join(["0"]*num)
    select = "#".join(rt_list)

    url = "https://evds2.tcmb.gov.tr/EVDSServlet"
    
    payload = {
        'thousand': '1',
        'decimal': '4',
        'frequency': 'Date',
        'aggregationType': aggregationType,
        'formula': formula,
        'skip': '0',
        'take': '20',
        # 'sort': 'Tarih#true',  #True sorts the value from new to old. ==> Tarih#true or Tarih#false
        'select': select,
        'startDate': (datetime.now() - timedelta(days=number_of_days)).strftime("%d-%m-%Y"),
        'endDate': (datetime.now() + timedelta(days=3)).strftime("%d-%m-%Y"),
        'categories': '5863@5865',
        'mongoAdresses': 'evds@evds',
        'datagroupString': 'bie_dkdovytl@bie_dkefkytl',
        'dateFormatValue': 'dd-mm-yyyy',
    }

    response = requests.post(url, data=payload)

    df = []

    for item in response.json()["items"]:
        df.append({
            "Date": (datetime.strptime(item["Tarih"], "%d-%m-%Y") - timedelta(days=1)).strftime("%d-%m-%Y"),
            "forexBuy": item[f"TP_DK_{currency}_A_YTL"],
            "forexSell": item[f"TP_DK_{currency}_S_YTL"],
            "Buy": item[f"TP_DK_{currency}_A_EF_YTL"],
            "Sell": item[f"TP_DK_{currency}_S_EF_YTL"]
        })

    df = df[::-1]
    # Find the first data
    for i in range(len(df)):
        if df[i]["forexBuy"] is not None:
            first_item_index = i
            break
    df = df[first_item_index:]

    # Now fill in the blanks
    for i, item in enumerate(df):
        if item["forexBuy"] is not None:
            last_item = item.copy()
            del last_item["Date"]
        else:
            new_item = {"Date": item["Date"]}
            new_item.update(last_item)
            df[i] = new_item

    df = df[::-1]
        
    return pd.DataFrame(df) if df else "No information found!"

parser = argparse.ArgumentParser(description="Get currency values from Turkish National Bank")
parser.add_argument("--cur", type=str, required=True, help="Name of the currency")
parser.add_argument("--days", type=int, required=False, help="Number of days of the past data")
parser.add_argument("--graph", type=str, required=False, help="Visualize graph")


args = parser.parse_args()
if args.days:
    days = args.days
else:
    days = 7

info = get_info(currency=args.cur.upper(), number_of_days=days)

print(info)

if args.graph:
    graph_dates = []
    for i in info["Date"]:
        graph_dates.append(i[:2])

    plt.plot(graph_dates, info["forexSell"], marker="o")
    plt.title("Graph")
    plt.show()
else:
    pass


