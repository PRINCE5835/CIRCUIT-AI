import asyncio
import logging
from functools import lru_cache
from pathlib import Path

import numpy as np

from engine.core.config import settings

logger = logging.getLogger(__name__)

ELECTRONICS_CLASSES = [
    "resistor", "capacitor", "inductor", "diode", "transistor",
    "led", "ic", "connector", "switch", "relay",
    "transformer", "potentiometer", "fuse", "crystal", "battery",
    "sensor", "motor", "heat_sink", "button", "jumper",
]


class YOLODetector:
    def __init__(self):
        self._model = None
        self._model_path = Path(settings.yolo_model_path) / "best.pt"
        self._loaded = False

    @property
    def is_available(self) -> bool:
        return self._model_path.exists()

    async def load(self):
        if self._loaded:
            return
        if not self.is_available:
            logger.warning("YOLO model not found at %s", self._model_path)
            return
        try:
            from ultralytics import YOLO
            self._model = await asyncio.to_thread(
                lambda: YOLO(str(self._model_path))
            )
            self._loaded = True
            logger.info("YOLO model loaded from %s", self._model_path)
        except Exception as e:
            logger.error("Failed to load YOLO model: %s", e)

    async def detect(
        self,
        image_bytes: bytes,
        confidence_threshold: float = 0.4,
        iou_threshold: float = 0.45,
    ) -> list[dict]:
        if not self._loaded:
            await self.load()
        if not self._model:
            return []

        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            import cv2
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            results = await asyncio.to_thread(
                lambda: self._model(
                    img,
                    conf=confidence_threshold,
                    iou=iou_threshold,
                    verbose=False,
                )
            )

            components = []
            for r in results:
                boxes = r.boxes
                if boxes is None:
                    continue
                for box in boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    x1, y1, x2, y2 = map(float, box.xyxy[0])
                    class_name = self._model.names[cls_id] if self._model.names else ELECTRONICS_CLASSES[cls_id] if cls_id < len(ELECTRONICS_CLASSES) else f"class_{cls_id}"

                    components.append({
                        "name": class_name,
                        "type": _map_to_type(class_name),
                        "confidence": round(conf, 3),
                        "quantity": 1,
                        "package": "",
                        "markings": "",
                        "bbox": [x1, y1, x2, y2],
                    })

            merged = _merge_duplicates(components)
            return merged

        except Exception as e:
            logger.error("YOLO detection error: %s", e)
            return []


def _map_to_type(name: str) -> str:
    name_lower = name.lower()
    if "resistor" in name_lower:
        return "resistor"
    if "capacitor" in name_lower or "capacit" in name_lower:
        return "capacitor"
    if "inductor" in name_lower:
        return "inductor"
    if "diode" in name_lower or "led" in name_lower:
        return "diode"
    if "transistor" in name_lower:
        return "transistor"
    if "ic" in name_lower or "chip" in name_lower or "integrated" in name_lower:
        return "ic"
    if "connector" in name_lower or "header" in name_lower or "pin" in name_lower:
        return "connector"
    if "switch" in name_lower:
        return "switch"
    if "relay" in name_lower:
        return "relay"
    if "transformer" in name_lower:
        return "transformer"
    if "battery" in name_lower or "cell" in name_lower:
        return "battery"
    if "sensor" in name_lower:
        return "sensor"
    if "motor" in name_lower:
        return "motor"
    if "fuse" in name_lower:
        return "fuse"
    return "other"


def _merge_duplicates(components: list[dict]) -> list[dict]:
    if not components:
        return []
    merged = {}
    for c in components:
        key = (c["name"], c["type"])
        if key in merged:
            merged[key]["quantity"] += 1
            merged[key]["confidence"] = max(merged[key]["confidence"], c["confidence"])
        else:
            merged[key] = dict(c)
    return list(merged.values())


detector = YOLODetector()
