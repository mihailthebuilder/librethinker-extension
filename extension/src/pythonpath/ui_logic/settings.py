import json
import uno
from pathlib import Path


class Settings:
    def __init__(self, ctx):
        self.settingsFilePath = self.getSettingsFilePath(ctx)
        if self.settingsFilePath.exists():
            with open(self.settingsFilePath, "r", encoding="utf-8") as f:
                data: dict[str, str, str] = json.load(f)
        else:
            data = {}

        self.modelId = data.get("modelId", "")
        self.apiKey = data.get("apiKey", "")
        self.modelUrl = data.get("modelUrl", "")

    @staticmethod
    def getSettingsFilePath(ctx) -> Path:
        path_settings = ctx.getByName("/singletons/com.sun.star.util.thePathSettings")
        user_config_url = path_settings.getPropertyValue("UserConfig")
        user_config_path = Path(uno.fileUrlToSystemPath(user_config_url))
        return user_config_path / "LibreThinkerConfig.json"

    def save(self, modelId: str, apiKey: str, modelUrl: str):
        data = {
            "modelId": modelId, 
            "apiKey": apiKey,
            "modelUrl": modelUrl,
        }
        with open(self.settingsFilePath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
