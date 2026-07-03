"""
Train YOLOv8 on Electronics Components Dataset.

Usage:
    # Download dataset first (see download_electronics_dataset.py)
    python scripts/train_yolo.py --data ./datasets/components/data.yaml --epochs 50

    # Use a custom dataset
    python scripts/train_yolo.py --data ./datasets/custom/data.yaml --model yolov8s.pt --epochs 100
"""
import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Train YOLOv8 for electronics component detection")
    parser.add_argument("--data", default="./datasets/components/data.yaml", help="Dataset YAML path")
    parser.add_argument("--model", default="yolov8n.pt", help="Base model (yolov8n.pt, yolov8s.pt, etc.)")
    parser.add_argument("--epochs", type=int, default=50, help="Number of epochs")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--device", default="cpu", help="Training device (cpu, cuda:0)")
    parser.add_argument("--project", default="runs/train", help="Project directory")
    parser.add_argument("--name", default="electronics-yolo", help="Experiment name")
    args = parser.parse_args()

    try:
        from ultralytics import YOLO
    except ImportError:
        print("Installing ultralytics...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "ultralytics"])
        from ultralytics import YOLO

    print(f"Training {args.model} on {args.data}")
    print(f"  Epochs: {args.epochs}, Img size: {args.imgsz}, Batch: {args.batch}")
    print(f"  Device: {args.device}")

    model = YOLO(args.model)
    results = model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        project=args.project,
        name=args.name,
        patience=15,
        save=True,
        augment=True,
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=0.0,
        translate=0.1,
        scale=0.5,
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        mosaic=1.0,
        mixup=0.0,
    )

    best_model = f"{args.project}/{args.name}/weights/best.pt"
    print(f"\nTraining complete! Best model saved to: {best_model}")
    print(f"  mAP@0.5: {results.results_dict.get('metrics/mAP50(B)', 'N/A'):.4f}")
    print(f"  mAP@0.5:0.95: {results.results_dict.get('metrics/mAP50-95(B)', 'N/A'):.4f}")


if __name__ == "__main__":
    main()
