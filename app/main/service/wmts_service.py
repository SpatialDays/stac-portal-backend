from typing import Dict
from flask import current_app
from ..service.stac_service import get_item_from_collection
from urllib.parse import urljoin, urlparse
def get_all_wmts_urls_for_item(collection_id: str, item_id: str) -> Dict[str,str]:
    item = get_item_from_collection(collection_id, item_id)
    return _extract_wmts_urls(item)

def _extract_wmts_urls(item: dict, titiler_url:str = None) -> Dict[str,str]:
    collection_id = item["collection"]
    item_id = item["id"]
    hrefs = {}
    for key,value in item["assets"].items():
        href = value["href"]
        href = urljoin(href, urlparse(href).path)

        if not href.split(".")[-1].lower() in ["tif","tiff","png","jpg","jpeg"]:
            continue

        eo_bands_list = []
        raster_bands_list = []
        try:
            eo_bands_list = value["eo:bands"]
        except KeyError:
            pass

        try:
            raster_bands_list = value["raster:bands"]
        except KeyError:
            pass

        if len(eo_bands_list) == 0 and len(raster_bands_list) == 0:
            continue
        if not titiler_url:
            titiler_url = current_app.config["TITILER_ENDPOINT"]
        if not titiler_url.endswith("/"):
            titiler_url += "/"

        if len(eo_bands_list) == 1 or len(raster_bands_list) == 1:
            # example: http://titiler-pgstac.os-eo-platform-rg-staging.azure.com/collections/os_rgbi/items/fdcd6488-6e3d-4889-83a5-9ba877e40e59/WMTSCapabilities.xml?TileMatrixSetId=WebMercatorQuad&tile_format=png&assets=data
            url = f"{titiler_url}collections/{collection_id}/items/{item_id}/WMTSCapabilities.xml?TileMatrixSetId=WebMercatorQuad&tile_format=png&assets={key}"
            hrefs[key] = url
            continue

        elif len(eo_bands_list) > 1:
            rgb_bands = [i for i, band in enumerate(eo_bands_list) if
                         band["description"] in ["red", "green", "blue", "gray"]]
            # example: http://titiler-pgstac.os-eo-platform-rg-staging.azure.com/collections/os_rgbi/items/fdcd6488-6e3d-4889-83a5-9ba877e40e59/WMTSCapabilities.xml?TileMatrixSetId=WebMercatorQuad&tile_format=png&assets=data&asset_bidx=data|1,2,3
            url = f"{titiler_url}collections/{collection_id}/items/{item_id}/WMTSCapabilities.xml?TileMatrixSetId=WebMercatorQuad&tile_format=png&assets={key}&asset_bidx={key}|"
            for i in rgb_bands:
                url += f"{i + 1},"
            # remove last comma
            url = url[:-1]
            hrefs[key] = url
            continue
        elif len(raster_bands_list) == 2 or len(raster_bands_list) == 3 or len(raster_bands_list) == 4:
            url = f"{titiler_url}collections/{collection_id}/items/{item_id}/WMTSCapabilities.xml?TileMatrixSetId=WebMercatorQuad&tile_format=png&assets={key}"
            hrefs[key] = url
            continue

        else:
            continue

    return hrefs