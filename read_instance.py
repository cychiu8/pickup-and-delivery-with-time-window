import pandas as pd


class ReadInstance:
    def __init__(self) -> None:
        self.instance_info = {}
        self.DEF_NUM = 10
        self.original = pd.DataFrame()
        self.nodes = pd.DataFrame()
        self.distance_matrix = pd.DataFrame()

    def read_instance_from_file(self, filename):
        """
        read instance from "Instances for the Pickup and Delivery Problem with Time Winodws"
        """

        # full file
        self.original = pd.read_csv(filename, header=None)

        # read the general information
        description = self.original.iloc[:self.DEF_NUM]
        description = description[0].str.split(":", n=-1, expand=True)
        description.columns = ['parameter', 'value']
        dict_de = description.set_index('parameter').T.to_dict(orient='list')
        for key in dict_de.keys():
            self.instance_info[key.lower()] = dict_de[key][0]

        # read the locations and requirements
        self.nodes = self.original.iloc[self.DEF_NUM +
                                        1: self.DEF_NUM + 1 + int(self.instance_info['size']) + 1]
        self.nodes = self.nodes[0].str.split(" ", n=-1, expand=True)
        self.nodes.columns = ['id', 'lat', 'lon', 'demand',
                              'etw', 'ltw', 'duration', 'pickup', 'delivery']

        # read the distance matrix
        self.distance_matrix = self.original.iloc[self.DEF_NUM + 2 + int(
            self.instance_info['size']): self.DEF_NUM + 1 + 2 * int(self.instance_info['size']) + 1]
        self.distance_matrix = self.distance_matrix[0].str.split(
            " ", n=-1, expand=True)

    def generate_instance(
        self,
        name='instance',
        location='Taipei',
        comment='TMS (2022)',
        type='PDPTW',
        size=100,
        distribution='',
        depot='central',
        route_time=400,
        time_window=60,
        capacity=300
    ):
        self.instance_info.name = name
        self.instance_info.location = location
        self.instance_info.comment = comment
        self.instance_info.type = type
        self.instance_info.size = size
        self.instance_info.distribution = distribution
        self.instance_info.depot = depot
        self.instance_info.route_time = route_time
        self.instance_info.time_window = time_window
        self.instance_info.capacity = capacity


filename = "./data/Instances for the Pickup and Delivery Problem with Time Windows based on open data/Instances/n100/n100/bar-n100-1.txt"
problem = ReadInstance()
problem.read_instance_from_file(filename)

infos = problem.instance_info
nodes = problem.nodes
matrix = problem.distance_matrix
