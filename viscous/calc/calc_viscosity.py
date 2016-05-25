def eastern_boundaries(lon,lat):
    m = Basemap(projection='cyl')
    boundaries = []
    last_l_is_land = m.is_land(lon[0],lat)
    for l in lon[1:]:
        current_l_is_land = m.is_land(l,lat)
        if last_l_is_land and not current_l_is_land:
            boundaries.append(l)
        last_l_is_land = current_l_is_land

    return boundaries

def calculate_coefficients(z,lon,lats,target_lat,dt,c1,c2,c3,c4,c5,c6,c7):
    # Constants, defined as in CCSM
    EARTH_RADIUS = 6370.0E3
    OMEGA = 7.292123625E-5
    PI = 4*math.atan(1)

    lat_i = find_nearest(lats, target_lat)
    lat = lats[lat_i]

    dlon = np.abs(lon[1] - lon[0])
    dx = dlon * EARTH_RADIUS / 180 * PI * math.cos(lat / 180 * PI)
    try:
        dlat = np.diff(lats)[lat_i]
    except IndexError:
        dlat = np.diff(lats)[-1]
    dy = dlat * EARTH_RADIUS / 180 * PI

    phip = PI * min(np.abs(lat),c7) / c7
    ASGS = c6
    BSGS = c1*(1+c2*(1-math.cos(phip)))
    if np.abs(lat) < 30:
        VS = 0.425 * np.cos(lat*PI/30) + 0.575
    else:
        VS = 0.15
    #AGRe = 0.5 * VS * np.exp(-z/1000) * dx
    AGRe = 0

    p = []
    boundaries = eastern_boundaries(lon,lat)
    for x in lon:
        boundary_distance = np.Inf
        in_boundary_layer = False
        for boundary in boundaries:
            if (x - c5*dlon <= boundary) & (x >= boundary):
                p_x = 0
                in_boundary_layer = True
            elif x >= boundary:
                boundary_distance = min(np.abs(x - boundary - c5*dlon),boundary_distance)
        if not in_boundary_layer:
            p_x = boundary_distance * c4 * EARTH_RADIUS / 180 * PI * math.cos(lat / 180 * PI)
        p.append(p_x)

    beta = 2 * OMEGA / EARTH_RADIUS * math.cos(lat * PI / 180)
    BMUNK = c3 * beta * dx**3 * np.exp(-np.asarray(p)**2)
    ANoise = [max(AGRe,x) for x in BMUNK]
    BNoise = ANoise
    Ap = [max(ASGS,x) for x in ANoise]
    Bp = [max(BSGS,x) for x in BNoise]
    AVCFL = 0.125 / (dt * (1/dx/dx + 1/dy/dy))
    BVCFL = AVCFL
    A = [min(AVCFL,x) for x in Ap]
    B = [min(BVCFL,x) for x in Bp]
    return np.asarray(A)/1E3, np.asarray(B)/1E3

