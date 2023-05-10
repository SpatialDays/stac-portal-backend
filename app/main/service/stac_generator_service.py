import re
from datetime import datetime
import mimetypes

import pystac
from flask import current_app
from pyproj import CRS
from rasterio.warp import transform_bounds
from shapely.geometry import Polygon

stac_extensions = {
    "eo": "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
    "proj": "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
    "view": "https://stac-extensions.github.io/view/v1.0.0/schema.json",
}


def create_STAC_Item(metadata):
    # EPSG (Source and destination)
    src_crs = return_epsg_from_wkt(metadata["staticVariables"]["wkt"])
    destination_crs = "epsg:4326"  # All STAC Items are in EPSG:4326

    # Converted Geoms
    wgs84_grouped_geom = return_geom_from_multiple_geom(
        metadata["groupedVariables"]["wgs84_geom"]
    )
    wgs84_bbox = return_bbox_from_geom(wgs84_grouped_geom, src_crs, destination_crs)
    wgs84_geom = return_geom_from_bbox(wgs84_bbox)

    # Original Geoms
    original_grouped_geom = return_geom_from_multiple_geom(
        metadata["groupedVariables"]["proj_geom"]
    )
    original_bbox = return_bbox_from_coordinates(
        original_grouped_geom, src_crs, src_crs
    )

    # Required fields
    id = metadata["staticVariables"]["id"]
    time_acquired = datetime.strptime(
        metadata["staticVariables"]["time_acquired"], "%Y-%m-%dT%H:%M:%S.%fZ"
    )

    # Properties
    properties = {
        "proj:bbox": original_bbox,
        "proj:epsg": src_crs,
    }
    # Call the appropriate parser to extend the properties

    additional_stac_parser(properties, metadata)

    # Instantiate pystac item
    item = pystac.Item(
        id=id,
        geometry=wgs84_geom,
        bbox=wgs84_bbox,
        datetime=time_acquired,
        properties=properties,
    )

    connection_string = current_app.config["AZURE_STORAGE_CONNECTION_STRING"]
    # split the connection string by ;
    account_key = connection_string.split("AccountKey=")[1].split(";")[0]
    connection_string_split = connection_string.split(";")
    azure_params = {}
    for param in connection_string_split:
        param_split = param.split("=")
        azure_params[param_split[0]] = param_split[1]
    azure_params["AccountKey"] = account_key
    account_name = azure_params["AccountName"]
    endpoint_suffix = azure_params["EndpointSuffix"]
    blob_url = f"https://{account_name}.blob.{endpoint_suffix}"

    for asset in metadata["assets"]:
        # Remove extension from asset name
        name = re.sub(r"\.[^.]*$", "", asset["filename"])

        href = (asset["href"],)
        href = href[0]

        # if the href does not begin with blob_url, prepend it
        if not href.startswith(blob_url):
            # if href starts does not start with slash add it
            if not href.startswith("/"):
                href = "/" + href
            href = blob_url + href

        item.add_asset(
            key=name,
            asset=pystac.Asset(
                href=href,
                media_type=asset["type"],  # TODO: Convert to pystac.MediaType
                extra_fields={
                    "eo:bands": asset["bands"],
                    "proj:shape": asset["shape"],
                    "proj:transform": asset["transform"],
                },
            ),
        )

    # Generate thumbnail
    thumbnail = generate_thumbnail(metadata)
    if thumbnail:
        thumbnail_href = generate_url(
            thumbnail["name"],
            metadata["staticVariables"]["url"].split("/")[0:-1],
            account_name,
            endpoint_suffix,
        )

        item.add_asset(
            key="thumbnail",
            asset=pystac.Asset(
                href=thumbnail_href,
                media_type=thumbnail["type"],
            ),
        )

    for other_asset in metadata["otherAssets"]:
        href = generate_url(
            other_asset["name"],
            metadata["staticVariables"]["url"].split("/")[0:-1],
            account_name,
            endpoint_suffix,
        )

        if not other_asset["type"]:
            other_asset["type"] = mimetypes.guess_type(other_asset["name"])[0]

        item.add_asset(
            key=other_asset["name"],
            asset=pystac.Asset(
                href=href,
                media_type=other_asset["type"],  # TODO: Convert to pystac.MediaType
            ),
        )

    # Configure extensions
    configure_extensions(item, properties)

    item.set_self_href("item.json")

    item.validate()
    item.save_object()

    item_json = item.to_dict()
    return item_json


