# Copyright © 2025 Saqib Ali Khan. All Rights Reserved.
# Licensed under Business Source License 1.1

"""Device capability detection utility.

Reports hardware capabilities (GPU, CPU, RAM) for client-side use.
Useful for clients deciding whether to run local models.

Install: pip install zeroveil[device]
"""

from __future__ import annotations

import logging
import os
import platform
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional

log = logging.getLogger("zeroveil.device_detector")


class DeviceCapability(Enum):
    """Device capability levels."""
    HIGH_POWER_GPU = auto()      # NVIDIA GPU with 8GB+ VRAM
    MEDIUM_POWER_GPU = auto()    # NVIDIA GPU with 4-8GB VRAM
    LOW_POWER_GPU = auto()       # NVIDIA GPU with <4GB VRAM
    CPU_CAPABLE = auto()         # CPU only (8+ cores, 16GB+ RAM)
    CPU_LIMITED = auto()         # Limited CPU
    MINIMAL = auto()             # Minimal hardware


@dataclass
class GPUInfo:
    """Information about a detected GPU."""
    id: int
    name: str
    memory_total_mb: float
    memory_free_mb: float
    load_percent: float

    @property
    def memory_total_gb(self) -> float:
        return self.memory_total_mb / 1024

    @property
    def memory_free_gb(self) -> float:
        return self.memory_free_mb / 1024


@dataclass
class SystemInfo:
    """System hardware information."""
    cpu_count: int
    cpu_physical_cores: int
    ram_total_gb: float
    ram_available_gb: float
    platform: str


@dataclass
class DeviceDetectionResult:
    """Result of device capability detection."""
    capability: DeviceCapability
    gpus: List[GPUInfo] = field(default_factory=list)
    system: Optional[SystemInfo] = None

    @property
    def has_gpu(self) -> bool:
        return len(self.gpus) > 0

    @property
    def total_vram_gb(self) -> float:
        return sum(g.memory_total_gb for g in self.gpus)

    @property
    def best_gpu(self) -> Optional[GPUInfo]:
        if not self.gpus:
            return None
        return max(self.gpus, key=lambda g: g.memory_total_mb)


def _detect_gpus_gputil() -> List[GPUInfo]:
    """Detect NVIDIA GPUs using GPUtil."""
    try:
        import GPUtil  # type: ignore
    except ImportError:
        return []

    try:
        gpus = GPUtil.getGPUs()
        return [
            GPUInfo(
                id=gpu.id,
                name=gpu.name,
                memory_total_mb=gpu.memoryTotal,
                memory_free_mb=gpu.memoryFree,
                load_percent=gpu.load * 100,
            )
            for gpu in gpus
        ]
    except Exception:
        return []


def _detect_gpus_torch() -> List[GPUInfo]:
    """Detect GPUs using PyTorch (fallback)."""
    try:
        import torch  # type: ignore
    except ImportError:
        return []

    if not torch.cuda.is_available():
        return []

    try:
        result = []
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            total = props.total_memory / (1024 ** 2)
            try:
                torch.cuda.set_device(i)
                free = torch.cuda.mem_get_info()[0] / (1024 ** 2)
            except Exception:
                free = total * 0.9

            result.append(GPUInfo(
                id=i,
                name=props.name,
                memory_total_mb=total,
                memory_free_mb=free,
                load_percent=0.0,
            ))
        return result
    except Exception:
        return []


def _detect_system_info() -> SystemInfo:
    """Detect CPU and RAM information."""
    import sys

    cpu_count = os.cpu_count() or 1
    cpu_physical = cpu_count
    ram_total = 8.0
    ram_available = 4.0

    try:
        import psutil  # type: ignore
        cpu_physical = psutil.cpu_count(logical=False) or cpu_count
        ram_total = psutil.virtual_memory().total / (1024 ** 3)
        ram_available = psutil.virtual_memory().available / (1024 ** 3)
    except ImportError:
        pass

    return SystemInfo(
        cpu_count=cpu_count,
        cpu_physical_cores=cpu_physical,
        ram_total_gb=ram_total,
        ram_available_gb=ram_available,
        platform=platform.system(),
    )


def _classify(gpus: List[GPUInfo], system: SystemInfo) -> DeviceCapability:
    """Classify device capability."""
    if gpus:
        best = max(gpus, key=lambda g: g.memory_total_mb)
        vram = best.memory_total_gb
        if vram >= 8:
            return DeviceCapability.HIGH_POWER_GPU
        elif vram >= 4:
            return DeviceCapability.MEDIUM_POWER_GPU
        else:
            return DeviceCapability.LOW_POWER_GPU

    if system.cpu_physical_cores >= 8 and system.ram_total_gb >= 16:
        return DeviceCapability.CPU_CAPABLE
    elif system.cpu_physical_cores >= 4 and system.ram_total_gb >= 8:
        return DeviceCapability.CPU_LIMITED

    return DeviceCapability.MINIMAL


def detect_device_capabilities() -> DeviceDetectionResult:
    """Detect device capabilities.

    Returns hardware information useful for deciding local vs cloud processing.

    Example:
        result = detect_device_capabilities()
        print(f"Capability: {result.capability.name}")
        if result.has_gpu:
            print(f"GPU: {result.best_gpu.name} ({result.best_gpu.memory_total_gb:.1f}GB)")
    """
    gpus = _detect_gpus_gputil() or _detect_gpus_torch()
    system = _detect_system_info()
    capability = _classify(gpus, system)

    return DeviceDetectionResult(
        capability=capability,
        gpus=gpus,
        system=system,
    )


def print_device_info() -> None:
    """Print detected device information."""
    result = detect_device_capabilities()

    print("\n=== Device Detection ===")
    print(f"Capability: {result.capability.name}")

    if result.gpus:
        print(f"\nGPUs ({len(result.gpus)}):")
        for gpu in result.gpus:
            print(f"  [{gpu.id}] {gpu.name}")
            print(f"      VRAM: {gpu.memory_total_gb:.1f}GB ({gpu.memory_free_gb:.1f}GB free)")

    if result.system:
        print(f"\nSystem:")
        print(f"  Platform: {result.system.platform}")
        print(f"  CPU: {result.system.cpu_physical_cores} cores")
        print(f"  RAM: {result.system.ram_total_gb:.1f}GB ({result.system.ram_available_gb:.1f}GB free)")

    print()


if __name__ == "__main__":
    print_device_info()
