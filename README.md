# Smashing-Wallpaper-Downloader
 CLI утилита, которая скачивает с сайта **Smashing magazine** все обои в требуемом разрешение за указанный месяц-год в текущую директорию пользователя.

## Установка и запуск

### 1. Создать виртуальное окружение 

```powershell
python -m venv .venv
```

### 2. Активировать виртуальное окружение (Windows)

```powershell
.venv/Scripts/activate
```

### 3. Установить зависимости
```powershell
pip install -r requirements.txt

```
$ python main.py --help
Usage: main.py [OPTIONS]

  Program for downloading files from 'www.smashingmagazine.com"

Options:
  -r, --resolution TEXT  Разрешение экрана  [required]
  -m, --my TEXT          Месяц и год  [required]
  --help                 Show this message and exit. 
```
 Например, чтобы скачать все изображения в разрешении 1920x1080 за май 2019 года:
 ```
 $ python main.py --resolution 1920x1080 --my 052019
 ```
