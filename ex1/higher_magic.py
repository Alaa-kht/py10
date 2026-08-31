from collections.abc import Callable


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target}"


def heal(target: str, power: int) -> str:
    return f"Heals {target}"


def power_echo(target: str, power: int) -> str:
    return str(power)


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined(target: str, power: int) -> tuple:
        return spell1(target, power), spell2(target, power)

    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)

    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def guarded(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"

    return guarded


def spell_sequence(spells: list[Callable]) -> Callable:
    def sequence(target: str, power: int) -> list:
        return [spell(target, power) for spell in spells]

    return sequence


def main() -> None:
    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    result = combined("Dragon", 10)
    print(f"Combined spell result: {result[0]}, {result[1]}")

    print("\nTesting power amplifier...")
    mega_check = power_amplifier(power_echo, 3)
    print(f"Original: {power_echo('Dragon', 10)}, "
          f"Amplified: {mega_check('Dragon', 10)}")

    print("\nTesting conditional caster...")
    guarded_fireball = conditional_caster(
        lambda target, power: power >= 20, fireball
    )
    print(guarded_fireball("Dragon", 10))
    print(guarded_fireball("Dragon", 25))

    print("\nTesting spell sequence...")
    combo = spell_sequence([fireball, heal])
    print(combo("Dragon", 10))


if __name__ == "__main__":
    main()
