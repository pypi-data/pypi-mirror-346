"""
viby 配置管理模块
"""

import os
import yaml
import platform
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ModelProfileConfig:
    name: str = ""
    api_base_url: Optional[str] = None
    api_key: Optional[str] = None
    max_tokens: Optional[int] = None


class Config:
    """viby 应用的配置管理器"""

    def __init__(self):
        # Default global API settings
        self.default_api_base_url: Optional[str] = "http://localhost:11434"
        self.default_api_key: Optional[str] = None

        # Model profiles
        self.default_model: ModelProfileConfig = ModelProfileConfig(name="qwen3:30b")
        self.think_model: Optional[ModelProfileConfig] = ModelProfileConfig(
            name=""
        )  # Initialize with empty name
        self.fast_model: Optional[ModelProfileConfig] = ModelProfileConfig(
            name=""
        )  # Initialize with empty name

        # Other general settings
        self.temperature: float = 0.7
        self.max_tokens: int = 40960
        self.api_timeout: int = 300
        self.language: str = "en-US"  # options: en-US, zh-CN
        self.enable_mcp: bool = True
        self.mcp_config_folder: Optional[str] = None
        self.enable_yolo_mode: bool = False  # yolo模式默认关闭

        # 为不同操作系统获取正确的配置目录路径
        self.config_dir: Path = self._get_config_dir()
        self.config_path: Path = self.config_dir / "config.yaml"

        # 确保配置目录存在
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.is_first_run: bool = not self.config_path.exists()
        if self.is_first_run:
            self.save_config()  # Save initial new-format config

        self.load_config()

    def _get_config_dir(self) -> Path:
        """
        获取适合当前操作系统的配置目录路径
        """
        system = platform.system()

        if system == "Windows":
            # Windows上使用 %APPDATA%\viby
            base_dir = Path(os.environ.get("APPDATA", str(Path.home())))
            return base_dir / "viby"
        else:
            return Path.home() / ".config" / "viby"

    def _to_dict(self, obj: Any) -> Any:
        """将对象转换为字典，处理嵌套对象"""
        if hasattr(obj, "__dict__"):
            return {
                k: self._to_dict(v) for k, v in obj.__dict__.items() if v is not None
            }
        elif isinstance(obj, list):
            return [self._to_dict(i) for i in obj]
        return obj

    def load_config(self) -> None:
        """从YAML文件加载配置，支持从旧格式迁移"""
        try:
            if self.config_path.exists():
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config_data = yaml.safe_load(f) or {}

                # --- 从旧格式迁移 ---
                migrated = False
                if "model" in config_data and isinstance(config_data["model"], str):
                    print("正在将旧配置格式迁移到新结构...")
                    self.default_api_base_url = config_data.get(
                        "base_url", self.default_api_base_url
                    )
                    self.default_api_key = config_data.get(
                        "api_key", self.default_api_key
                    )

                    self.default_model.name = config_data.get(
                        "model", self.default_model.name
                    )
                    self.default_model.api_base_url = config_data.get("base_url")

                    if config_data.get("think_model"):
                        if self.think_model is None:
                            self.think_model = ModelProfileConfig()
                        self.think_model.name = config_data["think_model"]
                        self.think_model.api_base_url = config_data.get(
                            "think_model_base_url"
                        )
                    else:
                        self.think_model = None

                    if config_data.get("fast_model"):
                        if self.fast_model is None:
                            self.fast_model = ModelProfileConfig()
                        self.fast_model.name = config_data["fast_model"]
                        self.fast_model.api_base_url = config_data.get(
                            "fast_model_base_url"
                        )
                    else:
                        self.fast_model = None

                    self.temperature = config_data.get("temperature", self.temperature)
                    self.max_tokens = config_data.get("max_tokens", self.max_tokens)
                    self.api_timeout = config_data.get("api_timeout", self.api_timeout)
                    self.language = config_data.get("language", self.language)
                    self.enable_mcp = config_data.get("enable_mcp", self.enable_mcp)
                    self.mcp_config_folder = config_data.get(
                        "mcp_config_folder", self.mcp_config_folder
                    )
                    migrated = True
                else:
                    self.default_api_base_url = config_data.get(
                        "default_api_base_url", self.default_api_base_url
                    )
                    self.default_api_key = config_data.get(
                        "default_api_key", self.default_api_key
                    )

                    default_model_data = config_data.get("default_model")
                    if default_model_data and isinstance(default_model_data, dict):
                        self.default_model = ModelProfileConfig(**default_model_data)

                    think_model_data = config_data.get("think_model")
                    if think_model_data and isinstance(think_model_data, dict):
                        self.think_model = ModelProfileConfig(**think_model_data)
                    elif not think_model_data:
                        self.think_model = None

                    fast_model_data = config_data.get("fast_model")
                    if fast_model_data and isinstance(fast_model_data, dict):
                        self.fast_model = ModelProfileConfig(**fast_model_data)
                    elif not fast_model_data:
                        self.fast_model = None

                    self.temperature = float(
                        config_data.get("temperature", self.temperature)
                    )
                    self.max_tokens = int(
                        config_data.get("max_tokens", self.max_tokens)
                    )
                    self.api_timeout = int(
                        config_data.get("api_timeout", self.api_timeout)
                    )
                    self.language = config_data.get("language", self.language)
                    self.enable_mcp = bool(
                        config_data.get("enable_mcp", self.enable_mcp)
                    )
                    self.mcp_config_folder = config_data.get(
                        "mcp_config_folder", self.mcp_config_folder
                    )
                    self.enable_yolo_mode = bool(
                        config_data.get("enable_yolo_mode", self.enable_yolo_mode)
                    )

                if migrated:
                    print("迁移完成。正在保存新格式的配置。")
                    self.save_config()

        except Exception as e:
            print(f"警告: 无法从 {self.config_path} 加载或迁移配置: {e}。使用默认值。")
            if not isinstance(self.default_model, ModelProfileConfig):
                self.default_model = ModelProfileConfig(name="qwen3:30b")
            self.think_model and self.fast_model

    def save_config(self) -> None:
        """将当前配置保存到 YAML 文件 (新格式)"""
        # 确保配置目录存在
        self.config_dir.mkdir(parents=True, exist_ok=True)

        config_data = {
            "default_api_base_url": self.default_api_base_url,
            "default_api_key": self.default_api_key,
            "default_model": self._to_dict(self.default_model)
            if self.default_model
            else None,
            "think_model": self._to_dict(self.think_model)
            if self.think_model and self.think_model.name
            else None,
            "fast_model": self._to_dict(self.fast_model)
            if self.fast_model and self.fast_model.name
            else None,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "api_timeout": self.api_timeout,
            "language": self.language,
            "enable_mcp": self.enable_mcp,
            "mcp_config_folder": self.mcp_config_folder,
            "enable_yolo_mode": self.enable_yolo_mode,
        }

        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(
                    config_data, f, sort_keys=False, default_flow_style=False
                )
        except Exception as e:
            print(f"警告: 无法保存配置到 {self.config_path}: {e}")

    def get_model_config(self, model_type: str = "default") -> Dict[str, Any]:
        """获取指定模型类型的完整配置，回退到全局默认值"""
        profile_to_use: Optional[ModelProfileConfig] = None

        if model_type == "default":
            profile_to_use = self.default_model
        elif model_type == "think" and self.think_model and self.think_model.name:
            profile_to_use = self.think_model
        elif model_type == "fast" and self.fast_model and self.fast_model.name:
            profile_to_use = self.fast_model
        else:
            profile_to_use = self.default_model

        if not profile_to_use or not profile_to_use.name:
            return {
                "model": "qwen3:30b",
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "base_url": self.default_api_base_url or "http://localhost:11434",
                "api_key": self.default_api_key,
                "api_timeout": self.api_timeout,
            }

        resolved_base_url = profile_to_use.api_base_url or self.default_api_base_url
        resolved_api_key = profile_to_use.api_key or self.default_api_key

        # 优先使用模型特定的 max_tokens 设置，如果没有则使用全局设置
        resolved_max_tokens = (
            profile_to_use.max_tokens
            if profile_to_use.max_tokens is not None
            else self.max_tokens
        )

        return {
            "model": profile_to_use.name,
            "temperature": self.temperature,
            "max_tokens": resolved_max_tokens,
            "base_url": resolved_base_url,
            "api_key": resolved_api_key,
            "api_timeout": self.api_timeout,
        }
