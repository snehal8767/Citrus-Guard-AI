# GIS

## Stack

Leaflet + react-leaflet with OpenStreetMap tiles. No API key, no cost, works offline with cached tiles.

## Data

- `data/geojson/zone_<A-H>.geojson` — per-zone polygons written by the seed script.
- `data/geojson/orchard_boundary.geojson` — estate boundary.
- The API serves zone centers (`latitude`/`longitude`); the frontend draws the matching 4×2 grid rectangles, so map and database can never disagree on zone positions.

## Zone styling

| Health | Colour |
|---|---|
| Healthy | `#4a8d3e` green |
| Watch | `#eab308` yellow |
| At Risk | `#f98707` citrus orange |
| Critical | `#dc2626` red |

Clicking a zone opens a popup + detail panel: name, health, risk score, area, center coordinates, latest sensor status, and the recommended action. Zone B is preselected so judges land on the story.

## Future field deployment

Replace grid rectangles with real surveyed polygons (drone orthomosaic → GeoJSON), served from a `geometry` column or the existing GeoJSON files.
