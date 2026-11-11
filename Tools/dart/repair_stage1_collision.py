"""Narrow migration for the authored baseline: persist NoCollision through profile reload."""
import unreal

assert "-run=pythonscript" in unreal.SystemLibrary.get_command_line().lower(), "Commandlet only; protect open editor work"
assert "VR_Dart_Game" in unreal.Paths.get_project_file_path(), "Wrong project"
levels = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert levels.load_level("/Game/DartLab/Maps/L_DartLab")
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
parts = {a.get_actor_label(): a for a in actors
         if a.get_actor_label() in ("DartBody", "DartTip", "DartFlights")}
assert len(parts) == 3
for actor in parts.values():
    assert "DartLabStage1" in [str(tag) for tag in actor.tags]
    actor.static_mesh_component.set_collision_profile_name("NoCollision")
    actor.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
assert levels.save_current_level()
unreal.log("DART_LAB_COLLISION_REPAIR PASS")
