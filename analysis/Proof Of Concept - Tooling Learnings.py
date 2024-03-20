# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Exploration of Tools
#
# Want to be able to read in data of the various formats, process them into a consistent format, and register and manage the file's metadata

# %% [markdown]
# # GeoJSON, H3, and Shapely

# %%
import geojson
import h3
import shapely

# %%
with open("../data/extract/OpenDataPhillyCompleteStreets.geojson", "r") as f:
    streets = geojson.load(f)

# %%
streets.keys()

# %%
streets["features"][0].keys()

# %%
streets["features"][0]["geometry"]

# %%
shapely.geometry.shape(streets["features"][0]["geometry"])

# %%
longitude, latitude = streets["features"][0]["geometry"]["coordinates"][0]
longitude, latitude

# %%
h3.geo_to_h3(latitude, longitude, 3)

# %%
for longitude, latitude in streets["features"][0]["geometry"]["coordinates"]:
    print(h3.geo_to_h3(latitude, longitude, 15))

# %%
new_geom = {"coordinates": [streets["features"][0]["geometry"]["coordinates"]], "type": "MultiPolygon"}
new_geom

# %%
streets["features"][0]["properties"]

# %% [markdown]
# # Shapefile (Fiona), H3, and Shapely

# %%
import fiona
import h3
import shapely

# %%
src = fiona.open("../data/extract/tl_2023_42_tabblock20/tl_2023_42_tabblock20.shp") 

# %%
print(src.schema)

# %%
print(src.crs)

# %%
dict(src[0].properties)

# %%
src[0].geometry.coordinates

# %%
geom = src[0].geometry

# %%
geom.type

# %%
geom.coordinates[0]

# %%
polygon = {
    "type": "Polygon",    
    "coordinates": [
        [
            [37.813318999983238, -122.4089866999972145],
            [37.7198061999978478, -122.3544736999993603],
            [37.8151571999998453, -122.4798767000009008],
            [37.813318999983238, -122.4089866999972145],
        ]
    ]
}

# %%
shapely.geometry.shape(polygon)

# %%
h3.polyfill(polygon, 7)

# %%
dict(geom)

# %%
shapely.geometry.shape(dict(geom))

# %%
h3.polyfill(dict(geom), 15)

# %%
src.close()

# %% [markdown]
# # Research Object Creation
#
# Attributes we care about
#
# - Authorship
# - Timestamps
# - File(s)
#   - Name
#   - Format
# - Upstream dependencies
# - Workflow/processes

# %% [markdown]
# Dataset Descriptions
#
# Use attributes and entities as needed
#
# - Attributes
#     - name
#     - publisher {"@id": "#local_id"} or {"@id": "url"}
#     - creater {"@id": "#person"}
#     - license
#     - datePublished
#     - keywords (ex. "streets, aggregated features, map")
#     - mainEntity Output Dataset 
# - Data Entities
#     - File
#         - source (File(s))
#         - description
#         - contentSize (MB, KB, or B)
#         - encodingFormat (from PRONOM: https://www.nationalarchives.gov.uk/PRONOM)
#         - sha256
#     - Dataset
#         - source (File(s))
#         - description
#         - contentSize (MB, KB, or B)
#         - encodingFormat (from PRONOM: https://www.nationalarchives.gov.uk/PRONOM)
#     - ComputationalWorkflow
#         - @type (pre-defined with built-in models) ["File", "SoftwareSourceCode", "ComputationalWorkflow"]
#         - source (File)
#         - author
#         - programmingLanguage
#         - input [{"@id": "#id1"}, {"@id": "#id2"}]
#         - output [{"@id": "#id3"}]
# - Contextual Entities
#     - Publisher
#         - @type Organization
#         - name
#         - url
#     - Person
#         - name
#     - programmingLanguage
#         - @type ["ComputerLanguage", "SoftwareApplication"]
#         - name
#         - version
#         - url
#     - encodingFormat
#         - @id PRONOM url
#         - @type Website
#         - name
#     - input
#         - @type FormalParameter
#         - name
#         - defaultValue {"@id": "#ReferenceToUpstreamDataset"}
#         - encodingFormat
#         - valueRequired True
#     - output
#         - @type FormalParameter
#         - name
#         - defaultValue {"@id": "#ReferenceToDownstreamDataset"}
#         - encodingFormat
#         - valueRequired True

# %%
from rocrate.rocrate import ROCrate
from rocrate.model import (
    Person,
    File,
    Dataset,
    ComputationalWorkflow,
    ContextEntity,
)

# %% [markdown]
# Dataset
#     source=source,
#     dest_path=dest_path,
#     fetch_remote=fetch_remote,
#     validate_url=validate_url,
#     properties=properties
#
# properties?
#
#

# %%
from pip._internal.operations import freeze

# %%
pkgs = list(freeze.freeze())
[pkg for pkg in pkgs if "polars" in pkg]

# %%
e = ContextEntity(
    crate,
    identifier="polars",
    properties={
        "@type": ["ComputerLanguage", "SoftwareApplication"],
        "name": "Polars 0.20.15",
        "version": "0.20.15",
        "url": "https://pypi.org/project/polars/0.20.15/",
    },
)

# %%
w = ComputationalWorkflow(
    crate,
    source="tmp/polars_transformation.json",
    properties={
        "author": {"@id": "#AA"},
        "programmingLanguage": {"@id": "#polars"},
    }
)

# %%
d = Dataset(
    crate,
    source="../data/extract/OpenDataPhillyCompleteStreets.geojson",
    properties={
        "description": "Data of centerlines of philly streets lines",
        "contentSize": "120",
        "encodingFormat": ["application/geo+json", {"@id": "https://www.nationalarchives.gov.uk/PRONOM/fmt/1367"}],
    }
)

# %%
f1 = File(
    crate,
    source="../data/extract/tl_2023_42_tabblock20/tl_2023_42_tabblock20.shp",
    properties={
        "description": "Shapefile for TIGER 20 Blocks in Philadelphia County, Pennsylvania",
        "contentSize": "352MB",
        "encodingFormat": "some URL",
        "sha256": "Will Format Later",
    }
)

# %%
d = Dataset(
    crate,    
    source="../data/extract/tl_2023_42_tabblock20",
    properties={
        "description": "Shapes and names of census blocks",
        "hasParts": [
            {"@id": "#tl_2023_42_tabblock20.shp"},
        ]
    }
)

# %%
new_crate = crate.add(
    d
)

# %%
new_crate

# %%
d.properties()

# %%
crate.data_entities

# %% [markdown]
# Crate properties:
#
# - name
# - datePublished
# - creator
# - license
# - description
# - keywords
# - publisher
# - isBasedOn
# - mainEntity
#
# Crate functions:
#
# - add_file
# - add_dataset
# - add

# %%

# %%
import datetime as dt

# %%
crate = ROCrate()

# %%
# Time
timestamp = dt.datetime.now()

# %%
crate.datePublished = timestamp

# %%
crate.datePublished

# %%

# %%
crate.contextual_entities

# %%
crate.data_entities

# %%
dt.datetime.now().isoformat()

# %%
alice_info = {
    "id": "AA",
    "name": "Alice Doe",
}

# %%
alice = crate.add(
    Person(
        crate,
        alice_info["id"],
        properties={"name": alice_info["name"]},
    )
)

# %%
crate.write("../metastore/test_crate/")

# %%
for e in crate.get_entities():
    print(e.id, e.type)

# %%
crate.get_by_type(alice)

# %%
alice

# %%
