import json
import os
import re
from datetime import datetime

DATA_FILE = "gym_workouts.json"


def load_workouts():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            workouts = json.load(file)
        return workouts if isinstance(workouts, list) else []
    except (json.JSONDecodeError, OSError):
        print("Nie udało się odczytać pliku z treningami.")
        return []


def save_workouts(workouts):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(workouts, file, indent=4, ensure_ascii=False)
        return True
    except OSError:
        print("Nie udało się zapisać treningu.")
        return False


def get_date():
    while True:
        date_str = input(
            "Podaj datę (RRRR-MM-DD) [Enter = dzisiaj]: "
        ).strip()

        if not date_str:
            return datetime.now().strftime("%Y-%m-%d")

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Niepoprawna data. Użyj formatu RRRR-MM-DD.")


def parse_set_input(user_input):
    """Obsługuje np. 80 10, 80x10 oraz 80,5 10."""
    value = user_input.strip().lower().replace("x", " ")
    match = re.fullmatch(r"\s*(\d+(?:[.,]\d+)?)\s+(\d+)\s*", value)

    if not match:
        return None

    weight = float(match.group(1).replace(",", "."))
    reps = int(match.group(2))

    if weight < 0 or reps <= 0:
        return None

    return weight, reps


def add_workout():
    print("\n--- NOWY TRENING ---")
    date_str = get_date()

    workout_name = input(
        "Nazwa treningu (np. Push, FBW, Klatka + Biceps): "
    ).strip() or "Trening ogólny"

    exercises = []

    while True:
        ex_name = input(
            "\nNazwa ćwiczenia (Enter, aby zakończyć trening): "
        ).strip()

        if not ex_name:
            break

        sets = []
        set_num = 1
        print(f"Dodajesz serie dla: {ex_name}")

        while True:
            sub_input = input(
                f"  Seria {set_num} — ciężar i powtórzenia "
                "(np. 80 10, 80x10 lub 80,5 10; Enter = koniec ćwiczenia): "
            ).strip()

            if not sub_input:
                break

            result = parse_set_input(sub_input)
            if result is None:
                print(
                    "  Błąd. Podaj np. 80 10 albo 80,5 10. "
                    "Ciężar nie może być ujemny, a powtórzenia muszą być większe od 0."
                )
                continue

            weight, reps = result
            sets.append({
                "set": set_num,
                "weight_kg": weight,
                "reps": reps,
            })
            set_num += 1

        if sets:
            exercises.append({"exercise": ex_name, "sets": sets})

    if not exercises:
        print("\nNie dodano żadnych ćwiczeń. Trening anulowany.")
        return

    workouts = load_workouts()
    existing_ids = [
        workout.get("id", 0)
        for workout in workouts
        if isinstance(workout, dict)
        and isinstance(workout.get("id", 0), int)
    ]
    new_id = max(existing_ids, default=0) + 1

    workouts.append({
        "id": new_id,
        "date": date_str,
        "name": workout_name,
        "exercises": exercises,
    })

    if save_workouts(workouts):
        print("\nTrening zapisany pomyślnie!")


def show_history():
    workouts = load_workouts()

    if not workouts:
        print("\nBrak zapisanych treningów.")
        return

    print("\n=== HISTORIA TRENINGÓW ===")
    for workout in reversed(workouts):
        print(
            f"\n[#{workout.get('id', '?')}] "
            f"{workout.get('date', 'Brak daty')} — "
            f"{workout.get('name', 'Trening')}"
        )
        total_tonnage = 0

        for exercise in workout.get("exercises", []):
            print(f"  • {exercise.get('exercise', 'Ćwiczenie')}:")
            for workout_set in exercise.get("sets", []):
                weight = workout_set.get("weight_kg", 0)
                reps = workout_set.get("reps", 0)
                set_number = workout_set.get("set", "?")
                total_tonnage += weight * reps
                print(
                    f"      Seria {set_number}: "
                    f"{weight:g} kg × {reps} powt."
                )

        print(f"   Łączny tonaż sesji: {total_tonnage:.1f} kg")


def show_personal_records():
    workouts = load_workouts()

    if not workouts:
        print("\nBrak danych do analizy rekordów.")
        return

    records = {}
    for workout in workouts:
        for exercise in workout.get("exercises", []):
            name = exercise.get("exercise", "").strip().title()
            for workout_set in exercise.get("sets", []):
                weight = workout_set.get("weight_kg", 0)
                if name and (
                    name not in records or weight > records[name]["weight"]
                ):
                    records[name] = {
                        "weight": weight,
                        "reps": workout_set.get("reps", 0),
                        "date": workout.get("date", "Brak daty"),
                    }

    print("\n=== REKORDY SIŁOWE (MAKSYMALNY CIĘŻAR) ===")
    for exercise_name, data in sorted(records.items()):
        print(
            f"  • {exercise_name}: {data['weight']:g} kg "
            f"na {data['reps']} powt. ({data['date']})"
        )


def main():
    while True:
        print("\n==============================")
        print("     GYM TRACKER - MENU       ")
        print("==============================")
        print("1. Dodaj nowy trening")
        print("2. Pokaż historię treningów")
        print("3. Pokaż rekordy (PRs)")
        print("4. Wyjście")

        choice = input("\nWybierz opcję (1-4): ").strip()

        if choice == "1":
            add_workout()
        elif choice == "2":
            show_history()
        elif choice == "3":
            show_personal_records()
        elif choice == "4":
            print("\nDo zobaczenia na kolejnym treningu!")
            break
        else:
            print("Niepoprawny wybór, spróbuj ponownie.")


if __name__ == "__main__":
    main()

