import globalmaptiles as gmapt
import math

def mapSectors(sector_list, lat, lon, zoom):
    gm = gmapt.GlobalMercator()

    mx, my = gm.LatLonToMeters(lat, lon)
    px, py = gm.MetersToPixels(mx, my, zoom)

    # This can produce a grid such that:
    #
    #     [-------------length------------]
    #
    # (-px/2, py/2)                       (px/2, py/2)
    #     ---------------------------------
    #     |               |               |
    #     |               |               |
    #     |               |               |
    #     |               |               |
    #     |               |(lat,lon)      |
    #     ---------------------------------
    #     |               |               |
    #     |               |               |
    #     |               |               |
    #     |               |               |
    #     |               |               |
    #     ---------------------------------
    # (-px/2, -py/2)                      (px/2, -py/2)
    #
    # Thus we can calculate sectors to scrape

    # Longest side of the map in pixels, very conservative
    length = 1400
    # Approx diff between length and other map side length
    width_diff = 500
    # Quadrant and sector side lengths (squares)
    quadrant = length / 2
    sector_size = quadrant / 4
    # Top left (x,y) of map
    top_left_x = px - quadrant
    top_left_y = py + quadrant
    # List of spurious coords (mapped to ocean, forests etc.)
    spurious_x = [(3,0), (3,1), (3,7),
                  (4,0), (4,1), (4,7),
                  (7,0), (8,0), (9,0), (10,0), (11,0), (12,0)]
    # The ranges are derived from visual inspection of the resulting lat,lon grid
    # View the grid by pasting contents of sector_list.txt into input box
    #   at: http://www.darrinward.com/lat-long/
    # width_diff is used to approximate differences in overlap between
    #   calculated positions, as maps are displayed centered instead of from
    #   the top left corner (which crops part of the map off, decreasing listings)
    for i in range(3, 13):
        pos_y = top_left_y - (i * (sector_size - (width_diff / 7)))
        for j in range(0, 8):
            # Removes spurious positions
            spurious_flag = 0
            for coord in spurious_x:
                if i == coord[0] and j == coord[1]:
                    spurious_flag = 1
            # If screen position is a one we want to look at, calculate lat, lon
            if spurious_flag != 1:
                pos_x = top_left_x + (j * sector_size)
                center_x, center_y = (pos_x + (sector_size / 2)), (pos_y - (sector_size / 2))
                p2mx, p2my = gm.PixelsToMeters(center_x, center_y, zoom)
                m2lx, m2ly = gm.MetersToLatLon(p2mx, p2my)
                sector_pos = {
                    "latitude":     m2lx,
                    "longitude":    m2ly
                }
                sector_list.append(sector_pos)

    with open('./sector_list.txt', 'w') as fout:
        for sector in sector_list:
            fout.write(str(sector['latitude'])+","+str(sector['longitude'])+"\n")
    return sector_list
