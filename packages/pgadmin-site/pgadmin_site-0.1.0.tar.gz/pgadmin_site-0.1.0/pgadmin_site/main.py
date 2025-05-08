"""
Основной модуль, содержащий функцию site для создания веб-интерфейса.
"""

import os
import logging
from typing import Optional

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, flash
from sqlalchemy import create_engine, MetaData, Table, Column, inspect, text, select
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy

# Настройка логирования
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def site(host: str, 
         port: int = 5432, 
         username: str = "postgres", 
         password: str = "", 
         database: str = "postgres", 
         web_port: int = 5000,
         debug: bool = False):
    """
    Создать и запустить локальный веб-сайт для работы с таблицами PostgreSQL.
    
    Args:
        host: Хост PostgreSQL сервера
        port: Порт PostgreSQL сервера
        username: Имя пользователя PostgreSQL
        password: Пароль PostgreSQL
        database: Имя базы данных PostgreSQL
        web_port: Порт для веб-интерфейса
        debug: Включить режим отладки
    """
    # Создаем Flask приложение
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['DEBUG'] = debug
    
    # Настраиваем подключение к базе данных
    connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db = SQLAlchemy(app)
    
    # Создаем прямое подключение к базе данных через SQLAlchemy
    # вместо использования db.engine, которое требует контекст приложения
    engine = create_engine(connection_string)
    
    # Получаем метаданные базы данных
    metadata = MetaData()
    inspector = inspect(engine)

    @app.route('/')
    def index():
        """Главная страница со списком доступных таблиц"""
        try:
            # Получаем список таблиц из базы данных
            table_names = inspector.get_table_names()
            return render_template('index.html', tables=table_names, current_db=database)
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при подключении к базе данных: {str(e)}")
            return render_template('error.html', error=str(e))
    
    @app.route('/table/<table_name>')
    def view_table(table_name):
        """Показать содержимое таблицы"""
        try:
            # Проверяем, что таблица существует
            if table_name not in inspector.get_table_names():
                abort(404, f"Таблица {table_name} не найдена")
            
            # Получаем информацию о колонках
            columns = inspector.get_columns(table_name)
            column_names = [col['name'] for col in columns]
            
            # Получаем данные из таблицы
            with engine.connect() as connection:
                query = text(f'SELECT * FROM "{table_name}" LIMIT 100')
                result = connection.execute(query)
                # Получаем строки, обрабатываем в зависимости от версии SQLAlchemy
                try:
                    # SQLAlchemy 2.0+
                    rows = [row._asdict() for row in result]
                except AttributeError:
                    try:
                        # SQLAlchemy 1.4+
                        rows = [dict(row) for row in result]
                    except TypeError:
                        # Если данные уже в виде словарей
                        rows = list(result)
            
            # Получаем список всех таблиц для навигации
            all_tables = inspector.get_table_names()
            current_index = all_tables.index(table_name)
            prev_table = all_tables[current_index - 1] if current_index > 0 else None
            next_table = all_tables[current_index + 1] if current_index < len(all_tables) - 1 else None
            
            return render_template(
                'table.html', 
                table_name=table_name,
                columns=column_names,
                rows=rows,
                all_tables=all_tables,
                prev_table=prev_table,
                next_table=next_table
            )
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при работе с таблицей {table_name}: {str(e)}")
            return render_template('error.html', error=str(e))
    
    @app.route('/table/<table_name>/edit/<int:row_id>', methods=['GET', 'POST'])
    def edit_row(table_name, row_id):
        """Редактировать строку в таблице"""
        try:
            # Проверяем, что таблица существует
            if table_name not in inspector.get_table_names():
                abort(404, f"Таблица {table_name} не найдена")
            
            # Получаем информацию о колонках и первичном ключе
            columns = inspector.get_columns(table_name)
            pk_columns = inspector.get_pk_constraint(table_name)['constrained_columns']
            
            if not pk_columns:
                abort(400, f"Таблица {table_name} не имеет первичного ключа")
            
            primary_key = pk_columns[0]  # Используем первый столбец первичного ключа
            
            if request.method == 'POST':
                # Собираем данные из формы
                data = {col['name']: request.form.get(col['name']) for col in columns}
                
                # Формируем SQL запрос для обновления
                update_parts = [f'"{col}" = :{col}' for col in data.keys()]
                update_sql = f'UPDATE "{table_name}" SET {", ".join(update_parts)} WHERE "{primary_key}" = :row_id'
                
                # Выполняем запрос
                with engine.begin() as connection:
                    connection.execute(text(update_sql), {**data, 'row_id': row_id})
                
                flash('Запись успешно обновлена', 'success')
                return redirect(url_for('view_table', table_name=table_name))
            
            # Получаем текущие данные строки
            with engine.connect() as connection:
                query = text(f'SELECT * FROM "{table_name}" WHERE "{primary_key}" = :row_id')
                result = connection.execute(query, {'row_id': row_id})
                # Получаем строку, обрабатываем в зависимости от версии SQLAlchemy
                row_result = result.fetchone()
                try:
                    # SQLAlchemy 2.0+
                    row = row_result._asdict()
                except AttributeError:
                    try:
                        # SQLAlchemy 1.4+
                        row = dict(row_result)
                    except TypeError:
                        # Если данные уже в виде словаря
                        row = row_result
            
            return render_template('edit_row.html', table_name=table_name, row=row, columns=columns)
        
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при редактировании строки: {str(e)}")
            return render_template('error.html', error=str(e))
    
    @app.route('/table/<table_name>/add', methods=['GET', 'POST'])
    def add_row(table_name):
        """Добавить новую строку в таблицу"""
        try:
            # Проверяем, что таблица существует
            if table_name not in inspector.get_table_names():
                abort(404, f"Таблица {table_name} не найдена")
            
            # Получаем информацию о колонках
            columns = inspector.get_columns(table_name)
            
            if request.method == 'POST':
                # Собираем данные из формы
                data = {}
                for col in columns:
                    value = request.form.get(col['name'])
                    if value or not col.get('nullable', True):
                        data[col['name']] = value
                
                # Формируем SQL запрос для вставки
                columns_str = ', '.join([f'"{col}"' for col in data.keys()])
                values_str = ', '.join([f':{col}' for col in data.keys()])
                insert_sql = f'INSERT INTO "{table_name}" ({columns_str}) VALUES ({values_str})'
                
                # Выполняем запрос
                with engine.begin() as connection:
                    connection.execute(text(insert_sql), data)
                
                flash('Запись успешно добавлена', 'success')
                return redirect(url_for('view_table', table_name=table_name))
            
            return render_template('add_row.html', table_name=table_name, columns=columns)
        
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении строки: {str(e)}")
            return render_template('error.html', error=str(e))
    
    @app.route('/table/<table_name>/delete/<int:row_id>', methods=['POST'])
    def delete_row(table_name, row_id):
        """Удалить строку из таблицы"""
        try:
            # Проверяем, что таблица существует
            if table_name not in inspector.get_table_names():
                abort(404, f"Таблица {table_name} не найдена")
            
            # Получаем информацию о первичном ключе
            pk_columns = inspector.get_pk_constraint(table_name)['constrained_columns']
            
            if not pk_columns:
                abort(400, f"Таблица {table_name} не имеет первичного ключа")
            
            primary_key = pk_columns[0]
            
            # Выполняем запрос на удаление
            with engine.begin() as connection:
                delete_sql = f'DELETE FROM "{table_name}" WHERE "{primary_key}" = :row_id'
                connection.execute(text(delete_sql), {'row_id': row_id})
            
            flash('Запись успешно удалена', 'success')
            return redirect(url_for('view_table', table_name=table_name))
        
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении строки: {str(e)}")
            return render_template('error.html', error=str(e))
    
    @app.route('/table/<table_name>/structure')
    def table_structure(table_name):
        """Показать структуру таблицы"""
        try:
            # Проверяем, что таблица существует
            if table_name not in inspector.get_table_names():
                abort(404, f"Таблица {table_name} не найдена")
            
            # Получаем информацию о колонках
            columns = inspector.get_columns(table_name)
            
            # Получаем информацию о первичном ключе
            pk_constraint = inspector.get_pk_constraint(table_name)
            pk_columns = pk_constraint['constrained_columns'] if pk_constraint else []
            
            # Получаем информацию о внешних ключах
            foreign_keys = inspector.get_foreign_keys(table_name)
            
            # Получаем информацию об индексах
            indexes = inspector.get_indexes(table_name)
            
            return render_template(
                'structure.html',
                table_name=table_name,
                columns=columns,
                pk_columns=pk_columns,
                foreign_keys=foreign_keys,
                indexes=indexes
            )
        
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении структуры таблицы: {str(e)}")
            return render_template('error.html', error=str(e))
    
    @app.route('/table/<table_name>/add_column', methods=['GET', 'POST'])
    def add_column(table_name):
        """Добавить новый столбец в таблицу"""
        try:
            # Проверяем, что таблица существует
            if table_name not in inspector.get_table_names():
                abort(404, f"Таблица {table_name} не найдена")
            
            if request.method == 'POST':
                column_name = request.form.get('column_name')
                column_type = request.form.get('column_type')
                nullable = request.form.get('nullable') == 'on'
                default = request.form.get('default')
                
                # Формируем SQL запрос для добавления столбца
                nullable_str = "NULL" if nullable else "NOT NULL"
                default_str = f"DEFAULT {default}" if default else ""
                
                alter_sql = f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" {column_type} {nullable_str} {default_str}'
                
                # Выполняем запрос
                with engine.begin() as connection:
                    connection.execute(text(alter_sql))
                
                flash('Столбец успешно добавлен', 'success')
                return redirect(url_for('table_structure', table_name=table_name))
            
            return render_template('add_column.html', table_name=table_name)
        
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении столбца: {str(e)}")
            return render_template('error.html', error=str(e))
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Обработчик ошибки 404"""
        return render_template('error.html', error=error), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Обработчик ошибки 500"""
        return render_template('error.html', error=error), 500
    
    # Запускаем приложение
    logger.info(f"Запуск веб-сервера на порту {web_port}")
    logger.info(f"Подключение к базе данных: {connection_string.replace(password, '****')}")
    
    app.run(host="0.0.0.0", port=web_port, debug=debug)
    
    return app 