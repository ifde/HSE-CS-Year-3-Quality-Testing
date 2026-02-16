# Ошибки в реализации VendingMachine

## Ошибка 1: Неверное возвращаемое значение в get_coins2()

### Код до исправления:
```python
def get_coins2(self):
    if self._mode == VendingMachine.Mode.OPERATION:
        return self._coins1  # BUG: должно быть return 0
    return self._coins2
```

### Данные, на которых наблюдается некорректное поведение:
```python
vm = VendingMachine()
vm.enter_admin_mode(117345294655382)
vm.fill_coins(25, 30)
vm.exit_admin_mode()
result = vm.get_coins2()
```

### Полученное значение: 25
### Ожидаемое значение: 0

### Описание проблемы:
В режиме OPERATION метод должен возвращать 0 для скрытия информации о наличии монет. Вместо этого метод неправильно возвращает `self._coins1`, что раскрывает конфиденциальную информацию о количестве монет номиналом 1.

### Код после исправления:
```python
def get_coins2(self):
    if self._mode == VendingMachine.Mode.OPERATION:
        return 0  # FIXED
    return self._coins2
```

---

## Ошибка 2: Неправильная логика проверки параметров в fill_coins()

### Код до исправления:
```python
def fill_coins(self, c1: int, c2: int):
    if self._mode == VendingMachine.Mode.OPERATION:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if c1 <= 0 or c2 > self._maxc1:  # BUG: проверяет c2 > self._maxc1
        return VendingMachine.Response.INVALID_PARAM
    if c1 <= 0 or c2 > self._maxc2:  # BUG: проверяет c1 <= 0
        return VendingMachine.Response.INVALID_PARAM
    self._coins1 = c1
    self._coins2 = c2
    return VendingMachine.Response.OK
```

### Данные, на которых наблюдается некорректное поведение:
```python
vm = VendingMachine()
vm.enter_admin_mode(117345294655382)
result = vm.fill_coins(60, 20)  # c1 = 60 превышает maxc1 = 50
```

### Полученное значение: OK (возвращает успех)
### Ожидаемое значение: INVALID_PARAM (должна быть ошибка)

### Описание проблемы:
Первое условие проверяет `c2 > self._maxc1` вместо `c1 > self._maxc1`, позволяя передать некорректное значение c1. Первая проверка также дублирует вторую строку.

### Код после исправления:
```python
def fill_coins(self, c1: int, c2: int):
    if self._mode == VendingMachine.Mode.OPERATION:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if c1 <= 0 or c1 > self._maxc1:  # FIXED: проверяет c1 > self._maxc1
        return VendingMachine.Response.INVALID_PARAM
    if c2 <= 0 or c2 > self._maxc2:  # FIXED: проверяет c2 > self._maxc2
        return VendingMachine.Response.INVALID_PARAM
    self._coins1 = c1
    self._coins2 = c2
    return VendingMachine.Response.OK
```

---

## Ошибка 3: Неверная реализация put_coin1()

### Код до исправления:
```python
def put_coin1(self):
    if self._mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self._coins2 == self._maxc2:  # BUG: проверяет coins2 вместо coins1
        return VendingMachine.Response.CANNOT_PERFORM
    self._balance += self._coinval2  # BUG: добавляет coinval2 вместо coinval1
    self._coins2 += 1  # BUG: увеличивает coins2 вместо coins1
    return VendingMachine.Response.OK
```

### Данные, на которых наблюдается некорректное поведение:
```python
vm = VendingMachine()
vm.enter_admin_mode(117345294655382)
vm.fill_coins(16, 1)
vm.exit_admin_mode()
vm.put_coin1()
balance = vm.get_current_balance()
```

### Полученное значение: 20 (баланс)
### Ожидаемое значение: 19 (баланс)

### Описание проблемы:
Метод `put_coin1()` должен добавлять монету номиналом 1, но вместо этого:
- Проверяет наличие места для монет номиналом 2
- Добавляет к балансу стоимость монеты номиналом 2 (2 единицы)
- Увеличивает счетчик монет номиналом 2 вместо 1

### Код после исправления:
```python
def put_coin1(self):
    if self._mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self._coins1 == self._maxc1:  # FIXED: проверяет coins1
        return VendingMachine.Response.CANNOT_PERFORM
    self._balance += self._coinval1  # FIXED: добавляет coinval1
    self._coins1 += 1  # FIXED: увеличивает coins1
    return VendingMachine.Response.OK
```

---

## Ошибка 4: Неверная реализация put_coin2()

