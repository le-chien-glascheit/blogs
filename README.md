 Симулятор портала с блогами
Здесь вы можете почувствовать себя Павлом Дуровым и создать свою базу данных с Блэк Джековичами и Викторами Петровичами.
 
Все как и всегда, так как от реальности не сбежать, мы учим отаку любить наш мир! 

        
             Настройка

        
     
## Установка

### With _poetry_ ( с Поэзией)
```shell
pip install poetry
```
```shell
poetry shell
```
```shell
poetry install
```

### With _pip_ (с Пипом)

```shell
python -m venv .venv
```
```shell
.venv/scripts/activate
```
```shell
 pip install -r requirements.txt
```



            Установка зависимостей
            Настройка проекта





# Запуск
#### Для создания тестовой базы данных:
```shell
  python blogs\models.py
```
#### Для запуска сервера:
```shell
  uvicorn blogs.api:app 
```

# Ссылки на документации:

О том как пользоваться poetry вы найдете на [poetry docs](https://python-poetry.org/docs/plugins/#using-plugins)

О том как пользоваться pip вы найдете на [pip docs](https://pip.pypa.io/en/stable/user_guide/)

###### _Для_ _тех_ _кто_ _решит_ _покопаться_ _в_ _коде_ _будут_ _полезны_ _ссылки_:

О том как пользоваться api вы найдете на [api docs](https://docs.python.org/3/)

О том как пользоваться sqlalchemy вы найдете на [sqlalchemy docs](https://www.sqlalchemy.org/)

# Blogs