import json
from pathlib import Path


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

FAVORITES_FILE = DATA_DIR / "favorites.json"


class FavoriteStorage:

    @staticmethod
    def load():
        """Load all favorite cities."""

        if not FAVORITES_FILE.exists():
            return []

        with open(FAVORITES_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save(favorites):
        """Overwrite favorites file."""

        with open(FAVORITES_FILE, "w") as f:
            json.dump(favorites, f, indent=4)

    @staticmethod
    def add(city, country):

        favorites = FavoriteStorage.load()

        exists = any(
            fav["city"].lower() == city.lower()
            and fav["country"].lower() == country.lower()
            for fav in favorites
        )

        if exists:
            return

        favorites.append(
            {
                "city": city,
                "country": country,
            }
        )

        FavoriteStorage.save(favorites)

    @staticmethod
    def remove(city, country):

        favorites = FavoriteStorage.load()

        favorites = [
            fav
            for fav in favorites
            if not (
                fav["city"].lower() == city.lower()
                and fav["country"].lower() == country.lower()
            )
        ]

        FavoriteStorage.save(favorites)