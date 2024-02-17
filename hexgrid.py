''' Base class for drawing hexagonal truchet grid to SVG '''

from xml.etree import ElementTree as ET
import math
import random


class HexGrid:
    ''' Hexagonal Grid for placing Truchet Tiles.

        Args:
            size: Number of tiles along one edge of the grid
            borders: Draw borders around each tile

        Class Attributes:
            TILEH: Height of one tile (point to point)
            TILEW: Width of one tile (flat to flat)
            EDGELEN: Length of a tile edge
            VERT_n: Coordinates of each tile vertex as string,
                where `n` is A through F.

        Tile coordinates:
            Coordinate (0, 0) is top left of bounding box
            surronding the tile. Vertices are labeled A through F,
            clockwise, with B the top center.

        Grid coordinates:
            (0, 0) is the center of the grid
    '''
    TILEH = 100
    TILEW = math.sqrt(3)/2 * TILEH
    EDGELEN = TILEH/2
    VERT_A = f'0 {TILEH/4}'
    VERT_B = f'{TILEW/2} 0'
    VERT_C = f'{TILEW} {TILEH/4}'
    VERT_D = f'{TILEW} {3*TILEH/4}'
    VERT_E = f'{TILEW/2} {TILEH}'
    VERT_F = f'0 {3*TILEH/4}' 

    def __init__(self, size: int, borders: bool = False):
        self.size = size
        self.tiles = []
        self.edgetiles = []
        self.cornertiles = []
        self.borders = borders

        width = self.TILEW * 2 * self.size - self.TILEW
        height = width * math.sqrt(3)/2

        self.svg = ET.Element('svg')
        self.svg.set('viewBox', f'{-width/2} {-height/2} {width} {height}')
        self.svg.set('width', f'{width}')
        self.svg.set('height', f'{height}')
        self.svg.set('xmlns', 'http://www.w3.org/2000/svg')
        self.svg.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')

    def _repr_svg_(self):
        ''' SVG representer for use in pyscript/jupyter '''
        return ET.tostring(self.draw())

    def _add_symbol(self, symbol: ET.Element):
        ''' Add a <symbol> to the SVG definitions '''
        if self.borders:
            border = ET.SubElement(symbol, 'path')
            border.set('d', f'M {self.VERT_A} L {self.VERT_B} {self.VERT_C} '
                            f'{self.VERT_D} {self.VERT_E} {self.VERT_F} Z')
            border.set('stroke', 'gray')
            border.set('fill', 'none')
        self.svg.append(symbol)

    def add_tile(self, symbol: ET.Element):
        ''' Add a symbol to the drawing. Symbol must be a
            <symbol> element with an `id` attribute, and may
            define any SVG drawing elements within.
        '''
        self.tiles.append(symbol)
        self._add_symbol(symbol)

    def add_edge_tile(self, symbol: ET.Element):
        ''' Add a symbol to the drawing for use along the grid edges.
            Symbol must be a <symbol> element with an `id` attribute,
            and may define any SVG drawing elemements within.
            Tile will be rotated to align edges `a` and `f` with the grid.
        '''
        self.edgetiles.append(symbol)
        self._add_symbol(symbol)

    def add_corner_tile(self, symbol: ET.Element):
        ''' Add a symbol to the drawing for use on the grid corners.
            Symbol must be a <symbol> element with an `id` attribute,
            and may define any SVG drawing elemements within.
            Tile will be rotated to align edge `a` with the grid.
        '''
        self.cornertiles.append(symbol)
        self._add_symbol(symbol)

    def draw(self) -> ET.Element:
        ''' Place all the tiles, randomly selecting tiles from
            the list of regular tiles, edge tiles, and corner tiles,
            and randomly applying rotation to the regular tiles.
        '''
        group = ET.SubElement(self.svg, 'g')
        for q in range(-self.size+1, self.size):
            for r in range(-self.size+1, self.size):
                if abs(q+r) > self.size-1: continue

                s = -q-r
                if max(abs(q), abs(r), abs(s)) == self.size-1:  # On the border
                    if (q==0 or r==0 or s==0) and len(self.cornertiles):  # On a corner
                        # There's probably more elegant ways to do this...
                        rotate = 0
                        if q == 0 and s == self.size-1:
                            rotate=4
                        elif s == 0 and q == self.size-1:
                            rotate=5
                        elif q == 0 and r == self.size-1:
                            rotate=1
                        elif r == 0 and s == self.size-1:
                            rotate=3
                        elif s == 0 and r == self.size-1:
                            rotate=2
                        tile = random.choice(self.cornertiles)
                        self._draw_tile(tile, q, r, rotate=rotate, zorder=0)

                    elif len(self.edgetiles):
                        rotate = 1
                        if r == self.size - 1:
                            rotate = 2
                        elif r == -self.size + 1:
                            rotate = -1
                        elif s == self.size - 1:
                            rotate = 4
                        elif q == -self.size + 1:
                            rotate = 3
                        elif q == self.size - 1:
                            rotate = 0
                        tile = random.choice(self.edgetiles)
                        self._draw_tile(tile, q, r, rotate=rotate)

                else:
                    tile = random.choice(self.tiles)
                    self._draw_tile(tile, q, r, rotate=random.randint(0, 5))
        return self.svg

    def _draw_tile(self, tile: ET.Element, q: int, r: int, rotate: int = 0,
                   zorder: int = 1):
        ''' Draw one tile in the grid

            Args:
                tile: The tile symbol to draw (added to svg via <use>)
                q: Diagonal coordinate for tile
                r: Horizontal coordinate for tile
                rotate: Rotation factor, integer from 0-4 (as multipler
                    of 60 degrees)
                zorder: Allow corner tiles to be placed underneath

            Note: See https://www.redblobgames.com/grids/hexagons/
                for description of (q, r) coordinate system.
        '''
        name = tile.get('id')
        group = self.svg.find('g')
        use = ET.Element('use')
        use.set('href', f'#{name}')
        use.set('xlink:href', f'#{name}')

        if zorder == 0:
            group.insert(0, use)
        else:
            group.append(use)

        # Convert axial to grid coordinates
        col = q + (r - r % 2) // 2
        row = r

        # Convert to x, y position
        x = col*self.TILEW + (row%2)*(self.TILEW/2) - self.TILEW/2
        y = row*(self.TILEH*3/4) - self.TILEH/2
        use.set('x', str(x))
        use.set('y', str(y))
        if rotate != 0:
            theta = rotate * 60
            use.set('transform', f'rotate({theta}, {x+self.TILEW/2} {y+self.TILEH/2})')

    def view_tiles(self) -> ET.Element:
        ''' Create an SVG showing each tile by itself '''
        gap = 15
        width = (self.TILEW + gap) * len(tiles)
        height = self.TILEH + gap

        svg = ET.Element('svg')
        svg.set('viewBox', f'0 0 {width} {height}')
        svg.set('width', f'{width}')
        svg.set('height', f'{height}')
        svg.set('xmlns', 'http://www.w3.org/2000/svg')
        svg.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')

        tiles = self.tiles + self.edgetiles + self.cornertiles
        for i, tile in enumerate(tiles):
            border = ET.SubElement(tile, 'path')
            border.set('d', f'M {self.VERT_A} L {self.VERT_B} {self.VERT_C} '
                            f'{self.VERT_D} {self.VERT_E} {self.VERT_F} Z')
            border.set('stroke', 'gray')
            border.set('fill', 'none')
            svg.append(tile)
            name = tile.get('id')
            use = ET.SubElement(svg, 'use')
            use.set('href', f'#{name}')
            use.set('xlink:href', f'#{name}')
            use.set('x', str(gap/2 + i*(self.TILEW + gap)))
            use.set('y', f'{gap/2}')
        return svg
