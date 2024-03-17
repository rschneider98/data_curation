# Philadelphia Groundwater Analysis for Data Curation Case Study

## Goal

We want to consume and integrate data from multiple upstream sources in order to analyze it as part of an active research model. This means we want to handle ingesting data in a consistent, conformed, controlled, and automated manner, so that it is available for researchers. We also want researchers to be able to consume this data and produce their own assets from this model. These assets will be used for the final research or by others.

## Analysis

### Managing Research Data

Research data that is actively worked on will go through many iterations and differences, so we want to track these as they are created to limit post-hoc documentation when writing and summarizing results. This will be managed through the research object crate to identify objects are they are written to a shared location. These RO metadata files will be stored as part of the Git repo, so as a process is peer-reviewed and merged, the final data can be "published" and referable by others as well through this metadata folder. This means that the process of review and tracking can be centralized while individuals work separately.

### Geography

Geographic data and math will be simplified by using geographically hashing to define a resolution and assigning the polygon/shape area to hexagons of different resolutions. These can be used to check inclusion/exclusion and distance much faster than otherwise allowable. This will possibly have some issues with how the different levels of data are integrated, but as long as assumptions are reasonable and documented, this seems like the best approach.

## Ingesting Data

Ingested data will either be pulled manually or automatically from a handful of data sources. These data sources will be identified with a research object crate and stored in a shared location and "published" to other researchers via Git. These ingested extracts will be transformed into a more analytically useful format by tidy-ing the columns and hashing geographical regions.

### United States Geological Survey (USGS) GroundWater Data

We are looking at the Philadelphia groundwater dataset provided by the USGS. This is a dataset created in tandem by the United States Geological Survey and the Philadelphia Water Department for the purpose on monitoring groundwater levels ([Philadelphia Area Groundwater Level Network](https://www.usgs.gov/data/philadelphia-area-groundwater-level-network)).


### OpenDataPhilly Complete Streets

Street types developed, identified, and mapped by the City Planning Commission along with center lines for streets. GeoJSON is downloadable from https://opendata.arcgis.com/datasets/ed90e9016aab4c429cb7dd8aef2a87a3_0.geojson with metadata defined [here](https://metadata.phila.gov/#home/datasetdetails/5543867320583086178c4f34/representationdetails/55438ac09b989a05172d0d6a/?view_287_per_page=50&view_287_page=1).


### OpenDataPhilly Land Use

The [land use dataset](https://opendataphilly.org/datasets/land-use/) is the planning department's classification for land use attributed to individual parcels of land. The metadata is defined [here](https://metadata.phila.gov/#home/datasetdetails/5543864420583086178c4e74/representationdetails/55438a7f9b989a05172d0cf3/).


### US 2020 Census Data

Block data for the US census was found using the interactive tooling with data.census.gov. Filtering to the County of Philadelphia, Pennsylvania and selecting Decennial Census for the Survey and Populations and People for the Topic, there is the DP1 dataset. This provides demographic data at a summary view of the county, but in order to get all census blocks, I had to first select all of the blocks in Pennsylvania and then include which Five Digit Zip Code that block was a part of. I was then able to download a CSV for this data.

Similarly, using the web interface for the Census, to find the 2020 Geographies, I went to this page: [https://www.census.gov/geographies/mapping-files/2020/geo/tiger-line-file.html](https://www.census.gov/geographies/mapping-files/2020/geo/tiger-line-file.html). From there, I selected the Web Interface for download, that I wanted 2020 Block Geographies for Pennsylvania, and then I filled out the rest of the form to have the CSV emailed to me.


### National Oceanic and Atmospheric Administration (NOAA) Weather Data

From NOAA's Weather and Climate Resources, there is the [Past Weather Dataset](https://www.ncdc.noaa.gov/cdo-web/datatools/lcd). I selected Philadelphia County, Pennsylvania and the two available stations are the Northeast Philadelphia Airport and the Philadelphia International Airport. From this, I selected Jan 1, 2015 - Dec 31, 2019 for the date ranges to observe.

## Tests

Tests are run with Tox.

Helpful commands:

- Run all tests and linting: `tox`
- Run a specific environment/tests: `tox -e <env>`
    - Example for flake8 linting: `tox -e lint`