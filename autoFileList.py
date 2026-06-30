from pathlib import Path
import shutil

# Source directory (Windows Downloads folder)
DOWNLOADS_DIR = Path(r"C:\Users\student\Downloads")

# Destination folders by category
DESTINATION_MAP = {
    "images": {".jpg", ".jpeg"},
    "data": {".csv", ".xlsx"},
    "docs": {".txt", ".doc", ".pdf"},
    "archive": {".zip"},
}


def build_extension_to_folder_map(base_dir: Path) -> dict[str, Path]:
    """Create destination directories and return extension-to-folder mapping."""
    extension_to_folder: dict[str, Path] = {}

    for folder_name, extensions in DESTINATION_MAP.items():
        folder_path = base_dir / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)

        for extension in extensions:
            extension_to_folder[extension] = folder_path

    return extension_to_folder


def get_unique_destination_path(destination_file: Path) -> Path:
    """Avoid overwriting by appending a numeric suffix when needed."""
    if not destination_file.exists():
        return destination_file

    stem = destination_file.stem
    suffix = destination_file.suffix
    parent = destination_file.parent

    index = 1
    while True:
        candidate = parent / f"{stem}_{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def move_files_by_extension(source_dir: Path) -> None:
    """Move files from source directory into categorized folders by extension."""
    if not source_dir.exists() or not source_dir.is_dir():
        print(f"다운로드 폴더를 찾을 수 없습니다: {source_dir}")
        return

    extension_to_folder = build_extension_to_folder_map(source_dir)

    moved_count = 0
    for item in source_dir.iterdir():
        if not item.is_file():
            continue

        extension = item.suffix.lower()
        destination_folder = extension_to_folder.get(extension)
        if destination_folder is None:
            continue

        destination_path = get_unique_destination_path(destination_folder / item.name)
        shutil.move(str(item), str(destination_path))
        moved_count += 1
        print(f"이동 완료: {item.name} -> {destination_path}")

    print(f"총 {moved_count}개 파일을 이동했습니다.")


if __name__ == "__main__":
    move_files_by_extension(DOWNLOADS_DIR)
