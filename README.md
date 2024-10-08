This code fetches foreign currency data from National Bank of the Republic of Türkiye.
To use the code properly, users must run it through a console with arguments.
The code receives two parameters: <br>
&emsp;--cur   :: Mandatory. Pass the symbol of one of the supported currencies.<br>
&emsp;--days  :: Optional. Pass an int value. Determines how many days of data the program will fetch. Default is 7.<br>
&emsp;--graph :: Optional. Pass a boolean True to generate a graph. Default is False.<br>
  <br><br>
Example usage:  >> python historical_data.py --cur eur
                >> python historical_data.py --cur usd --days 10
