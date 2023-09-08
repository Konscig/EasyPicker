from environs import Env
from dataclasses import dataclass


@dataclass
class Bot:
    bot_token: str
    api_id: int
    api_hash: str
    group_id: str
    group_name: str
    admin_id: int

@dataclass
class Settings:
    bot: Bot


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bot=Bot(
            bot_token=env.str("HTTP_API"),
            api_id=env.int("API_ID"),
            api_hash=env.str("API_HASH"),
            group_id=env.str("GROUP_ID"),
            group_name=env.str("GROUP_NAME"),
            admin_id=env.int("ADMIN_ID")
        )
    )


settings = get_settings('api')
print(settings)
