#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Для индивидуального задания лабораторной работы добавьте тесты с использованием
# модуля unittest, проверяющие операции по работе с базой данных.


import os
import sys
import unittest

from src.train_manager import add_train, connect_db, find_train, list_trains


class TestDatabaseOperations(unittest.TestCase):
    def setUp(self):
        """Создание временной базы данных в памяти перед каждым тестом."""
        self.conn = connect_db("test_trains")

    def tearDown(self):
        """Закрытие соединения с базой данных после каждого теста."""
        self.conn.close()
        os.remove("data/test_trains.db")

    def test_add_train(self):
        """Проверка добавления поезда и станции."""
        add_train(self.conn, "Москва", "001A", "12:00", "Казань")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM trains WHERE number = '001A'")
        train = cursor.fetchone()

        self.assertIsNotNone(train)
        self.assertEqual(train[1], "Москва")
        self.assertEqual(train[2], "001A")
        self.assertEqual(train[3], "12:00")

        cursor.execute("SELECT * FROM stations WHERE train_id = ?", (train[0],))
        station = cursor.fetchone()

        self.assertIsNotNone(station)
        self.assertEqual(station[1], "Казань")

    def test_find_train(self):
        """Проверка поиска поезда по номеру."""
        add_train(self.conn, "Москва", "002B", "14:00", "Казань")

        self.assertTupleEqual(
            find_train(self.conn, "002B"), ("002B", "Москва", "14:00", "Казань")
        )

    def test_list_trains(self):
        """Проверка отображения списка поездов."""
        add_train(self.conn, "Москва", "003C", "15:00", "Казань")
        add_train(self.conn, "Санкт-Петербург", "004D", "16:00", "Тверь")

        train_list = list_trains(self.conn)
        self.assertTupleEqual(
            ("003C", "Москва", "15:00", "Казань"),
            train_list[0],
        )
        self.assertTupleEqual(
            ("004D", "Санкт-Петербург", "16:00", "Тверь"),
            train_list[1],
        )

    def test_find_nonexistent_train(self):
        """Проверка поиска несуществующего поезда.\n"""
        self.assertIsNone(find_train(self.conn, "999Z"))


if __name__ == "__main__":
    unittest.main()
