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
print()
print("Finished traffic pipeline")
print("--------------------------------------------------------------------")