def return_geom_from_multiple_geom(geom):
    """Return a single geometry from a list of geometries"""
    # For now, just return the first geom and convert to geometry obect
    return geom[0]


def return_bbox_from_geom(geom, src_crs, destination_crs):
    """
    Return a bbox from a geometry
    """
    geom = Polygon(geom["coordinates"][0])
    left, bottom, right, top = transform_bounds(
        "epsg:4326", destination_crs, *geom.bounds
    )
    return [left, bottom, right, top]


def return_geom_from_bbox(bbox):
    """Return a geometry from a bbox"""
    return {
        "type": "Polygon",
        "coordinates": [
            [
                [bbox[0], bbox[1]],
                [bbox[2], bbox[1]],
                [bbox[2], bbox[3]],
                [bbox[0], bbox[3]],
                [bbox[0], bbox[1]],
            ]
        ],
    }


def return_epsg_from_wkt(wkt):
    """Return an EPSG code from a WKT"""
    src_crs = CRS.from_wkt(wkt)
    return src_crs.to_epsg()


def return_bbox_from_coordinates(geom, src_crs, destination_crs):
    """Return a bbox from mapped coorindates"""
    left, bottom, right, top = transform_bounds(
        src_crs,
        destination_crs,
        geom["lowerLeft"][0],
        geom["lowerLeft"][1],
        geom["lowerRight"][0],
        geom["upperLeft"][1],
    )
    return [left, bottom, right, top]


def planet_stac_parser(properties, metadata):
    """Parse Planet STAC metadata"""
    planet_properties = metadata["properties"]
    if planet_properties.get("gsd"):
        properties["gsd"] = planet_properties["gsd"]

    # EO Additions
        
    ## eo:cloud_cover is expecting a %, so take from the cloud_percent field in planet, rather than the cloud_cover which is 0-1    
    if planet_properties.get("cloud_percent") != None:
        properties["eo:cloud_cover"] = planet_properties["cloud_percent"]

    # View Additions
    if planet_properties.get("sun_elevation"):
        properties["view:sun_elevation"] = planet_properties["sun_elevation"]
    if planet_properties.get("sun_azimuth"):
        properties["view:sun_azimuth"] = planet_properties["sun_azimuth"]
    if planet_properties.get("view_angle"):
        properties["view:off_nadir"] = planet_properties["view_angle"]

    # Thumbnail


def additional_stac_parser(properties, metadata):
    """Parse Maxar STAC metadata['additional']"""
    # Cloud Cover
    if metadata["additional"].get("cloudCover") != None:
        properties["eo:cloud_cover"] = float(metadata["additional"]["cloudCover"])

    # View additions
    try:
        if metadata["additional"]["sunAzimuth"] != None:
            properties["view:sun_azimuth"] = float(metadata["additional"]["sunAzimuth"])
    except Exception:
        pass

    try:
        if metadata["additional"]["sunElevation"]:
            properties["view:sun_elevation"] = float(
                metadata["additional"]["sunElevation"]
            )
    except Exception:
        pass

    try:
        if metadata["additional"]["offNadirAngle"]:
            properties["view:off_nadir"] = float(
                metadata["additional"]["offNadirAngle"]
            )
    except Exception:
        pass

    try:
        if metadata["additional"]["gsd"]:
            properties["gsd"] = float(metadata["additional"]["gsd"])
    except Exception:
        pass


# Function that checkswhat extensions are present and adds them to the item
def configure_extensions(item, properties):
    if any(key.startswith("eo:") for key in properties):
        item.stac_extensions.append(stac_extensions["eo"])
    if any(key.startswith("view:") for key in properties):
        item.stac_extensions.append(stac_extensions["view"])
    if any(key.startswith("proj:") for key in properties):
        item.stac_extensions.append(stac_extensions["proj"])


def generate_thumbnail(metadata):
    """Generate a thumbnail"""
    # Maxar
    thumbnail = [
        asset
        for asset in metadata["otherAssets"]
        if asset["type"] == "image/jpeg" and "BROWSE" in asset["name"]
    ]

    return thumbnail[0] if thumbnail else None


def generate_url(item_name, base_url, account_name, endpoint_suffix):
    blob_url = f"https://{account_name}.blob.{endpoint_suffix}"

    href = "/".join(base_url) + "/" + item_name
    if not href.startswith(blob_url):
        # if href starts does not start with slash add it
        if not href.startswith("/"):
            href = "/" + href
        href = blob_url + href

    return href
