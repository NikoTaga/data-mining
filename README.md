# - если не установлен пакет python3-venv, естанавливаем его:
    sudo apt-get install python3-venv

- создаем виртуальное окружение
    python3 -m venv ../venv

- запускаем виртуальное окружение
    source ../venv/bin/activate

- деактивация виртуального окружения
    deactivate 
    
## Установка зависимостей
    pip install -r requirements.txt