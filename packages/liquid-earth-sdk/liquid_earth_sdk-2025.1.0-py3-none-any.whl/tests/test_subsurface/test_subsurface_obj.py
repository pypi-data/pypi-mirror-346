import os

import pytest

import subsurface as ss
from liquid_earth_sdk.core.output import ServerResponse
from liquid_earth_sdk.modules.blob_client.blob_interface import DataToPushMesh

from liquid_earth_sdk.api import le_api
from subsurface.modules.reader.mesh._trimesh_reader import load_with_trimesh

ONLY_EXPLICIT = os.getenv("ONLY_EXPLICIT", True)


@pytest.mark.skipif(ONLY_EXPLICIT, reason="Run Explicit")
def test_obj_one_element_no_texture():
    path_to_obj = os.getenv("TERRA_PATH_DEVOPS") + "/meshes/OBJ/TexturedMesh/PenguinBaseMesh.obj"
    trimesh_obj = load_with_trimesh(
        path_to_file_or_buffer=path_to_obj,
        plot=False
    )
    ts: ss.TriSurf = ss.modules.reader.mesh._trimesh_reader.trimesh_to_unstruct(trimesh_obj)

    if False:
        s = ss.visualization.to_pyvista_mesh(ts)
        ss.visualization.pv_plot([s], image_2d=False)

    if True:
        unstruct: ss.UnstructuredData = ts.mesh
        response: ServerResponse = le_api.upload_mesh_to_new_space(
            space_name="[TEMP] Test PythonSDk: OBJ one element no texture",
            data=unstruct,
            file_name="obj_one_element_no_texture",
            token=(os.environ.get("LIQUID_EARTH_API_TOKEN")),
            grab_link=False
        )

        pass


@pytest.mark.skipif(ONLY_EXPLICIT, reason="Run Explicit")
def test_OBJ_trimesh_THREE_ELEMENTS_no_texture_to_unstruct():
    path_to_obj = os.getenv("TERRA_PATH_DEVOPS") + "/meshes/OBJ/MultiMaterialObj/MultiMaterialObj.obj"
    trimesh_obj = load_with_trimesh(
        path_to_file_or_buffer=path_to_obj,
        plot=False
    )
    ts: ss.TriSurf = ss.modules.reader.mesh._trimesh_reader.trimesh_to_unstruct(trimesh_obj)

    if False:
        s = ss.visualization.to_pyvista_mesh(ts)
        ss.visualization.pv_plot([s], image_2d=False)

    if True:
        unstruct: ss.UnstructuredData = ts.mesh
        # response: ServerResponse = le_api.upload_mesh_to_new_space(
        response: ServerResponse = le_api.upload_mesh_to_existing_space(
            space_name="[TEMP] Test PythonSDk: OBJ three element no texture",
            data=unstruct,
            file_name="obj_one_element_no_texture",
            token=(os.environ.get("LIQUID_EARTH_API_TOKEN")),
            grab_link=False
        )

        pass


@pytest.mark.skipif(ONLY_EXPLICIT, reason="Run Explicit")
def test_OBJ_ONE_element_texture_to_unstruct():
    path_to_obj = os.getenv("TERRA_PATH_DEVOPS") + "/meshes/OBJ/Faces/Lapp_458_Rum_19_2_2024-02-21_0820_scan5_geoim4.obj"
    trimesh_obj = load_with_trimesh(
        path_to_file_or_buffer=path_to_obj,
        plot=False
    )
    ts: ss.TriSurf = ss.modules.reader.mesh._trimesh_reader.trimesh_to_unstruct(trimesh_obj)

    if False:
        s = ss.visualization.to_pyvista_mesh(ts)
        ss.visualization.pv_plot([s], image_2d=False)

    if True:
        response: ServerResponse = le_api.upload_mesh_to_existing_space(
            space_name="[TEMP] Test PythonSDk: OBJ one element one texture",
            data=DataToPushMesh(
                unstructured_data=ts.mesh,
                texture=ts.texture
            ),
            file_name="obj_one_element_one_texture",
            token=(os.environ.get("LIQUID_EARTH_API_TOKEN")),
            grab_link=False
        )

        pass


@pytest.mark.skipif(ONLY_EXPLICIT, reason="Run Explicit")
def test_OBJ_three_submeshes_texture_to_unstruct():
    """
    NOTE (April 25) at this stage we do not support submeshes in liquid earth
    """
    path_to_obj = os.getenv("TERRA_PATH_DEVOPS") + "/meshes/OBJ/Core scans Boliden/rsrbF9l2zc/model.obj"
    trimesh_obj = load_with_trimesh(
        path_to_file_or_buffer=path_to_obj,
        plot=False
    )
    ts: ss.TriSurf = ss.modules.reader.mesh._trimesh_reader.trimesh_to_unstruct(trimesh_obj)

    if True:
        s = ss.visualization.to_pyvista_mesh(ts)
        ss.visualization.pv_plot([s], image_2d=False)

    if True:
        unstruct: ss.UnstructuredData = ts.mesh
        response: ServerResponse = le_api.upload_mesh_to_new_space(
            space_name="[TEMP] Test PythonSDk: OBJ Submeshes element multiple texture",
            data=unstruct,
            file_name="obj_submeshes_multiple_texture",
            token=(os.environ.get("LIQUID_EARTH_API_TOKEN")),
            grab_link=False
        )

        pass
