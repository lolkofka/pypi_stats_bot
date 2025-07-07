import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

ENV_PATH = ".env"

# dir_name = os.path.dirname(ENV_PATH)

# if not os.path.exists(dir_name):
#     os.makedirs(dir_name)

if not os.path.exists(ENV_PATH):
    with open(ENV_PATH, "w") as f:
        f.write(
            "BOT_TOKEN=\n"
            "PEPY_API_KEY=\n"
            "ADMINS=1043461599,787751346\n"
            "PACKAGES=aiovaksms,synkvaksms,vaksms,vaksmsapi\n"
        )
    print("✅ Файл .env был создан. Заполни его и перезапусти бота.")
    exit()

load_dotenv(dotenv_path=ENV_PATH)

class Config(BaseModel):
    bot_token: str = Field(..., env="BOT_TOKEN")
    pepy_api_key: str = Field(..., env="PEPY_API_KEY")
    admins: list[int]
    packages: list[str]

    @classmethod
    def load(cls):
        raw_admins = os.getenv("ADMINS", "")
        raw_packages = os.getenv("PACKAGES", "")
        admin_list = [int(i.strip()) for i in raw_admins.split(",") if i.strip().isdigit()]
        package_list = [p.strip() for p in raw_packages.split(",") if p.strip()]
        return cls(
            bot_token=os.getenv("BOT_TOKEN"),
            pepy_api_key=os.getenv("PEPY_API_KEY"),
            admins=admin_list,
            packages=package_list
        )
