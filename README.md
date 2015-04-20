This script takes an OSM file and parses it into edges, nodes, and geometry files, as described below.  It processes a 3.5 GB file in about 11 seconds.
##How to Use osm
- Place your osm file in the same directory as osm.py
- Run this command ```python osm.py [name-of-your-osm-file].osm```

##Nodes.txt

This text file contains the nodes of the road network. The file defines all nodes (basically intersections), with each row representing a single node and containing the following fields seperated by a single space:

    <NodeId> <lat> <long>

Where:

- ```<NodeId>```: An integer value specifying the unique identification number of the node within the road network.
- ```<lat>```: This value specifies the latitudinal location of the node within the road network in degrees.
- ```<long>```: This value specifies the longitudinal location of the node within the road network in degrees.
Example:
    81633740 33.074845 -97.322028

##Edges.txt

This text file contains the "rough" edges of the road network. Each row representing a single edge and contains four values separated by a single space.

    <EdgeId> <from> <to> <cost>

- ```<EdgeId>```: An integer value specifying the unique identification number of the edge within the road network. It is not related in any way to NodeId.
- ```<from>```: This value represents the id of the node that is at the head of the edge. If the edge is defined as (u,v), <from> is u. These node id values correspond to the <NodeId> values in Nodes.txt.
- ```<to>```: This value represents id of the node that is at the tail of the edge. If the edge is defined as (u,v), ```<to>``` is v. These node id values correspond to the ```<NodeId>``` values in Nodes.txt.
- ```<cost>```: This value defines the actual cost of a vehicle to traverse from one end of the edge to the other end. It is a cost function based on length of the edge and the speed limit on the road segment the edge represents.

Note that the road network graph is a directed graph. The edge that goes from node u to node v has a different ```<EdgeId>``` from the edge that goes in the other direction (from node v to node u).

##EdgeGeometry.txt

This text files contains the geometry data of each edge in the road network. The edge geometry makes a best attempt to define the polyline of the actual road that the edge is representing. Each row contains a minimum of eight values, with each value being separated by a caret (^). Each entry defines n different points along the edge by specifying the point’s latitude and longitude values. There will be more than eight values in a single entry if the entry contains longitude/latitude information about more than just the first and last points of the edge. The form of an edge geometry row is:

    <EdgeId>^<Name>^<Type>^<Length>^<Lat_1>^<Lon_1>^...^<Lat_n>^<Lon_n>

- ```<EdgeId>```: An integer value specifying the unique identification number of the edge within the road network. This value will match a single edge defined in the Edges.txt file.
- ```<Name>```: This value describes the real-world name of the road segment that this specific edge represents. If no name is defined, the attribute will contain an empty string.
- ```<Type>```: This value describes the type of road that is represented by the edge. Some common values are:
    - motorway
    - motorwaylink
    - primary
    - primarylink
    - secondary
    - secondarylink
    - tertiary
    - residential
    - livingstreet
    - service
    - trunk
    - trunk_link
    - unclassified

- ```<Length>```: This value is the length, in meters, of the edge.
- ```<Lat_1>```: This value is the latitude of the first point of the edge. 
If the edge is defined as (u,v), ```<Lat_1>``` is the latitude value of u.
- ```<Lon_1>```: This value is the longitude of the first point of the edge. 
If the edge is defined as (u,v), ```<Lon_1>``` is the longitude value of v.
....```<Lat_i><Lon_i>```....: The latitude and longitude values for several points between the first and the last points of the edge. These points are optional and the number of optional points varies according to the geometry of the represented edge.
- ```<Lat_n>``` : This value is the latitude of the last point of the edge. 
If the edge is defined as (u,v), ```<Lat_n>``` is the latitude value of v.
- ```<Lon_n>``` : This value is the longitude of the last point of the edge. 
If the edge is defined as (u,v), ```<Lon_n>``` is the longitude value of v.
