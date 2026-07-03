"""
Download Electronics Components Dataset for YOLO training.

Sources (tried in order):
  1. Kaggle: "Electronic components and devices" by Sunim Acharya (11K images, 36 classes)
  2. Roboflow: "Electronics Components" by Jovine (YOLO-format annotations)

Usage:
    # From Kaggle (requires kaggle API key)
    python scripts/download_electronics_dataset.py --source kaggle

    # From Roboflow (requires roboflow API key)
    python scripts/download_electronics_dataset.py --source roboflow --api-key YOUR_KEY

    # Direct pretrained model download (no dataset needed for inference)
    python scripts/download_electronics_dataset.py --source pretrained
"""
import argparse
import subprocess
import sys
from pathlib import Path
import urllib.request
import zipfile
import shutil


DATASETS_DIR = Path("./datasets")
MODELS_DIR = Path("./engine/models/yolo")


def download_pretrained():
    """Download a pre-trained YOLO model for electronics components."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # Try to get a pre-trained model from GitHub
    urls = [
        # Pre-trained model from hassanmroueh2003's project
        "https://github.com/hassanmroueh2003/Electronic-Component-Detection-using-YOLOv8/raw/main/best.pt",
        # Fallback: base YOLOv8n
    ]

    for url in urls:
        try:
            dest = MODELS_DIR / "best.pt"
            print(f"Downloading {url} ...")
            urllib.request.urlretrieve(url, dest)
            print(f"  Saved to {dest}")
            return
        except Exception as e:
            print(f"  Failed: {e}")

    # Fallback: download base YOLOv8n
    print("Downloading base YOLOv8n (untrained on electronics)...")
    try:
        from ultralytics import YOLO
        model = YOLO("yolov8n.pt")
        model.save(str(MODELS_DIR / "best.pt"))
        print(f"  Saved to {MODELS_DIR / 'best.pt'}")
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "ultralytics"])
        from ultralytics import YOLO
        model = YOLO("yolov8n.pt")
        model.save(str(MODELS_DIR / "best.pt"))
        print(f"  Saved to {MODELS_DIR / 'best.pt'}")


def download_kaggle():
    """Download from Kaggle."""
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)
    dest = DATASETS_DIR / "kaggle_electronics"

    if dest.exists():
        print(f"Dataset already exists at {dest}")
        return

    print("Downloading from Kaggle: 'electronic-components' by aryaminus")
    print("This requires kaggle API credentials (~/.kaggle/kaggle.json)")
    try:
        subprocess.check_call([
            sys.executable, "-m", "kaggle", "datasets", "download",
            "-d", "aryaminus/electronic-components",
            "-p", str(dest),
        ])
        # Unzip
        zip_path = dest / "electronic-components.zip"
        if zip_path.exists():
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(dest)
            zip_path.unlink()
        print(f"  Dataset saved to {dest}")
    except Exception as e:
        print(f"  Kaggle download failed: {e}")
        print("  Install kaggle: pip install kaggle")
        print("  Set up API key: https://www.kaggle.com/docs/api")


def download_roboflow(api_key: str):
    """Download from Roboflow Universe."""
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)
    dest = DATASETS_DIR / "roboflow_electronics"

    if dest.exists():
        print(f"Dataset already exists at {dest}")
        return

    print("Downloading from Roboflow: 'electronics-components' by Jovine")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "roboflow",
        ])
        from roboflow import Roboflow
        rf = Roboflow(api_key=api_key)
        project = rf.workspace("jovine").project("electronics-components")
        version = project.version(1)
        version.download(model_format="yolov8", location=str(dest))
        print(f"  Dataset saved to {dest}")
    except Exception as e:
        print(f"  Roboflow download failed: {e}")
        print(f"  Get API key at: https://universe.roboflow.com/jovine/electronics-components")


def convert_kaggle_to_yolo():
    """Convert Kaggle classification dataset to YOLO detection format.
    The Kaggle dataset is for classification (36 class folders).
    This creates a basic train/val split for detection training."""
    src = DATASETS_DIR / "kaggle_electronics"
    dest = DATASETS_DIR / "components"

    if not src.exists():
        print("Kaggle dataset not found. Run with --source kaggle first.")
        return

    if dest.exists():
        print(f"YOLO dataset already exists at {dest}")
        return

    print("Converting Kaggle dataset to YOLO format...")
    print("NOTE: This creates pseudo-annotations (full-image bounding boxes).")
    print("For production, use Roboflow dataset with real annotations.")

    (dest / "train" / "images").mkdir(parents=True, exist_ok=True)
    (dest / "valid" / "images").mkdir(parents=True, exist_ok=True)
    (dest / "train" / "labels").mkdir(parents=True, exist_ok=True)
    (dest / "valid" / "labels").mkdir(parents=True, exist_ok=True)

    import random
    random.seed(42)

    class_names = sorted([p.name for p in src.iterdir() if p.is_dir()])
    class_map = {name: i for i, name in enumerate(class_names)}

    all_images = []
    for class_dir in src.iterdir():
        if not class_dir.is_dir():
            continue
        class_name = class_dir.name
        cls_id = class_map[class_name]
        for img_path in class_dir.glob("*.*"):
            if img_path.suffix.lower() in (".jpg", ".jpeg", ".png", ".bmp", ".webp"):
                all_images.append((img_path, cls_id, class_name))

    random.shuffle(all_images)
    split = int(len(all_images) * 0.8)
    train_imgs = all_images[:split]
    val_imgs = all_images[split:]

    for img_set, split_name in [(train_imgs, "train"), (val_imgs, "valid")]:
        for img_path, cls_id, _ in img_set:
            img_dest = dest / split_name / "images" / img_path.name
            shutil.copy2(img_path, img_dest)

            label_path = dest / split_name / "labels" / f"{img_path.stem}.txt"
            pseudo_bbox = "0.5 0.5 1.0 1.0"
            label_path.write_text(f"{cls_id} {pseudo_bbox}\n")

    yaml_path = dest / "data.yaml"
    yaml_content = (
        f"train: {dest}/train/images\n"
        f"val: {dest}/valid/images\n\n"
        f"nc: {len(class_names)}\n"
        f"names: {class_names}\n"
    )
    yaml_path.write_text(yaml_content)

    print(f"Converted {len(train_imgs)} train + {len(val_imgs)} val images")
    print(f"Classes ({len(class_names)}): {class_names}")
    print(f"YOLO dataset ready at: {dest}")
    print(f"Config: {yaml_path}")
    print("\nTrain with:")
    print(f"  python scripts/train_yolo.py --data {yaml_path}")


def main():
    parser = argparse.ArgumentParser(description="Download electronics components dataset")
    parser.add_argument("--source", choices=["kaggle", "roboflow", "pretrained", "convert"],
                       default="pretrained", help="Download source")
    parser.add_argument("--api-key", help="API key (Roboflow)")
    args = parser.parse_args()

    if args.source == "kaggle":
        download_kaggle()
    elif args.source == "roboflow":
        if not args.api_key:
            print("Error: --api-key required for Roboflow")
            sys.exit(1)
        download_roboflow(args.api_key)
    elif args.source == "pretrained":
        download_pretrained()
    elif args.source == "convert":
        convert_kaggle_to_yolo()


if __name__ == "__main__":
    main()
