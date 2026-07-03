### Миграции
в папке backend выполнить миграции
```commandline
alembic revision --autogenerate -m "Create tables"
```
```commandline
alembic upgrade head 
```

### Создать запись в бд для админа
после миграции бд в папке backend выполнить команду 
```commandline
python -m app.seed
```

### Запустить backend 
```commandline
uvicorn app.main:app --reload
```

##### (создает запись в бд с пользователь admin:admin)

### Запустить frontend
```
npm run dev
```




