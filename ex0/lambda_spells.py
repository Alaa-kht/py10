def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda artifact: artifact["power"],
                  reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda mage: mage["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: f"* {spell} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    powers = list(map(lambda mage: mage["power"], mages))
    return {
        "max_power": max(mages, key=lambda mage: mage["power"])["power"],
        "min_power": min(mages, key=lambda mage: mage["power"])["power"],
        "avg_power": round(sum(powers) / len(powers), 2),
    }


def main() -> None:
    artifacts = [
        {"name": "Crystal Orb", "power": 85, "type": "orb"},
        {"name": "Fire Staff", "power": 92, "type": "staff"},
        {"name": "Ice Wand", "power": 60, "type": "wand"},
    ]
    mages = [
        {"name": "Alex", "power": 75, "element": "fire"},
        {"name": "Jordan", "power": 45, "element": "water"},
        {"name": "Riley", "power": 90, "element": "earth"},
    ]
    spells = ["fireball", "heal", "shield"]

    print("Testing artifact sorter...")
    top = artifact_sorter(artifacts)
    print(f"{top[0]['name']} ({top[0]['power']} power) comes before "
          f"{top[1]['name']} ({top[1]['power']} power)")

    print("\nTesting power filter...")
    strong_mages = power_filter(mages, 60)
    names = ", ".join(mage["name"] for mage in strong_mages)
    print(f"Mages with power >= 60: {names}")

    print("\nTesting spell transformer...")
    print(" ".join(spell_transformer(spells)))

    print("\nTesting mage stats...")
    stats = mage_stats(mages)
    print(f"Max power: {stats['max_power']}, "
          f"Min power: {stats['min_power']}, "
          f"Avg power: {stats['avg_power']}")


if __name__ == "__main__":
    main()
