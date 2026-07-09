import heapq
from graph import Graph
from typing import List, Dic, Any, Optional

class Pathfinding:
	def __init__(self):
		pass
	def find_short_path(self,
					 start_zone: Any,
					 end_zone: Any,
					 adjacency_list: Dic[str, List[Any]]
					 ) -> Optional[List[Any]]:
		
		distance = {(0.0, start_zone)}
		previous_nodes = {}