import json

class Map_Loader:
	def __init__(self):
		self.map_data = []
		self.light_orb = []
		self.spawn_point = []
		self.foliage = []
		self.outer_tiles = []
		self.tile_map = []

	def Load(self,path):
		with open(f'{path}') as file:
			tile_data = json.load(file)

		for key in tile_data:
			for list in tile_data[key]:
				for data in list:
					if data != [-1]:
						self.map_data.append(data)
		
		for list in self.map_data:
			if list[1] == 'entity' and list[2] == '0.png':
				self.spawn_point.append([list[3],list[4]])
			elif list[1] == 'entity' and list[2] == '1.png':
				self.light_orb.append([list[3],list[4]])
			elif list[0] == 0:
				self.outer_tiles.append(list)
			else:
				self.tile_map.append(list)

		for list in self.tile_map:
			if list[1] == 'foliage':
				self.foliage.append(list)

# map_data = Map_Loader().Load('map/map0.json')
