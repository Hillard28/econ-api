"""
Early work in progress.
FRED and Census API keys can be obtained for free; to obtain, visit:
https://fred.stlouisfed.org/
https://www.census.gov/data/developers.html

Observation arguments

Units
lin: Levels
chg: Change
ch1: Change from a year ago
pch: Percent change
pc1: Percent change from a year ago
pca: Compounded annual rate of change
cch: Continuously compounded rate of change
cca: Continuously compounded annual rate of change
log: Natural log

Frequency
d: Daily
w: Weekly
bw: Biweekly
m: Monthly
q: Quarterly
sa: Semiannual
a: Annual
wef: Weekly, ending Friday
weth: Weekly, ending Thursday
wew: Weekly, ending Wednesday
wetu: Weekly, ending Tuesday
wem: Weekly, ending Monday
wesu: Weekly, ending Sunday
wesa: Weekly, ending Saturday
bwew: Biweekly, ending Wednesday
bwem: Bieekly, ending Monday

Aggregation method
avg: Average
sum: Sum
eop: End of period
"""

# For loading data if you want to skip all the previous inputs
import requests


class Fred(object):

    root_url = "https://api.stlouisfed.org/fred/"

    def __init__(self, api_key=None):
        """Set key used to access FRED API"""
        self.api_key = None
        if api_key is not None:
            self.api_key = str(api_key)
        if self.api_key is None:
            raise ValueError("Please enter an API key")
        elif len(self.api_key) < 32:
            raise ValueError("Please enter a valid API key")

    def search_series(self, search_text, search_type="full_text", limit=1000, **kwargs):
        """
        Search for series maintained by FRED using keywords

        Parameters
        ----------
        search_text: str
            Text used to search FRED (required)
        search_type: str
            Type of search performed (optional, default: "full_text")
        limit: int
            Maximum number of results (optional, default: 1000)
        order_by: str
            Orders results by attribute (optional, default: "search_rank")
        """
        url = (
            self.root_url
            + "series/search?search_text="
            + search_text.replace(" ", "+")
            + "&search_type="
            + search_type
            + "&limit="
            + str(limit)
        )

        if kwargs.keys():
            for arg, val in kwargs.items():
                url += "&" + str(arg) + "=" + str(val)
        url += "&api_key=" + self.api_key + "&file_type=json"

        request = requests.get(url).json()

        return request

    def get_series_info(self, series_id):
        """Get info on specific FRED series"""
        url = self.root_url + "series?series_id=" + series_id

        url += "&api_key=" + self.api_key + "&file_type=json"

        request = requests.get(url).json()

        return request

    def get_observations(
        self,
        series_id,
        observation_start="1776-07-04",
        observation_end="9999-12-31",
        **kwargs
    ):
        """
        Get series maintained by FRED using ID

        Parameters
        ----------
        series_id: str
            FRED series ID (required)
        observation_start: datetime or datetime-like str
            Earliest observation date (optional, default: "1776-07-04")
        observation_end: datetime or datetime-like str
            Latest observation date (optional, default: "9999-12-31")
            WILL NEED TO BE UPDATED FOR THE 101ST CENTURY
        units: str
            Data value transformations (optional, default: "lin")
        frequency: str
            Frequency of observations (optional, default: None)
        aggregation_method: str
            Data aggregation if frequency set (optional, default: "avg")

        Returns
        -------
        Dates: list(str)
        Series ID: str
        Series values: list(str)
        """
        url = (
            self.root_url
            + "series/observations?series_id="
            + series_id
            + "&observation_start="
            + observation_start
            + "&observation_end="
            + observation_end
        )

        if kwargs.keys():
            for arg, val in kwargs.items():
                url += "&" + str(arg) + "=" + str(val)
        url += "&api_key=" + self.api_key + "&file_type=json"

        request = requests.get(url).json()

        data = []

        for item in request["observations"]:
            observation = {}
            observation["id"] = series_id
            observation["date"] = item["date"]
            observation["value"] = item["value"]
            data.append(observation)
        return data


