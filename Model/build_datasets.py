import random
import shutil
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path_to_dataset_folder>")
        sys.exit(1)

    data_dir = Path(sys.argv[1])
    if not data_dir.exists():
        print("Provided path does not exist.")
        sys.exit(1)

    parent_dir = data_dir.parent
    output_dirs = {
        "training": parent_dir / "training",
        "validation": parent_dir / "validation",
        "testing": parent_dir / "testing"
    }

    # Create output folders if they don't exist
    for dir_path in output_dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)

    # Find all .gui files and derive base filenames (0, 1, ...)
    base_filenames = sorted([f.stem for f in data_dir.glob("*.gui")], key=lambda x: int(x))
    total = len(base_filenames)

    # Shuffle for randomness
    random.shuffle(base_filenames)

    # Split sizes
    train_end = int(total * 0.8)
    val_end = train_end + int(total * 0.1)

    splits = {
        "training": base_filenames[:train_end],
        "validation": base_filenames[train_end:val_end],
        "testing": base_filenames[val_end:]
    }

    # Move and rename files
    for split_name, files in splits.items():
        for new_idx, base in enumerate(files):
            for ext in [".png", ".gui"]:
                src = data_dir / f"{base}{ext}"
                dst = output_dirs[split_name] / f"{new_idx}{ext}"
                if src.exists():
                    shutil.copy(str(src), str(dst))

    print(f"Split completed! {total} samples distributed into training, validation, and testing.")


if __name__ == "__main__":
    main()
