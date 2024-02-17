''' Customize and draw the hexagonal Truchet tile image '''
from typing import Sequence
import math
from xml.etree import ElementTree as ET
from hexgrid import HexGrid


# Centers of each tile edge
a = f'0 {HexGrid.TILEH/2}'
b = f'{HexGrid.TILEW/4} {HexGrid.TILEH/8}'
c = f'{3*HexGrid.TILEW/4} {HexGrid.TILEH/8}'
d = f'{HexGrid.TILEW} {HexGrid.TILEH/2}'
e = f'{3*HexGrid.TILEW/4} {7*HexGrid.TILEH/8}'
f = f'{HexGrid.TILEW/4} {7*HexGrid.TILEH/8}'

# Centers with overlap extensions to avoid gap in adjacent SVG shapes
# that most SVG renderers seem to leave behind
ext = 1
ext60 = ext * math.sin(math.radians(60))
a_ = f'{-ext} {HexGrid.TILEH/2}'
b_ = f'{HexGrid.TILEW/4-ext/2} {HexGrid.TILEH/8-ext60}'
c_ = f'{3*HexGrid.TILEW/4+ext/2} {HexGrid.TILEH/8-ext60}'
d_ = f'{HexGrid.TILEW+ext} {HexGrid.TILEH/2}'
e_ = f'{3*HexGrid.TILEW/4+ext/2} {7*HexGrid.TILEH/8+ext60}'
f_ = f'{HexGrid.TILEW/4-ext/2} {7*HexGrid.TILEH/8+ext60}'

# Double extensions for the thin lines so they overlap the wide lines
a__ = f'{-ext*2} {HexGrid.TILEH/2}'
b__ = f'{HexGrid.TILEW/4-ext} {HexGrid.TILEH/8-ext60*2}'
c__ = f'{3*HexGrid.TILEW/4+ext} {HexGrid.TILEH/8-ext60*2}'
d__ = f'{HexGrid.TILEW+ext*2} {HexGrid.TILEH/2}'
e__ = f'{3*HexGrid.TILEW/4+ext} {7*HexGrid.TILEH/8+ext60*2}'
f__ = f'{HexGrid.TILEW/4-ext} {7*HexGrid.TILEH/8+ext60*2}'


def path(start, end, color: str, stroke: str) -> ET.Element:
    ''' Get SVG path element connecting start and end '''
    line = ET.Element('path')
    line.set('d', pathd(start, end))
    line.set('stroke', color)
    line.set('stroke-width', stroke)
    line.set('fill', 'none')
    return line


def pathd(start: tuple[float, float], end: tuple[float, float]) -> str:
    ''' Get SVG path `d` parameter connecting start and end coordinates '''
    return {
        (a_, f_): f'M {a_} L {a} A {HexGrid.EDGELEN/2} {HexGrid.EDGELEN/2} 0 0 1 {f} L {f_}',
        (b_, c_): f'M {b_} L {b} A {HexGrid.EDGELEN/2} {HexGrid.EDGELEN/2} 0 0 0 {c} L {c_}',
        (d_, e_): f'M {d_} L {d} A {HexGrid.EDGELEN/2} {HexGrid.EDGELEN/2} 0 0 0 {e} L {e_}',
        (c_, d_): f'M {c_} L {c} A {HexGrid.EDGELEN/2} {HexGrid.EDGELEN/2} 0 0 0 {d} L {d_}',
        (b_, e_): f'M {b_} L {e_}',
        (a_, d_): f'M {a_} L {d_}',
        (c_, f_): f'M {c_} L {f_}',
        (a_, c_): f'M {a_} L {a} Q {HexGrid.TILEW/2} {HexGrid.TILEW/2} {c} L {c_}',
        (b_, f_): f'M {b_} L {b} Q {HexGrid.TILEW/2} {HexGrid.TILEW/2} {f} L {f_}',
        (a_, None): f'M {a_} L {HexGrid.TILEW/8} {HexGrid.TILEH/2}',

        (a__, f__): f'M {a__} L {a} A {HexGrid.EDGELEN/2} {HexGrid.EDGELEN/2} 0 0 1 {f} L {f__}',
        (b__, c__): f'M {b__} L {b} A {HexGrid.EDGELEN/2} {HexGrid.EDGELEN/2} 0 0 0 {c} L {c__}',
        (d__, e__): f'M {d__} L {d} A {HexGrid.EDGELEN/2} {HexGrid.EDGELEN/2} 0 0 0 {e} L {e__}',
        (c__, d__): f'M {c__} L {c} A {HexGrid.EDGELEN/2} {HexGrid.EDGELEN/2} 0 0 0 {d} L {d__}',
        (b__, e__): f'M {b__} L {e__}',
        (a__, d__): f'M {a__} L {d__}',
        (c__, f__): f'M {c__} L {f__}',
        (a__, c__): f'M {a__} L {a} Q {HexGrid.TILEW/2} {HexGrid.TILEW/2} {c} L {c__}',
        (b__, f__): f'M {b__} L {b} Q {HexGrid.TILEW/2} {HexGrid.TILEW/2} {f} L {f__}',
        (a, None): f'M {a} L {HexGrid.TILEW/8} {HexGrid.TILEH/2}',
    }.get((start, end))


