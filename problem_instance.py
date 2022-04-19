import pandas as pd
import random
import re
from service_geocoding_query import ServiceAddressQuery


class ProblemInstance:
    """
    for the problem instance
    """

    def __init__(self, max_quantity=5, api_key=None) -> None:
        """
        initial the problem instance
        """
        self.max_quantity = max_quantity

        filename = "./data/order_data.xlsx"
        self.pickup_location = pd.read_excel(filename, sheet_name='訂單取貨點')
        self.delivery_location = pd.read_excel(filename, sheet_name='顧客點')
        self.product_list = pd.read_excel(filename, sheet_name='貨物')

        self.candidates_of_pickup_location = self.pickup_location.shape[0]
        self.candidates_of_devlivery_location = self.delivery_location.shape[0]
        self.num_of_product = self.product_list.shape[0]

        self.product_list['貨物名稱'][0:5].fillna('冰箱', inplace=True)
        self.product_list['貨物名稱'][6:11].fillna('冷氣', inplace=True)
        self.product_list['貨物名稱'][10:15].fillna('洗衣機', inplace=True)

        self.time_period = {
            'morning': {
                'start': 13,
                'end': 17
            },
            'afternoon': {
                'start': 9,
                'end': 12
            }
        }
        self.problem_instance = pd.DataFrame(
            columns=['pickup_location_id', 'pk_addr', 'pk_lon', 'pk_lat', 'pk_tw', 'order_detail', 'delivery_location_id',  'dl_addr', 'dl_lon', 'dl_lat', 'dl_tw'])

        self.service_address_query = ServiceAddressQuery(
            source="google_api", api_key=api_key)

        pass

    def __get_CBM(self, width, length, height):
        """
        calculate the CBM of the product
        """
        return width * length * height / 1000000

    def __random_delivery_house_number(self, location_range):
        if location_range == "全":
            return 1
        elif location_range == "單全":
            return 1
        elif location_range == "雙全":
            return 2
        else:
            try:
                """
                雙 210號以下
                """
                regex = re.compile(r'^(\w)\s+(\d+)\w+以(\w)')
                match = regex.search(location_range)
                if match != None:
                    if match.group(3) == "上":
                        # 以上, 因為不確定上界, 所以直接取此下界
                        return match.group(2)
                    if match.group(1) == "單":
                        # odd
                        return random.randrange(1, int(match.group(2)), 2)
                    else:
                        # oven
                        return random.randrange(2, int(match.group(2)), 2)
                """
                雙  60號至  76號
                """
                regex = re.compile(r'(\w)\s+(\d+)號至\s+(\d+)號')
                match = regex.search(location_range)
                if match != None:
                    # between two number
                    return random.randrange(int(match.group(2)), int(match.group(3)), 2)
                """
                其餘各種:
                　 119號
                　 766巷連  46號以上
                """
                regex = re.compile(r'(\d+)')
                match = regex.search(location_range)
                if match != None:
                    return match.group(1)

                """
                都不 match 的話
                """
                return 1
            except Exception as e:
                print("Error: {}, Range: {}".format(e, location_range))
                return None

    def __get_delivery_address(self, id):
        raw = self.delivery_location.loc[id]
        address = raw['縣市名稱'] + raw['鄉鎮市區'] + raw['原始路名'] + \
            str(self.__random_delivery_house_number(raw['投遞範圍'])) + '號'
        return address

    def __get_address(self, type, id):
        """
        get the address from pickup location list or delivery location list
        type = 'pickup' or 'delivery'
        """
        if type == "pickup":
            address = self.pickup_location.loc[id]['住址']
        elif type == "delivery":
            address = self.__get_delivery_address(id)
        return address

    def __generate_data_point(self, period):
        """
        generate each requirement
        including:
            'pickup_location_id', 'pk_addr', 'pk_lon', 'pk_lat', 'pk_tw', 
            'order_detail', 
            'delivery_location_id', 'dl_addr', 'dl_lon', 'dl_lat', 'dl_tw'
        """
        num_of_product = random.randrange(1, self.max_quantity)
        products = []
        for num in range(num_of_product):
            id = random.randrange(0, self.num_of_product)
            raw = self.product_list.loc[id]
            product = {
                "product_type": raw['貨物名稱'],
                "product_name": raw['規格'],
                "product_CBM": self.__get_CBM(raw['寬'], raw['深'], raw['高'])
            }
            products.append(product)
        data_point = {
            "pickup_location_id": random.randrange(0, self.candidates_of_pickup_location),
            "pk_tw": random.randrange(self.time_period[period]['start'], self.time_period[period]['end'], 1),
            "order_detail": products,
            "delivery_location_id": random.randrange(0, self.candidates_of_devlivery_location),
            "dl_tw": random.randrange(self.time_period[period]['start'], self.time_period[period]['end'], 1),
        }
        data_point["pk_addr"] = self.__get_address(
            type="pickup", id=data_point['pickup_location_id'])
        data_point["dl_addr"] = self.__get_address(
            type="delivery", id=data_point['delivery_location_id'])

        pk_geocode = self.service_address_query.query_geocoding_pipeline(
            data_point['pk_addr'])
        data_point['pk_lon'] = pk_geocode[0]
        data_point['pk_lat'] = pk_geocode[1]
        dl_geocode = self.service_address_query.query_geocoding_pipeline(
            data_point['dl_addr'])
        data_point['dl_lon'] = dl_geocode[0]
        data_point['dl_lat'] = dl_geocode[1]

        return pd.concat([self.problem_instance, pd.DataFrame(data_point).from_dict(data_point, orient="index").T])

    def generate_instance(self, instance_size=100, period="morning"):
        """
        generate the problem instance
        """
        self.instance_size = instance_size
        self.problem_instance = pd.DataFrame(
            columns=['pickup_location_id', 'pk_addr', 'pk_lon', 'pk_lat', 'pk_tw', 'order_detail', 'delivery_location_id',  'dl_addr', 'dl_lon', 'dl_lat', 'dl_tw'])
        for n in range(self.instance_size):
            self.problem_instance = self.__generate_data_point(
                period=period)
        self.problem_instance.reset_index(inplace=True, drop=True)
        return self.problem_instance

    def output_generate_instance(self):
        self.problem_instance.to_csv('n' + str(self.instance_size)+'.csv')
