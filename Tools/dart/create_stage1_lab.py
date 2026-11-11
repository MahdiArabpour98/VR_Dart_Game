"""Author only the new static DartLab map. Existing lab assets are never overwritten."""
import unreal

assert "-run=pythonscript" in unreal.SystemLibrary.get_command_line().lower(), "Commandlet only; protect open editor work"
MAP = "/Game/DartLab/Maps/L_DartLab"
assert "VR_Dart_Game" in unreal.Paths.get_project_file_path(), "Wrong project"
assert not unreal.EditorAssetLibrary.does_asset_exist(MAP), "Lab exists; refusing overwrite"
levels = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
assert levels.new_level(MAP), "Could not create lab map"


def mesh(label, asset, location, scale, rotation=unreal.Rotator(), collision=True):
    actor = actors.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(*location), rotation)
    actor.set_actor_label(label)
    actor.set_actor_scale3d(unreal.Vector(*scale))
    component = actor.static_mesh_component
    component.set_static_mesh(unreal.load_asset("/Engine/BasicShapes/" + asset))
    component.set_simulate_physics(False)
    component.set_collision_profile_name("BlockAll" if collision else "NoCollision")
    component.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS if collision
                                    else unreal.CollisionEnabled.NO_COLLISION)
    actor.set_editor_property("tags", ["DartLabStage1"])
    return actor


mesh("LabFloor", "Cube", (150, 0, -5), (8, 6, 0.1))
mesh("DartBoard", "Cylinder", (239, 0, 173), (0.451, 0.451, 0.04), unreal.Rotator(90, 0, 0))
mesh("BoardStand", "Cube", (243, 0, 85), (0.06, 0.12, 1.7))
mesh("DartTable", "Cube", (0, -65, 78), (0.6, 0.6, 0.04))
mesh("TablePedestal", "Cube", (0, -65, 38), (0.1, 0.1, 0.76))
body = mesh("DartBody", "Cylinder", (0, -65, 82), (0.006, 0.006, 0.12),
            unreal.Rotator(90, 0, 0), False)
tip = mesh("DartTip", "Cone", (7.5, -65, 82), (0.006, 0.006, 0.03),
           unreal.Rotator(90, 0, 0), False)
flights = mesh("DartFlights", "Cube", (-6.5, -65, 82), (0.01, 0.025, 0.025), collision=False)
for child in (tip, flights):
    child.attach_to_actor(body, "", unreal.AttachmentRule.KEEP_WORLD,
                          unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, False)
start = actors.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(0, 0, 5))
start.set_actor_label("LabPlayerStart")
light = actors.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0, 0, 300),
                                      unreal.Rotator(-50, -30, 0))
light.set_actor_label("LabLight")
light.light_component.set_editor_property("intensity", 3.0)
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
settings = world.get_world_settings()
settings.set_editor_property("world_to_meters", 100.0)
settings.set_editor_property("default_game_mode", unreal.load_class(None,
    "/Game/XRFramework/Blueprints/BP_XRGameMode.BP_XRGameMode_C"))
assert levels.save_current_level(), "Failed to save new lab map"
unreal.log("DART_LAB_CREATE PASS " + MAP)
