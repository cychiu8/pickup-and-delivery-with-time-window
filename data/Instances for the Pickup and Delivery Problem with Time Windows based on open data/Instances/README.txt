
## Structure of instance files (or how to read them).

"Instances for the Pickup and Delivery Problem with Time Windows 
 based on open data"

===============================================================================
===============================================================================

The first 10 lines of each file contain general information about the
instance. These are:

NAME:          <unique instance identification>
LOCATION:      <city where it was generated>
COMMENT:       <a general reference>
TYPE:          <the type is always PDPTW>
SIZE:          <number of nodes including the depot>
DISTRIBUTION:  <the type of distribution>
DEPOT:         <type of depot location: either 'central' or 'random'>
ROUTE-TIME:    <time horizon>
TIME-WINDOW:   <time window width>
CAPACITY:      <maximum vehicle capacity>

Then, a line containing the word NODES is followed by SIZE lines
containing the complete information of each location (node) in the
instance file. For each line, there are 9 fields separated by a
single white space character as below:

<id> <lat> <long> <dem> <etw> <ltw> <dur> <p> <d>

The fields are:
<id>:   the unique node identifier ( node 0 is the unique depot )
<lat>:  latitude of this location
<lon>:  longitude of this location
<dem>:  the demand of this node ( dem > 0 for pickup, dem < 0 for delivery )
<etw>:  earliest possible time to start service (Time Window)
<ltw>:  latest possible time to start service (Time Window)
<dur>:  the service duration at this location
<p>:    the pickup pair if <id> is a delivery, and 0 otherwise
<d>:    the delivery pair if <id> is a pickup, and 0 otherwise


The <p> and <d> are for completeness reasons only. In all instances,
for a pickup location <id> its delivery is given by (<id>+((SIZE-1)/2)).
For a delivery location <id>, its pickup is given by (<id>-((SIZE-1)/2)).


After all NODES, there is a line containing the word EDGES followed by SIZE
lines, each one with SIZE integer values separated by a single white space
character. These integers represent the travel times between each pair of
locations in the instance, measured in minutes and computed using the
Open Source Routing Machine (OSRM)[1] tool.

All instances end with a line containing the word EOF.

===============================================================================
===============================================================================

NOTES:
      (1): For cluster and cluster-random distributions, (x / y) indicate
       that x seeds were chosen to create clusters and the density used
       in the selection of locations was y.

      (2): There are only two float values in an instance: <lat> and <lon>.
       All other values are integers.
       (except for the cluster density when applicable)

      (3): The only information that is strictly necessary to solve an 
       instance is included in the following fields: CAPACITY, NODES, EDGES. 
       All the remaining values are either auxiliary (e.g., SIZE) or simply 
       additional information about the instance.

===============================================================================
===============================================================================

References:
[1]: Luxen, D., Vetter, C., 2011. Real-time routing with openstreetmap data. 
     In: Proceedings of the 19th ACM SIGSPATIAL International Conference 
     on Advances in Geographic Information Systems. GIS ’11. ACM, New York, 
     NY, USA, pp. 513–516.

===============================================================================
===============================================================================

## Carlo Sartori and Luciana Buriol (2019).



