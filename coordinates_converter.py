# converting decimal degrees (° dec) to sexagesimal angle (dd.mmss,ss)
def dec_to_sangle(dec):
    deg, minute, second, dms = 0, 0, 0, 0
    deg = int(dec)
    minute = int((dec - deg) * 60)
    second = (((dec - deg) * 60) - minute) * 60
    dms = deg + (float(minute) / 100) + (second / 10000)
    return dms

# converting sexagesimal angle (dd.mmss,ss) to seconds
def sangle_to_seconds(dms):
    deg, minute, second, tot_seconds = 0, 0, 0, 0 
    deg = int(dms)
    minute = int((dms - deg) * 100)
    second = (((dms - deg) * 100) - minute) * 100
    tot_seconds = second + (minute * 60) + (deg * 3600)
    return tot_seconds

# converting LV95 to WGS84, returns lat and lng in Decimal degrees °
def lv95_to_wgs84(geomx, geomy):
    y_acute = float(geomx - 2600000)/1000000
    x_acute = float(geomy - 1200000)/1000000 
    l_acute = 2.6779094 + 4.728982 * y_acute + 0.791484 * y_acute * x_acute + 0.1306 * y_acute * pow(x_acute, 2 )- 0.0436 * pow(y_acute, 3)
    f_acute = 16.9023892 + 3.238272 * x_acute - 0.270978 * pow(y_acute, 2) - 0.002528 * pow(x_acute, 2) - 0.0447 * pow(y_acute, 2) * x_acute - 0.0140 * pow(x_acute, 3)
    dec_lng = round((l_acute * 100 / 36), 5)
    dec_lat = round((f_acute * 100 / 36), 5)
    return (dec_lat, dec_lng)

# converting decimal degrees (° dec) angle to LV95
def wgs84_to_lv95(lat_deg, lng_deg):
    f_acute = (sangle_to_seconds(dec_to_sangle(lat_deg)) - 169028.66) / 10000
    l_acute = (sangle_to_seconds(dec_to_sangle(lng_deg)) - 26782.5) / 10000
    geomx = 2600072.37 + 211455.93 * l_acute - 10938.51 * l_acute * f_acute - 0.36 * l_acute * pow(f_acute, 2) - 44.54 * pow(l_acute, 3) # E_m
    geomy = 1200147.07 + 308807.95 * f_acute + 3745.25 * pow(l_acute, 2) + 76.63 * pow(f_acute, 2) - 194.56 * pow(l_acute, 2) * f_acute + 119.79 * pow(f_acute, 3) # N_m
    return (geomx, geomy)

# lat and lng in decimal degrees to tile numbers
def deg2num(lat_deg, lng_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lng_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

# Tile numbers to lat and lng in decimal degrees
def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lng_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lng_deg)