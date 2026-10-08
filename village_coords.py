"""Village locations for the coverage map.

Coordinates are the GeoNames populated-place points (degrees, minutes, seconds),
looked up on geonames.org in October 2026. Qoubbei is listed there as
"Qoubbeyaa" (قبيع); search GeoNames by the Arabic name when a spelling fails.
"""

DMS = {
    # name: ((lat d, m, s), (lon d, m, s))
    "Arsoun": ((33, 51, 35), (35, 41, 20)),
    "Bhamdoun": ((33, 48, 31), (35, 39, 35)),
    "Bmariam": ((33, 49, 53), (35, 43, 5)),
    "Btebyat": ((33, 50, 8), (35, 42, 28)),
    "Btekhnay": ((33, 50, 28), (35, 43, 6)),
    "Bzebdine": ((33, 52, 17), (35, 43, 54)),
    "Chbaniyeh": ((33, 49, 16), (35, 42, 25)),
    "Deir El Harf": ((33, 50, 53), (35, 41, 18)),
    "Dlaibeh": ((33, 52, 42), (35, 41, 8)),
    "Falougha": ((33, 50, 16), (35, 44, 27)),
    "Hammana": ((33, 49, 33), (35, 44, 5)),
    "Jouar El Haouz": ((33, 51, 46), (35, 45, 34)),
    "Kfar Selouan": ((33, 51, 23), (35, 46, 45)),
    "Khalwet": ((33, 50, 27), (35, 44, 11)),
    "Khraybeh": ((33, 49, 34), (35, 42, 47)),
    "Kornayel": ((33, 51, 19), (35, 43, 35)),
    "Qalaa": ((33, 50, 23), (35, 43, 48)),
    "Qortada": ((33, 51, 35), (35, 37, 25)),
    "Qoubbei": ((33, 48, 49), (35, 41, 47)),
    "Qraiyeh": ((33, 48, 25), (35, 40, 34)),
    "Qseibe": ((33, 52, 0), (35, 39, 4)),
    "Ras El Maten": ((33, 50, 52), (35, 39, 52)),
    "Salima": ((33, 52, 23), (35, 41, 46)),
    "Saoufar": ((33, 48, 8), (35, 41, 56)),
}


def deg(dms):
    d, m, s = dms
    return d + m / 60 + s / 3600


COORDS = {name: (deg(lat), deg(lon)) for name, (lat, lon) in DMS.items()}