class Census(object):

    root_url = "https://api.census.gov/data/"

    def __init__(self, key=None):
        self.key = None
        if key is not None:
            self.key = str(key)
        if self.key is None:
            print("You will be limited to 500 queries per IP address")
        elif len(self.key) < 32:
            print("You may not have entered a valid API key")

    def get_dict(self, source="acs1", year=2019):
        if "acs" in source:
            src = year + "/acs/" + source
        elif "sf" in source:
            src = year + "/dec/" + source
        else:
            src = year + "/" + source
        url = self.root_url + src + "/variables.json"

        request = requests.get(url).json()

        data = request["variables"]

        return data

    def get_data(
        self,
        source="acs1",
        year=2019,
        variables="",
        geographical_level="",
        geographies="",
        **kwargs
    ):

        if "acs" in source:
            src = year + "/acs/" + source + "?"
        elif "sf" in source:
            src = year + "/dec/" + source + "?"
        else:
            src = year + "/" + source + "?"
        if type(variables) is list or type(variables) is tuple:
            var = "get=" + ",".join(variables)
        else:
            var = "get=" + variables
        geographical_level = geographical_level.replace(" ", "%20")
        if geographies != "":
            geo = "for=" + geographical_level + ":" + geographies
        else:
            geo = "for=" + geographical_level + ":*"
        kwarg = ""
        if kwargs.keys():
            for arg, val in kwargs.items():
                if arg == "state":
                    kwarg += "&in=" + str(arg) + ":" + str(val)
                else:
                    kwarg += "&" + str(arg) + "=" + str(val)
        if self.key is not None:
            url = self.root_url + src + var + "&" + geo + kwarg + "&key=" + self.key
        else:
            url = self.root_url + src + var + "&" + geo + kwarg
        request = requests.get(url).json()

        data = []
        for entry in request[1:]:
            observation = {}
            for entry1, entry2 in zip(request[0], entry):
                observation[entry1] = entry2
            data.append(observation)
        return data


class AlphaVantage(object):

    root_url = "https://www.alphavantage.co/query?"

    def __init__(self, api_key=None):
        """Set key used to access Alpha Vantage API"""
        self.api_key = None
        if api_key is not None:
            self.api_key = str(api_key)
        if self.api_key is None:
            raise ValueError("Please enter an API key")
        elif len(self.api_key) < 16:
            raise ValueError("Please enter a valid API key")

    def get_observations(
        self,
        symbol,
        period,
        interval="",
        adjusted=False,
        extended=False,
        **kwargs
    ):
        if period.lower() == "monthly":
            if adjusted == False:
                function = "MONTHLY"
            elif adjusted == True:
                function = "MONTHLY_ADJUSTED"
        elif period.lower() == "weekly":
            if adjusted == False:
                function = "WEEKLY"
            elif adjusted == True:
                function = "WEEKLY_ADJUSTED"
        elif period.lower() == "daily":
            if adjusted == False:
                function = "DAILY"
            elif adjusted == True:
                function = "DAILY_ADJUSTED"
        elif period.lower() == "intraday":
            if extended == False and interval != "":
                function = "INTRADAY&interval=" + interval
            elif extended == True and interval != "":
                function = "INTRADAY_EXTENDED&interval=" + interval
            else:
                raise ValueError("Please enter a valid interval")
        
        url = (
            self.root_url
            + "function=TIME_SERIES_" + function
            + "&symbol="
            + symbol.upper()
            )

        if kwargs.keys():
            for arg, val in kwargs.items():
                url += "&" + str(arg) + "=" + str(val)
        url += "&apikey=" + self.api_key + "&datatype=json"

        request = requests.get(url).json()
        
        data = []
        
        if period.lower() == "intraday":
            for key, item in request["Time Series (" + interval + ")"].items():
                observation = {}
                observation["id"] = symbol
                observation["date"] = key
                for value in item:
                    observation[value[3:]] = item[value]
                data.append(observation)
        else:
            for key, item in request["Time Series (" + function.capitalize() + ")"].items():
                observation = {}
                observation["id"] = symbol
                observation["date"] = key
                for value in item:
                    observation[value[3:]] = item[value]
                data.append(observation)

        return data
