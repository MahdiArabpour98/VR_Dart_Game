"""Run inside Unreal Python commandlet; verifies the saved static lab, not VR gameplay."""
import json
from pathlib import Path
import unreal

MAP = "/Game/DartLab/Maps/L_DartLab"
REPORT = Path(__file__).resolve().parents[2] / "interaction/dart/stage1/map-report.json"


def verify():
    assert "-run=pythonscript" in unreal.SystemLibrary.get_command_line().lower(), "Commandlet only; protect open editor work"
    assert "VR_Dart_Game" in unreal.Paths.get_project_file_path(), "Wrong project"
    assert unreal.EditorAssetLibrary.does_asset_exist(MAP), "Dart lab map does not exist"
    editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    assert editor.load_level(MAP), "Could not load saved lab"
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
    by_label = {a.get_actor_label(): a for a in actors}
    expected = ["LabFloor", "DartBoard", "DartBody", "DartTip", "DartFlights", "LabPlayerStart", "LabLight"]
    for label in expected:
        assert label in by_label, f"Missing actor: {label}"
    board = by_label["DartBoard"]
    center = board.get_actor_location()
    assert abs(center.x - 239.0) < 0.01 and abs(center.z - 173.0) < 0.01
    scale = board.get_actor_scale3d()
    assert abs(scale.x * 100.0 - 45.1) < 0.01, "Board diameter must be 45.1 cm"
    assert abs(scale.z * 100.0 - 4.0) < 0.01
    # Board center x=239 minus its half thickness=2 gives a face 237 cm from x=0.
    assert abs(center.x - scale.z * 50.0 - 237.0) < 0.01
    assert board.static_mesh_component.get_collision_enabled() != unreal.CollisionEnabled.NO_COLLISION
    for label in ("DartBody", "DartTip", "DartFlights"):
        mesh = by_label[label].static_mesh_component
        assert not mesh.is_simulating_physics(), "Stage 1 dart is a static placeholder"
        assert mesh.get_collision_enabled() == unreal.CollisionEnabled.NO_COLLISION, (
            f"{label}: collision={mesh.get_collision_enabled()}, profile={mesh.get_collision_profile_name()}")
    floor_location, floor_extent = by_label["LabFloor"].get_actor_bounds(False)
    assert abs(floor_location.z + floor_extent.z) < 0.1, "Floor surface must be z=0"
    body = by_label["DartBody"]
    for label in ("DartTip", "DartFlights"):
        assert by_label[label].get_attach_parent_actor() == body, "One composite dart required"
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    settings = world.get_world_settings()
    assert abs(settings.get_editor_property("world_to_meters") - 100.0) < 0.001
    mode = settings.get_editor_property("default_game_mode")
    assert mode and "BP_XRGameMode" in mode.get_path_name(), "XR template GameMode must be retained"
    return {"ok": True, "map": MAP, "actors": expected, "board_face_distance_cm": 237,
            "board_center_height_cm": 173, "board_diameter_cm": 45.1,
            "stage": "static baseline; no grab or throw implemented", "headset_tested": False}


if __name__ == "__main__":
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    try:
        report = verify()
    except Exception as error:
        REPORT.write_text(json.dumps({"ok": False, "error": str(error)}, indent=2), encoding="utf-8")
        raise
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    unreal.log("DART_LAB_VERIFY PASS " + json.dumps(report))
