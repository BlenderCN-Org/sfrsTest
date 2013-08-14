@set BLENDER_PATH= "E:\\Graphics\\BlenderFoundation\\blender-2.68-RC1-windows32\\blender.exe"
@set FLAGS_BG="--background"
@set PYTHON="--python"
@set SCRIPT_FILE="E:\\DevelProjects\\gitRepository\\sfrsTest\\sfrsTest\\src\\sfrsMinimal\\Instances.py"
@set BLEND_FILE="E:\\DevelProjects\\gitRepository\\sfrsTest\\sfrsTest\\src\\blends\\casestudies\\Instances.blend"

@set val=%BLENDER_PATH%  %BLEND_FILE% %FLAGS_BG% %PYTHON% %SCRIPT_FILE%  %*
%val%