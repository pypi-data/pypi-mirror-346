import os

import pytest

import subsurface as ss
from liquid_earth_sdk.core.output import ServerResponse
from liquid_earth_sdk.modules.blob_client.blob_interface import DataToPushMesh

from liquid_earth_sdk.api import le_api
from subsurface.modules.reader import load_gltf_with_trimesh
from subsurface.modules.reader.mesh._trimesh_reader import TriMeshTransformations

ONLY_EXPLICIT = os.getenv("ONLY_EXPLICIT", True)


@pytest.mark.skipif(ONLY_EXPLICIT, reason="Run Explicit")
def test_glb_one_element_no_texture():
    glb_path = os.getenv("TERRA_PATH_DEVOPS") + "/meshes/GLB - GLTF/Duck.glb"
    ts: ss.TriSurf = load_gltf_with_trimesh(glb_path, coordinate_system=TriMeshTransformations.RIGHT_HANDED_Z_UP)

    if False:
        s = ss.visualization.to_pyvista_mesh(ts)
        ss.visualization.pv_plot([s], image_2d=False)

    if True:
        response: ServerResponse = le_api.upload_mesh_to_existing_space(
            space_name="[TEMP] Test PythonSDk: glb one element no texture",
            data=DataToPushMesh(
                unstructured_data=ts.mesh,
                texture=ts.texture
            ),
            file_name="glb_duck",
            token=(os.environ.get("LIQUID_EARTH_API_TOKEN")),
            grab_link=False
        )

        pass


@pytest.mark.skipif(ONLY_EXPLICIT, reason="Run Explicit")
def test_glb_scene():
    """
    ! We do not support to upload a scene with multiple textures yet
    """
    glb_path = os.getenv("TERRA_PATH_DEVOPS") + "/meshes/GLB - GLTF/GlbFile.glb"
    ts: ss.TriSurf = load_glb_with_trimesh(glb_path)
    
    assert len(ts.multi_texture_cache), 10

    if True:
        s = ss.visualization.to_pyvista_mesh(ts)
        ss.visualization.pv_plot([s], image_2d=False)

    if True:
        response: ServerResponse = le_api.upload_mesh_to_new_space(
            space_name="[TEMP] Test PythonSDk: glb scene",
            data=DataToPushMesh(
                unstructured_data=ts.mesh,
                texture=ts.texture
            ),
            file_name="glb_map",
            token=(os.environ.get("LIQUID_EARTH_API_TOKEN")),
            grab_link=False
        )

        pass
