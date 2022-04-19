"""Service for query geocoding information using different map apis"""
import re
import requests
import time
import argparse
import googlemaps
import pandas as pd
from datetime import datetime


class ServiceAddressQuery:
    """This class is for querying geocoding information using different map apis"""

    def __init__(self, source, api_key=None, result_column_name="geocoding_info"):
        """Initial the variables.
        Arguments:
        """
        self.source = source
        self.result_column_name = result_column_name
        if self.source == "google_api":
            if api_key is None:
                raise Exception('Need api_key!')
            # need to install
            self.api_key = api_key
            self.gmaps = googlemaps.Client(key=self.api_key)
            self.query_method = self.google_map_api_query
            self.sleep_time = 0
        elif self.source == "google_url":
            self.url = "https://www.google.com.tw/maps/place"
            self.query_method = self.google_url_query
            self.sleep_time = 3

    def query_geocoding_pipeline(self, address=None, df_input=None, column_name="address"):
        """"""
        self.df_input = df_input
        self.column_name = column_name
        if self.df_input is not None or address is not None:
            if self.df_input is None:
                geocode_result_raw, location_result, location_type = self.query_method(
                    address)
                if geocode_result_raw is not None:
                    print("Type: {}".format(location_type))
                    print("Longitude: {}".format(location_result["lng"]))
                    print("Latitude: {}".format(location_result["lat"]))
                    return (location_result["lng"], location_result["lat"])
                else:
                    print("Can't get the geocoding info.")
                    return (-1000, -1000)
            else:
                if self.column_name not in self.df_input.columns:
                    raise Exception('Need to revise column_name to address!')
                result = []
                for address in self.df_input[self.column_name]:
                    time.sleep(self.sleep_time)
                    _, location_result, _ = self.query_method(address)
                    if location_result is not None:
                        result.append(
                            (location_result["lng"], location_result["lat"]))
                    else:
                        result.append((-1000, -1000))
                    print("Address: {}, Longitude: {}, Latitude: {}".format(
                        address, location_result["lng"], location_result["lat"]))
                self.df_output = self.df_input.copy(deep=True)
                self.df_output[self.result_column_name] = result
                return self.df_output
        else:
            raise Exception("Need a address or a dataframe input!")

    def google_map_api_query(self, address):
        """"""
        try:
            geocode_result = self.gmaps.geocode(address)
            location_result = geocode_result[0]["geometry"]["location"]
            location_type = geocode_result[0]["geometry"]["location_type"]
            return geocode_result, location_result, location_type
        except Exception as e:
            print("Error: {}, Address: {}".format(e, address))
            return None, None, None

    def google_url_query(self, address):
        """"""
        # get the address having correct format
        address_new = re.search("\S+號", address)
        if address_new:
            address_new = address_new.group()
        else:
            raise Exception("Address is incorrect foramt!")
        try:
            response = requests.get("{}/{}".format(self.url, address_new))
            # find longitude and latitude in the text
            tmp_r = re.findall("\d+\.\d+,\d+\.\d+", response.text)
            status = False
            # check the result in taiwan
            for axis in tmp_r:
                y, x = axis.split(",")
                if (22 <= float(y) <= 26) and (120 <= float(x) <= 123):
                    status = True
                if status:
                    break
            if not status:
                print("Can't find suitable x, y")
                return None, None, None
            return response.text, {"lng": float(x), "lat": float(y)}, "google_url"
        except Exception as e:
            print("Error: {}, Address: {}".format(e, address))
            return None, None, None


if __name__ == "__main__":
    """"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', type=str, required=False, default=None,
                        help="The string of google api key if you use google map api.")
    parser.add_argument('--source', type=str, required=True, default=None,
                        help="The source you want to use to query geocoding info.")
    # if string input
    parser.add_argument('--address', type=str, required=True, default=None,
                        help="The address you want to query.")
    # if dataframe input
    parser.add_argument('--path', required=False, type=str, default=None,
                        help="The csv path if you want to use dataframe as input.")
    parser.add_argument('--output_path', required=False, type=str, default="./result.csv",
                        help="The result output path.")
    parser.add_argument('--column_name', required=False, type=str, default="address",
                        help="The column of dataframe for address.")
    args = parser.parse_args()
    service_address_query = ServiceAddressQuery(
        source=args.source, api_key=args.api_key)
    if args.path:
        df_input = pd.read_csv(args.path)
        address = None
    else:
        df_input = None
        address = args.address
    result = service_address_query.query_geocoding_pipeline(
        address=address, df_input=df_input)
    if args.path:
        result.to_csv(args.output_path)
