# Gym Tracker

Prosty tracker treningów w Pythonie. Program działa w terminalu i zapisuje historię w lokalnym pliku JSON.

## Wymagania

- Python 3.8 lub nowszy
- Bez dodatkowych bibliotek do instalowania

## Uruchomienie

1. Pobierz projekt lub sklonuj repozytorium.
2. Otwórz terminal w folderze projektu.
3. Uruchom:

```bash
python gym_tracker.py
```

W systemie Windows, jeśli polecenie `python` nie działa, spróbuj:

```powershell
py gym_tracker.py
```

## Co potrafi program

- dodaje trening, ćwiczenia i serie;
- przyjmuje ciężar i powtórzenia, np. `80 10`, `80x10` lub `80,5 10`;
- wyświetla historię i łączny tonaż sesji;
- pokazuje rekordowy ciężar dla każdego ćwiczenia;
- zapisuje dane w pliku `gym_workouts.json` obok programu.

Plik z treningami jest lokalny i został dodany do `.gitignore`, więc nie będzie przesyłany do GitHuba. Zrób jego kopię, jeśli chcesz przenieść historię na inny komputer.

## Dodanie projektu do GitHuba

Na GitHubie utwórz nowe repozytorium, a następnie wybierz **Add file → Upload files** i wgraj pliki z tego folderu. Możesz też wypakować ZIP i przesłać jego zawartość.
