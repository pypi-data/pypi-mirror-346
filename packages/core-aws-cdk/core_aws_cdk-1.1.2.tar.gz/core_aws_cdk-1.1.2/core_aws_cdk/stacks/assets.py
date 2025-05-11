# -*- coding: utf-8 -*-

import glob
import os
import pathlib
import shutil
import typing

from aws_cdk.aws_lambda import AssetCode


class ZipAssetCode(AssetCode):
    """
    It will produce the ZIP file which contains the package
    and the required dependencies...
    """

    DEFAULT_EXCLUDED_DEPENDENCIES = (
        "bin", "boto3", "botocore", "certifi", "charset_normalizer", "click", "coverage",
        "dateutil", "docutils", "idna", "jmespath", "packaging", "pip", "python-dateutil",
        "requests", "s3transfer", "setuptools", "urllib3"
    )

    DEFAULT_EXCLUDED_FILES = (
        "*.dist-info",
        "__pycache__",
        "*.pyc",
        "*.pyo"
    )

    def __init__(
            self, work_dir: pathlib.Path, project_directory: pathlib.Path,
            include_paths: typing.List[str] = None, include_project_folders: typing.List[str] = None,
            excluded_dependencies: typing.Iterable[str] = DEFAULT_EXCLUDED_DEPENDENCIES,
            excluded_files: typing.Iterable[str] = DEFAULT_EXCLUDED_FILES,
            python_version: str = "python3.12",
            pip_args: str = "") -> None:

        """
        :param work_dir: Path to the folder where the Lambda code lives.
        :param project_directory: Path to the folder where the project code lives.
        :param include_paths: List of files (within work_dir) to include in the package.

        :param include_project_folders:
            List of folders (within project_directory) to include in the package. Useful whenever you
            need to include modules/files to the Lambda, but the code is commons to other components
            and is located outside the Lambda folder.

        :param python_version: Python version used.

        :param pip_args:
            Extra arguments to pass to pip install command
            like: --implementation=cp --only-binary=":all:" --platform=manylinux2010_x86_64

        :param excluded_dependencies:
        :param excluded_files:
        """

        self.work_dir = work_dir
        self.python_version = python_version
        self.project_directory = project_directory
        self.build_dir = self.work_dir / ".build"
        self.pip_args = pip_args

        self._include_paths = include_paths
        self._include_project_folders = include_project_folders or []
        self._zip_file = work_dir.name

        self.excluded_dependencies = excluded_dependencies or []
        self.excluded_files = excluded_files or []

        path = self.create_package()
        super().__init__(path.as_posix())

    @property
    def is_inline(self) -> bool:
        return False

    def create_package(self) -> pathlib.Path:
        print("\n###################################################################")
        print(f"# Project folder: {self.project_directory}")
        print(f"# Lambda folder: {self.work_dir}")
        print(f"# Build folder: {self.build_dir}")
        print("###################################################################")

        try:
            os.chdir(self.work_dir.as_posix())

            print("\n**************************** STEP 1 ****************************")
            print("Removing previous content into build folder...")
            os.system(f"rm -rf \"{self.build_dir}\"/*")

            print("Creating folder...")
            shutil.rmtree(self.build_dir, ignore_errors=True)
            self.build_dir.mkdir(parents=True)

            print("Installing dependencies...")
            req_path = self.work_dir / "requirements.txt"

            os.system(
                f"/bin/sh -c '{self.python_version} -m pip install {self.pip_args} "
                f"--target \"{self.build_dir}\" --requirement \"{req_path}\" "
                f"&& find \"{self.build_dir}\" -name \\*.so -exec strip \\{{\\}} \\;'"
            )

            print("\n**************************** STEP 2 ****************************")
            print("Removing excluded elements...")
            excluded_dependencies = set(self.excluded_dependencies)
            excluded_files = set(self.excluded_files)

            for pattern in excluded_dependencies.union(excluded_files):
                pattern = str(self.build_dir / '**' / pattern)
                print(f"\t-> {pattern}")
                files = glob.glob(pattern, recursive=True)

                for file_path in files:
                    try:
                        shutil.rmtree(file_path) \
                            if os.path.isdir(file_path) \
                            else os.remove(file_path) if os.path.isfile(file_path) \
                            else None

                    except OSError:
                        print(f"Error deleting file/folder: {file_path}")

            print("\n**************************** STEP 3 ****************************")
            print("Copying project files...")

            for folder in self._include_project_folders:
                folder_ = (self.project_directory / folder).resolve()
                print(f"\t->  {folder_}")
                os.system(f"cp -R \"{folder_}\" \"{self.build_dir}\"")

            for include_path in self._include_paths:
                print(f"\t->  {(pathlib.Path.cwd() / include_path).resolve()}")
                os.system(f"cp -R \"{include_path}\" \"{self.build_dir}\"")

            print("\n**************************** STEP 4 ****************************")
            zip_file_path = (self.work_dir / self._zip_file).resolve()
            print(f"Creating package into {zip_file_path}.zip")

            shutil.make_archive(
                base_name=str(zip_file_path),
                format="zip",
                root_dir=str(self.build_dir),
                verbose=True
            )

            return self.work_dir.joinpath(self._zip_file + ".zip").resolve()

        except Exception as ex:
            raise Exception("Error during build.", str(ex))
