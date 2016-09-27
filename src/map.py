class Map:
	def __init__(self, buildarea, strategy):
		self.width = int(buildarea[0])
		self.height = int(buildarea[1])
		self.strategy = strategy
		self.map = [[0 for j in range(self.width)] for i in range(self.height)]
		
	def mark(self, sx, sy, width, height):
		for x in range(int(width)):
			for y in range(int(height)):
				if sx+x >= 0 and sx+x < self.width and sy+y >= 0 and sy+y <self.height:
					self.map[sx+x][sy+y] = 1
					
	def fits(self, x, y, width, height):
		for dx in range(int(width)):
			for dy in range(int(height)):
				if self.map[x+dx][y+dy] != 0:
					return False
		return True
					
	def find(self, width, height):
		if self.strategy == "row":
			for y in range(int(self.height-height)):
				for x in range(int(self.width-width)):
					if self.fits(x, y, width, height):
						return (x,y)
		else: # strategy assumed to be "column"
			for x in range(int(self.width-width)):
				for y in range(int(self.height-height)):
					if self.fits(x, y, width, height):
						return (x,y)

		return (None, None)