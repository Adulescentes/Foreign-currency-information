This code fetches foreign currency data from National Bank of the Republic of Türkiye.
To use the code properly, users must run it through a console with arguments.
The code receives two parameters:
  --cur   :: Mandatory. Pass the symbol of one of the supported currencies.
  --days  :: Optional. Pass an int value. Determines how many days of data the program will fetch. Default is 7.
  --graph :: Optional. Pass a boolean True to generate a graph. Default is False.
  
Example usage:  >> python historical_data.py --cur eur
                >> python historical_data.py --cur usd --days 10
