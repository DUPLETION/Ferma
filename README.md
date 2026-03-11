# Программируемая ферма

Игра-симулятор фермы, в которой игрок управляет роботом с помощью Python-кода.

## Установка на Android через GitHub

### Шаг 1: Создайте репозиторий на GitHub

1. Зайдите на [github.com](https://github.com)
2. Нажмите **New repository**
3. Назовите репозиторий `farmbot`
4. Выберите **Public**
5. Нажмите **Create repository**

### Шаг 2: Загрузите код

В терминале выполните:

```bash
cd D:\FERMA
git init
git add .
git commit -m "Initial commit"
```

Затем добавьте удалённый репозиторий:

```bash
git remote add origin https://github.com/YOUR_USERNAME/farmbot.git
git push -u origin main
```

Замените `YOUR_USERNAME` на ваше имя пользователя GitHub.

### Шаг 3: Запустите сборку

1. Откройте репозиторий на github.com
2. Перейдите на вкладку **Actions**
3. Нажмите **Build Android APK** слева
4. Нажмите кнопку **Run workflow** (зеленая)
5. Дождитесь завершения сборки (5-15 минут)
6. Скачайте APK из раздела **Artifacts**

### Шаг 4: Установите на телефон

1. Скачайте файл `farmbot-debug.apk` на телефон
2. Разрешите установку из неизвестных источников
3. Установите приложение

## Как играть

1. Напишите Python-код в редакторе
2. Нажмите **Запустить код**
3. Робот будет выполнять ваш код каждый тик (0.2 сек)

### Доступные команды

```python
move_up()      # Вверх
move_down()    # Вниз
move_left()    # Влево
move_right()   # Вправо
plant("wheat") # Посадить пшеницу
harvest()      # Собрать урожай
water()        # Полить растение
is_empty()     # Проверить, пустая ли клетка
is_plant()     # Есть ли растение
can_harvest()  # Готов ли урожай
scan()         # Сканировать соседние клетки
get_position() # Получить позицию робота
get_inventory() # Получить инвентарь
print("текст") # Вывод в консоль
```

### Пример кода

```python
while True:
    if can_harvest():
        harvest()
    else:
        move_right()
```

## Требования

- Python 3.8+
- Kivy 2.1+
