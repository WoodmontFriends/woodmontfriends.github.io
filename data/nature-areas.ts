// Areas covered by the park nature map, traced in Google My Maps ("Woodmont Boundaries").
// The map shows only sightings inside at least one area, and searches iNaturalist
// using the box around all of them. Rings are [longitude, latitude] pairs, as in KML.
export type NatureArea = {
  id: string
  name: string
  style: 'park' | 'outline'
  ring: [number, number][]
}

const parse = (coords: string) =>
  coords.trim().split(/\s+/).map(p => p.split(',').map(Number) as [number, number])

export const NATURE_AREAS: NatureArea[] = [
  {
    id: 'park',
    name: 'Woodmont Park',
    style: 'park',
    ring: parse(`
      -77.587457,37.525002 -77.587259,37.524865 -77.584365,37.52471 -77.584353,37.524898
      -77.58503,37.525151 -77.585638,37.525502 -77.586169,37.527339 -77.585916,37.527993
      -77.586739,37.528097 -77.587275,37.525247 -77.587457,37.525002`),
  },
  {
    id: 'neighborhood',
    name: 'Woodmont neighborhood',
    style: 'outline',
    ring: parse(`
      -77.599323,37.525716 -77.598666,37.525564 -77.582131,37.524627 -77.581809,37.532351
      -77.587384,37.533185 -77.589056,37.533261 -77.590727,37.53327 -77.59227,37.532776
      -77.593641,37.532147 -77.59544,37.530581 -77.599957,37.526421 -77.599323,37.525716`),
  },
  {
    id: 'watershed',
    name: 'Community centers & watershed',
    style: 'outline',
    ring: parse(`
      -77.600128,37.524848 -77.59784,37.524849 -77.59543,37.524372 -77.593067,37.524083
      -77.592271,37.523479 -77.590672,37.523381 -77.590408,37.523962 -77.590041,37.524388
      -77.589385,37.524482 -77.586332,37.524257 -77.585084,37.524536 -77.583538,37.52425
      -77.583086,37.523749 -77.583503,37.523682 -77.58392,37.523785 -77.584797,37.523957
      -77.585392,37.523926 -77.586152,37.523831 -77.587029,37.523763 -77.587553,37.523652
      -77.587906,37.523984 -77.588543,37.523881 -77.589046,37.523845 -77.589405,37.523431
      -77.590226,37.522523 -77.589467,37.522358 -77.588744,37.522838 -77.587921,37.522737
      -77.586201,37.522533 -77.585362,37.522142 -77.582797,37.522644 -77.582108,37.523284
      -77.579316,37.523549 -77.578928,37.52304 -77.57691,37.522853 -77.574892,37.522939
      -77.572162,37.52312 -77.570977,37.522075 -77.570668,37.522046 -77.570041,37.522712
      -77.569157,37.523276 -77.570538,37.524758 -77.572526,37.524727 -77.574743,37.52429
      -77.57626,37.524268 -77.576675,37.524666 -77.576734,37.525037 -77.577279,37.525318
      -77.579057,37.525304 -77.582099,37.525648 -77.58242,37.524744 -77.584365,37.52471
      -77.584336,37.525004 -77.58503,37.525151 -77.585638,37.525502 -77.586123,37.52748
      -77.585916,37.527993 -77.586739,37.528097 -77.587071,37.526672 -77.587275,37.525247
      -77.587742,37.52508 -77.595378,37.525404 -77.599368,37.52543 -77.601383,37.525116
      -77.600128,37.524848`),
  },
]

// Box around every area, for the iNaturalist search and the map's starting view.
export const NATURE_BOUNDS = (() => {
  const pts = NATURE_AREAS.flatMap(a => a.ring)
  return {
    swlat: Math.min(...pts.map(p => p[1])),
    swlng: Math.min(...pts.map(p => p[0])),
    nelat: Math.max(...pts.map(p => p[1])),
    nelng: Math.max(...pts.map(p => p[0])),
  }
})()

// Standard ray-casting point-in-polygon test.
export function inArea(lng: number, lat: number, area: NatureArea) {
  const r = area.ring
  let inside = false
  for (let i = 0, j = r.length - 1; i < r.length; j = i++) {
    const [xi, yi] = r[i]
    const [xj, yj] = r[j]
    if ((yi > lat) !== (yj > lat) && lng < ((xj - xi) * (lat - yi)) / (yj - yi) + xi) inside = !inside
  }
  return inside
}
