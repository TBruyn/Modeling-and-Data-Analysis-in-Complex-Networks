import json
import networkx
import UserTrafficCollector
import TrafficCombiner
import TrafficGraphMediator

print("--------------------------------------------------------------------")
print("Traffic pipeline")
print("--------------------------------------------------------------------")
print("Collect traffic")
UserTrafficCollector
print()
print("Merge traffic files")
TrafficCombiner
print()
print("Create new traffic graph")
TrafficGraphMediator.create_graph()
TrafficGraphMediator.create_graph(
    outputfile='/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final/data/traffic_graph_half_1.json',
    inputfile='/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final/data/merged_traffic_array_half_1.json'
)
TrafficGraphMediator.create_graph(
    outputfile='/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final/data/traffic_graph_half_2.json',
    inputfile='/home/tim/Documents/Modeling-and-Data-Analysis-in-Complex-Networks/final/data/merged_traffic_array_half_2.json'
)
print()
print("Finished traffic pipeline")
print("Updated:")
print("\tmerged_traffic_graph_latest.json")
print("\tmerged_traffic_graph_half_1.json")
print("\tmerged_traffic_graph_half_2.json")
print("--------------------------------------------------------------------")