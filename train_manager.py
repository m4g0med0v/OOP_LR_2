#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Написать программу, выполняющую следующие действия: ввод с клавиатуры данных в список,
# состоящий из словарей заданной структуры; записи должны быть упорядочены по номерам поездов;
# вывод на экран информации о поезде, номер которого введен с клавиатуры;
# если таких поездов нет, выдать на дисплей соответствующее сообщение.

import argparse
import os
import sqlite3
from pathlib import Path


def connect_db(db_name):
    """Создание соединения с базой данных и создание таблиц."""
    if not Path("data/").exists():
        os.mkdir("data")

    conn = sqlite3.connect(f"data/{db_name}.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination TEXT NOT NULL,
            number TEXT NOT NULL UNIQUE,
            time TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_name TEXT NOT NULL,
            train_id INTEGER,
            FOREIGN KEY (train_id) REFERENCES trains(id)
        )
    """)

    conn.commit()
    return conn


def add_train(conn, destination, number, time, station_name):
    """Добавить новый поезд и связанную станцию в базу данных."""
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO trains (destination, number, time) VALUES (?, ?, ?)",
        (destination, number, time),
    )
    train_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO stations (station_name, train_id) VALUES (?, ?)",
        (station_name, train_id),
    )

    conn.commit()

    return find_train(conn, number)


def list_trains(conn):
    """Вывести все поезда и их станции."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT trains.number, trains.destination, trains.time, stations.station_name
        FROM trains
        LEFT JOIN stations ON trains.id = stations.train_id
    """)

    trains = cursor.fetchall()

    return trains


def find_train(conn, number):
    """Найти и вывести информацию о поезде по его номеру."""
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT trains.number, trains.destination, trains.time, stations.station_name
        FROM trains
        LEFT JOIN stations ON trains.id = stations.train_id
        WHERE trains.number = ?
    """,
        (number,),
    )

    train = cursor.fetchone()

    return train


def main():
    parser = argparse.ArgumentParser(description="Управление списком поездов")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Команды")

    add_parser = subparsers.add_parser("add", help="Добавить новый поезд")
    add_parser.add_argument(
        "-d", "--destination", required=True, help="Название пункта назначения"
    )
    add_parser.add_argument("-n", "--number", required=True, help="Номер поезда")
    add_parser.add_argument(
        "-t", "--time", required=True, help="Время отправления (чч:мм)"
    )
    add_parser.add_argument("-s", "--station", required=True, help="Название станции")

    subparsers.add_parser("list", help="Показать все поезда")

    find_parser = subparsers.add_parser("find", help="Найти поезд по номеру")
    find_parser.add_argument("number", help="Номер поезда для поиска")

    args = parser.parse_args()

    conn = connect_db("trains")

    if args.command == "add":
        ans = add_train(conn, args.destination, args.number, args.time, args.station)
        print(f"Поезд №{ans[0]} в {ans[1]} добавлен.")

    elif args.command == "list":
        ans = list_trains(conn)
        if ans:
            for train in ans:
                print(
                    f"Поезд №{train[0]} отправляется в {train[1]} в {train[2]}, станция: {train[3]}."
                )
        else:
            print("Нет данных о поездах.")

    elif args.command == "find":
        ans = find_train(conn, args.number)
        if ans:
            print(
                f"Поезд №{train[0]} отправляется в {train[1]} в {train[2]}, станция: {train[3]}."
            )
        else:
            print(f"Поезд с номером {args.number} не найден.")

    conn.close()


if __name__ == "__main__":
    main()