def basesymbol(name: str) -> ET.Element:
    ''' Get SVG <symbol> to build different tiles on '''
    symbol = ET.Element('symbol')
    symbol.set('id', name)
    symbol.set('width', str(HexGrid.TILEW))
    symbol.set('height', str(HexGrid.TILEH))
    return symbol


def build_hex(
        size: int = 9,
        widestroke: str = str(HexGrid.TILEW/2 - 6),
        thinstroke: str = '12',
        widecolor: str = 'black',
        thincolor: str = 'white',
        border: bool = False,
        tiles: Sequence[int] = (1,2,3,4)) -> HexGrid:
    ''' Build a Hex Truchet Tile image

        Args:
            size: Number of tiles across one edge
            widestroke: Width of lower path
            thinstroke: Width of upper path
            widecolor: Color of lower path
            thincolor: Color of upper path
            border: Draw borders around each tile
            tiles: Number of tiles to include in the image
    '''
    dwg = HexGrid(size=size, borders=border)

    if 1 in tiles:
        tile1 = basesymbol('tile1')
        tile1.append(path(a_, f_, widecolor, widestroke))
        tile1.append(path(a__, f__, thincolor, thinstroke))
        tile1.append(path(b_, c_, widecolor, widestroke))
        tile1.append(path(b__, c__, thincolor, thinstroke))
        tile1.append(path(d_, e_,  widecolor, widestroke))
        tile1.append(path(d__, e__,  thincolor, thinstroke))
        dwg.add_tile(tile1)

    if 2 in tiles:
        tile2 = basesymbol('tile2')
        tile2.append(path(a_, f_, widecolor, widestroke))
        tile2.append(path(a__, f__, thincolor, thinstroke))
        tile2.append(path(c_, d_, widecolor, widestroke))
        tile2.append(path(c__, d__, thincolor, thinstroke))
        tile2.append(path(b_, e_, widecolor, widestroke))
        tile2.append(path(b__, e__, thincolor, thinstroke))
        dwg.add_tile(tile2)

    if 3 in tiles:
        tile3 = basesymbol('tile3')
        tile3.append(path(a_, d_, widecolor, widestroke))
        tile3.append(path(a__, d__, thincolor, thinstroke))
        tile3.append(path(b_, e_, widecolor, widestroke))
        tile3.append(path(b__, e__, thincolor, thinstroke))
        tile3.append(path(c_, f_, widecolor, widestroke))
        tile3.append(path(c__, f__, thincolor, thinstroke))
        dwg.add_tile(tile3)

    if 4 in tiles:
        tile4 = basesymbol('tile4')
        tile4.append(path(a_, c_, widecolor, widestroke))
        tile4.append(path(a__, c__, thincolor, thinstroke))
        tile4.append(path(b_, f_, widecolor, widestroke))
        tile4.append(path(b__, f__, thincolor, thinstroke))
        tile4.append(path(d_, e_, widecolor, widestroke))
        tile4.append(path(d__, e__, thincolor, thinstroke))
        dwg.add_tile(tile4)

    # Tile to go on edges of big hexagon
    tile_edge = basesymbol('edge')
    tile_edge.append(path(a_, f_, widecolor, widestroke))
    tile_edge.append(path(a__, f__, thincolor, thinstroke))
    dwg.add_edge_tile(tile_edge)

    # Tile to go on corners of big hexagon
    tile_corner = basesymbol('corner')
    tile_corner.append(path(a_, None, widecolor, widestroke))
    tile_corner.append(path(a, None, thincolor, thinstroke))
    for p in tile_corner.findall('path'):
        p.set('stroke-linecap', 'round')
    dwg.add_corner_tile(tile_corner)
    return dwg


if __name__ == '__main__':
    
    # -- change parameters here --
    dwg = build_hex(
        size=9,             # Number of tiles across an edge
        widestroke='36',    # Width of lower stroke
        thinstroke='8',     # Width of upper stroke
        widecolor='black',  # Color of lower stroke
        thincolor='white',  # Color of upper stroke
        border=False,       # Draw borders around each tile
        tiles=(1,2,3,4))    # Remove numbers to disable that tile

    with open('hexagon.svg', 'w') as f:
        f.write(ET.tostring(dwg.draw(), encoding='unicode'))

    # Uncomment this to preview each tile by themselves
    #with open('tiles.svg', 'w') as f:
    #    f.write(ET.tostring(dwg.view_tiles()).deocde('utf-8'))
