# Data Light Simulation

Projekt dyplomowy z zakresu optymalizacji rozmieszczenia źródeł światła przy użyciu algorytmów genetycznych.

## Opis projektu

Aplikacja wykorzystuje algorytmy genetyczne do optymalizacji rozmieszczenia źródeł światła w przestrzeni trójwymiarowej. Program symuluje rozkład natężenia oświetlenia, uwzględniając pozycję źródeł światła, ich światłość (mierzoną w kandelach) oraz kąt oprawy światła.

## Wymagania systemowe

- Python 3.x
- Następujące biblioteki Python:
  - `matplotlib` - do wizualizacji wyników
  - `numpy` - do obliczeń numerycznych

## Instalacja

### 1. Rozpakowanie zipa

### 2. Instalacja zależności

Zainstaluj wymagane biblioteki Python przy użyciu pip:

```bash
pip install matplotlib numpy
```

## Uruchamianie programu

### Generowanie pomiarów

Skrypt `generator. py` służy do generowania symulowanych pomiarów natężenia oświetlenia:

```bash
python generator.py
```

Skrypt `generator3.py` generuje pomiary uwzględniając kształt stożkowy wiązki światła:

```bash
python generator3.py
```

### Wizualizacja wyników - Wykresy fitness

Aby wyświetlić wykresy dopasowania najlepszego osobnika w kolejnych pokoleniach:

```bash
python script.py
```

Dla bardziej zaawansowanej analizy hiperparametrów:

```bash
python script2.py
```

### Generowanie map cieplnych (heatmap)

Wizualizacja rozkładu natężenia oświetlenia w przestrzeni:

```bash
python heatmap.py
```

Dla symulacji z uwzględnieniem generacji:

```bash
python heatmap_sim.py
```

### Wizualizacja 3D (Blender)

Skrypt `visualisation3D.py` służy do wizualizacji wyników w programie Blender.

**Uwaga:** Ten skrypt wymaga uruchomienia w środowisku Blender:

1. Otwórz Blender
2. Przejdź do zakładki "Scripting"
3. Otwórz plik `visualisation3D.py`
4. Skopiuj zawartość pliku do skryptu w Blenderze
5. Uruchom skrypt

## Struktura projektu

```
data_light_simulation/
├── generator.py          # Generator pomiarów (pojedyncze źródło światła)
├── generator3.py         # Generator pomiarów (kształt stożkowy wiązki)
├── script.py            # Wizualizacja wyników treningu
├── script2.py           # Analiza hiperparametrów
├── heatmap.py           # Generowanie map cieplnych
├── heatmap_sim.py       # Symulacja map cieplnych dla generacji
├── visualisation3D.py   # Wizualizacja 3D w Blender
├── measurements/        # Katalog z danymi eksperymentalnymi
└── results/            # Katalog z wynikami algorytmów genetycznych
    ├── v3/             # Wyniki wersji 3
    ├── v4/             # Wyniki wersji 4
    └── v4_par/         # Wyniki optymalizacji hiperparametrów
```

## Format plików wynikowych

Pliki wynikowe (np. `results/v4/ga4_exp001_1.txt`) zawierają informacje o parametrach algorytmu genetycznego i kolejnych generacjach:

```
Generation X:  Best fitness = Y
Individual positions: [x y z] [x y z] ...
Individual candel values: I1 I2 ...
Individual angle values: α1 α2 ...
```

## Przykłady użycia

### Wygenerowanie danych pomiarowych

```bash
python generator.py
```

### Analiza funkcji przystosowania

```bash
python script.py
```

### Wizualizacja rozkładu światła

```bash
python heatmap.py
```
