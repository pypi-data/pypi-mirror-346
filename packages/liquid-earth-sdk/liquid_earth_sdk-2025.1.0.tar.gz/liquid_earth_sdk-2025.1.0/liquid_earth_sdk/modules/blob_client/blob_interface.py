import logging
from dataclasses import dataclass
from io import BytesIO
from typing import Union, Optional

from azure.storage.blob import BlobClient

import subsurface


@dataclass
class DataToPushMesh:
    unstructured_data: subsurface.UnstructuredData
    texture: Optional[subsurface.StructuredData]


valid_data_types = Union[
    subsurface.UnstructuredData,
    subsurface.StructuredData,
    DataToPushMesh
]


def push_unstructured_data(data_to_push: valid_data_types, sas: dict[str]) -> bool:
    """
    Upload  data to Azure Blob Storage.
    """
    logger = logging.getLogger(__name__)

    try:
        match data_to_push:
            case subsurface.UnstructuredData():
                _push_unstruct_to_le(
                    unstructured_data=data_to_push,
                    sas=sas,
                    logger=logger
                )
            case DataToPushMesh():
                # Handle texture separately if present
                _push_unstruct_to_le(logger, sas, data_to_push.unstructured_data)
                if data_to_push.texture:
                    _push_texture_to_png(data_to_push.texture, sas, logger)
            case subsurface.StructuredData():
                # Handle structured data
                raise NotImplementedError()
            case _:
                raise TypeError(f"Unsupported data type: {type(data_to_push)}")
        return True

    except Exception as e:
        error_message = f"Error uploading data to blob storage: {str(e)}"
        logger.error(error_message)
        raise ValueError(error_message) from e


def _push_unstruct_to_le(logger, sas: dict[str], unstructured_data):
    sas = sas.get("sasForTestLe", None)
    if not sas:
        raise ValueError("Missing required SAS token in sas_dict")
    binary_data = unstructured_data.to_binary()
    # Initialize blob client and create data stream
    blob_client = BlobClient.from_blob_url(sas)
    data_stream = BytesIO(binary_data)
    # Upload data to blob storage
    upload_result: dict = blob_client.upload_blob(
        data_stream,
        blob_type="BlockBlob",
        overwrite=True
    )
    logger.info(f"Successfully uploaded blob: {upload_result}")


def _push_texture_to_png(texture: subsurface.StructuredData, sas: dict[str], logger):
    from PIL import Image
    array = texture.values
    # Assume 'array' is your numpy image array
    # It should have shape (height, width, 3) or (height, width, 4)

    assert array.shape[2] == 3 or array.shape[2] == 4

    # Convert the numpy array to a PIL image
    image = Image.fromarray(array.astype('uint8'))

    # Alternatively, save to a bytes buffer for in-memory use
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    compressed_png_data = buffer.getvalue()

    sas = sas.get("sasForTexture", None)
    if not sas:
        raise ValueError("Missing required SAS token in sas_dict")

    # Upload the PNG data to Azure Blob Storage
    blob_client = BlobClient.from_blob_url(sas)
    blob_client.upload_blob(
        compressed_png_data,
        blob_type="BlockBlob",
        overwrite=True
    )

    logger.info(f"Successfully uploaded texture blob: {sas}")
