import logging
import shutil
import subprocess
from pathlib import Path, PurePath

from config import VERSION

logging.basicConfig(level=logging.ERROR, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("RuwaInstaller")


class RuwaInstaller:
    __project_path = "/tmp/ruwa"
    __build_path = "/tmp/ruwa/build"
    app_default_path = ""
    options = {}

    def __init__(self, options: dict, path: PurePath | str):
        RuwaInstaller.app_default_path = path
        RuwaInstaller.options = options

        logger.info("Initializing Ruwa installer")
        logger.info("Installation path: %s", path)
        logger.info("Options: %s", options)


    @staticmethod
    def check_packages() -> list | None:
        packages = [
            "base-devel",
            "cmake",
            "ninja",
            "git",
            "qt6-base",
            "qt6-tools",
            "qt6-declarative",
            "qt6-svg",
        ]
        missing = []

        for package in packages:
            result = subprocess.run(["pacman", "-Q", package],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            )

            if result.returncode != 0:
                logger.warning("Package is not installed: %s", package)
                missing.append(package)
            else: 
                logger.info("Package is installed: %s", package)
        if missing:
            logger.error("Missing packages: %s", ", ".join(missing))
            return missing


    @staticmethod
    def download_ruwa() -> str | None:
        path = RuwaInstaller.__project_path

        logger.info("Starting Ruwa download...")
        logger.info("Repository: https://github.com/LuskusDeus/Ruwa.git")
        logger.info("Version/branch: %s", VERSION)
        
        if Path(path).exists():
            shutil.rmtree(path)

        result = subprocess.run(
            [
                "git",
                "clone",
                "-b",
                VERSION,
                "https://github.com/LuskusDeus/Ruwa.git",
                path,
            ],
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0:
            logger.error("git clone failed: %s", result.stderr.strip())
            return result.stderr
        logger.info("Ruwa source downloaded successfully.")


    def __fix_lasso_shader_check():
        file_path = ( Path(RuwaInstaller.__project_path) / "src/shared/rendering/ShaderDirectoryResolver.cpp")
        logger.info("Applying patch fix lasso shader: %s", file_path)

        old = '        QStringLiteral("lasso_mask.comp.glsl"),'
        new = '//        QStringLiteral("lasso_mask.comp.glsl"),'

        with open(file_path, "r+", encoding="utf-8",) as f:
            content = f.read()
            if old not in content:
                logger.warning("Lasso shader check line not found: %s", file_path)
                return
            content = content.replace(old, new, 1)
            f.seek(0)
            f.write(content)
            f.truncate()

    def __apply_patches():
        file_path = ( Path(RuwaInstaller.__project_path) / "plugins/standard/distort/src/effects/Pinch.c")
        logger.info("Applying patch: %s", file_path)
        
        with open(file_path, "r+", encoding="utf-8",) as f:
            content = f.read()
            if "#include <math.h>" in content:
                return

            f.seek(0, 0)
            f.write("#include <math.h>\n")
            f.write(content)
            
        RuwaInstaller.__fix_lasso_shader_check()
        logger.info("Patch applied successfully.")
        
    @staticmethod
    def configure() -> None:
        logger.info("Starting CMake configuration...")
        
        result = subprocess.run(
            [
                "cmake",
                "-S",
                RuwaInstaller.__project_path,
                "-B",
                RuwaInstaller.__build_path,
                "-G",
                "Ninja",
                "-DCMAKE_BUILD_TYPE=Release",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            logger.error( "CMake configuration failed:\n%s", result.stderr, )
            return result.stderr

        logger.info("CMake configuration completed successfully.")


    @staticmethod
    def build():
        logger.info("Starting Ruwa build...")
        
        RuwaInstaller.__apply_patches()
        result = subprocess.run(
            ["cmake", "--build", RuwaInstaller.__build_path, "-j"],
            #capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            logger.error("Build failed:\n%s", result.stderr)
            return result.stderr

        shader_dir = (
            Path(RuwaInstaller.__build_path) / "shaders"
        )
        shader_file = shader_dir / "lasso_mask.comp.glsl"
        logger.info("Checking generated shaders...")
        logger.info("Shader directory: %s", shader_dir)
        if shader_file.exists():
            logger.info(
                "Found shader: %s",
                shader_file,
            )
        else:
            logger.error(
                "Missing shader: %s",
                shader_file,
            )

    
        logger.info("Ruwa build completed successfully.")      
        return True


    @staticmethod
    def install():
        destination_app = Path(RuwaInstaller.app_default_path).expanduser()
        destination_app.mkdir(parents=True, exist_ok=True)

        logger.info("Starting installation...")
        logger.info("Installation directory: %s", destination_app)
        
        build_path = Path(RuwaInstaller.__build_path)
        resources = [
            build_path / "effects",
            build_path / "plugins",
            build_path / "Ruwa",
            build_path / "shaders",
            build_path / "RuwaPigmentLutGenerator",
            build_path / "out-x86_64-Release" / "lib",
        ]
        logger.info("Checking build resources...")
        try:
            for resource in resources:
                if resource.exists():
                    logger.info("Found: %s", resource)
                else:
                    logger.error("NOT FOUND: %s", resource)
                    
                destination = destination_app / resource.name
                if resource.is_dir():
                    shutil.copytree(
                        resource,
                        destination,
                        dirs_exist_ok=True,
                    )
                else:
                    shutil.copy2(resource, destination)
    
        except OSError as e:
            logger.exception("Installation failed")
            return str(e)

        return True


    @staticmethod
    def create_shortcut():
        logger.info("Creating desktop entry...")
        
        destination = Path("~/.local/share/applications").expanduser()
        destination_app = Path(RuwaInstaller.app_default_path).expanduser()
        destination_app.mkdir(parents=True, exist_ok=True)

        env_string = " ".join(
            f'{key}={value}'
            for key, value in RuwaInstaller.options.items()
            if key != "add_shortcut"
        )

        desktop_file = destination / "ruwa.desktop"
        CONTENT = f"""[Desktop Entry]
Type=Application
Name=Ruwa
Exec=env LD_LIBRARY_PATH={destination_app / 'lib'} {env_string} {destination_app}/Ruwa %U
Icon=ruwa
Terminal=false
Categories=Graphics;
MimeType=image/jpeg;image/png;image/webp;image/svg+xml;
"""
        with open(desktop_file, "w", encoding="utf-8") as f:
            f.write(CONTENT)

        subprocess.run(["update-desktop-database", str(destination)], check=True)


if __name__ == "__main__":
    installer = RuwaInstaller(
            options={
                "QT_QPA_PLATFORMTHEME": "xdgdesktopportal",
                "QT_QPA_PLATFORM": "xcb"
            },
            path='~/.local/bin/ruwa-test'
        )
    installer.check_packages()
    installer.download_ruwa()
    installer.configure()
    installer.build()
    installer.install()
    installer.create_shortcut()
    