### Код до исправления:
```python
def put_coin2(self):
    if self._mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self._coins1 == self._maxc1:  # BUG: проверяет coins1 вместо coins2
        return VendingMachine.Response.CANNOT_PERFORM
    self._balance += self._coinval1  # BUG: добавляет coinval1 вместо coinval2
    self._coins1 += 1  # BUG: увеличивает coins1 вместо coins2
    return VendingMachine.Response.OK
```

### Данные, на которых наблюдается некорректное поведение:
```python
vm = VendingMachine()
vm.enter_admin_mode(117345294655382)
vm.fill_coins(16, 1)  # coins1 = 10 (не максимум), coins2 = 30
vm.exit_admin_mode()
result = vm.put_coin2()
balance = vm.get_current_balance()
```

### Полученное значение: 19 (баланс)

### Ожидаемое значение: 20 (баланс)

### Описание проблемы:
Метод `put_coin2()` должен добавлять монету номиналом 2, но вместо этого:
- Проверяет наличие места для монет номиналом 1 (что неправильно)
- Добавляет к балансу стоимость монеты номиналом 1 (1 единица вместо 2)
- Увеличивает счетчик монет номиналом 1 вместо 2

### Код после исправления:
```python
def put_coin2(self):
    if self._mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self._coins2 == self._maxc2:  # FIXED: проверяет coins2
        return VendingMachine.Response.CANNOT_PERFORM
    self._balance += self._coinval2  # FIXED: добавляет coinval2
    self._coins2 += 1  # FIXED: увеличивает coins2
    return VendingMachine.Response.OK
```

---

## Ошибка 5: Использование необъявленной переменной в set_prices()

### Код до исправления:
```python
def set_prices(self, p: int):
    if self._mode == VendingMachine.Mode.OPERATION:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if _price <= 0:  # BUG: используется _price вместо p
        return VendingMachine.Response.INVALID_PARAM
    self._price = p
    return VendingMachine.Response.OK
```

### Данные, на которых наблюдается некорректное поведение:
```python
vm = VendingMachine()
vm.enter_admin_mode(117345294655382)
vm.set_prices(0)
```

### Полученное значение: NameError: name '_price' is not defined
### Ожидаемое значение: INVALID_PARAM

### Описание проблемы:
Метод использует неквалифицированное имя `_price` вместо `p`, что вызывает `NameError` при попытке проверить значение.

### Код после исправления:
```python
def set_prices(self, p: int):
    if self._mode == VendingMachine.Mode.OPERATION:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if p <= 0:  # FIXED: используется параметр p
        return VendingMachine.Response.INVALID_PARAM
    self._price = p
    return VendingMachine.Response.OK
```

---

## Ошибка 6: Неверный код ошибки в enter_admin_mode()

### Код до исправления:
```python
def enter_admin_mode(self, code: int):
    if self._balance != 0:
        return VendingMachine.Response.UNSUITABLE_CHANGE  # BUG: неверный код
    if code != self._id:
        return VendingMachine.Response.INVALID_PARAM
    self._mode = VendingMachine.Mode.ADMINISTERING
    return VendingMachine.Response.OK
```

### Данные, на которых наблюдается некорректное поведение:
```python
vm = VendingMachine()
vm.enter_admin_mode(117345294655382)
vm.fill_coins(8, 8)
vm.exit_admin_mode()
vm.put_coin1()
result = vm.enter_admin_mode(117345294655382)
```

### Полученное значение: UNSUITABLE_CHANGE
### Ожидаемое значение: CANNOT_PERFORM

### Описание проблемы:
Согласно спецификации, когда баланс пользователя не равен нулю, метод должен возвращать `CANNOT_PERFORM`, а не `UNSUITABLE_CHANGE`. Код `UNSUITABLE_CHANGE` предназначен для ситуаций с невозможностью выдачи сдачи требуемыми номиналами.

### Код после исправления:
```python
def enter_admin_mode(self, code: int):
    if self._balance != 0:
        return VendingMachine.Response.CANNOT_PERFORM  # FIXED
    if code != self._id:
        return VendingMachine.Response.INVALID_PARAM
    self._mode = VendingMachine.Mode.ADMINISTERING
    return VendingMachine.Response.OK
```

---

## Суммарный анализ

**Всего найдено ошибок: 6**

- **Критические ошибки (нарушают функциональность):** 4
  - put_coin1() - полностью неверная реализация
  - put_coin2() - полностью неверная реализация
  - get_coins2() - возвращает неверное значение
  - enter_admin_mode() - возвращает неверный код ошибки

- **Логические ошибки (могут привести к неопределенному поведению):** 2
  - fill_coins() - неправильная проверка границ
  - set_prices() - использование необъявленной переменной

Все эти ошибки должны быть исправлены для корректной работы торгового автомата согласно спецификации.
