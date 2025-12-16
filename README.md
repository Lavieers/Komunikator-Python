# MessBOX - Wieloużytkownikowy Komunikator Python

MessBOX to lekka aplikacja typu czat oparta na architekturze klient-serwer, stworzona w języku Python. Projekt wykorzystuje bibliotekę `customtkinter` dla nowoczesnego wyglądu interfejsu oraz gniazda (sockets) do komunikacji w czasie rzeczywistym.

## Opis Projektu
Projekt umożliwia wielu użytkownikom jednoczesne połączenie się z centralnym serwerem, przesyłanie wiadomości publicznych, prywatnych oraz korzystanie z interaktywnych komend. Aplikacja została zaprojektowana z myślą o prostocie obsługi i estetyce wizualnej (obsługa motywów Dark/Light).

## Funkcje
* **Komunikacja w czasie rzeczywistym**: Wysyłanie i odbieranie wiadomości bez opóźnień.
* **Wiadomości prywatne**: Możliwość wysłania bezpośredniej wiadomości do konkretnego użytkownika za pomocą komendy `/msg`.
* **System komend**:
    * `/help` - Lista dostępnych funkcji.
    * `/online` - Sprawdzenie, kto aktualnie jest zalogowany.
    * `/fact` - Losowanie ciekawostki z bazy serwera.
    * `/nickname` - Zmiana nazwy użytkownika w trakcie sesji.
    * `/clear` - Czyszczenie okna rozmowy.
* **Interfejs Emoji**: Wbudowane okno wyboru emotikon oraz automatyczna konwersja kodów tekstowych (np. `:)` na 😊).
* **Statystyki sesji**: Licznik wysłanych i odebranych wiadomości widoczny w oknie klienta.
* **Powiadomienia dźwiękowe**: Sygnały dźwiękowe przy dołączaniu do czatu i odbieraniu wiadomości.
* **Historia czatu**: Serwer automatycznie zapisuje przebieg rozmów w pliku `chat_history.txt`.

## Zastosowanie
Projekt może służyć jako:
1.  Baza do budowy własnego, bezpiecznego komunikatora wewnątrz sieci lokalnej (LAN).
2.  Materiał edukacyjny do nauki programowania sieciowego (Sockets) i wielowątkowości (Threading) w Pythonie.
3.  Przykład implementacji nowoczesnego GUI za pomocą `CustomTkinter`.

## Instalacja i Uruchomienie

1. **Wymagania**: 
Python 3.x oraz biblioteka `customtkinter`.
   ```bash
   pip install customtkinter


## Autorzy
 * Kinga Łopata
 * Amelia Kucharz
 * Piotr Kula
