Домашнее задание
Запуск автотестов с использованием Jenkins

Цель:
Научиться поднимать Jenkins и выполнять базовую конфигурацию джоб

Поднять Jenkins любым способом (docker, jar ...)
Настроить джобу которая будет запускать ваши автотесты на opencart
1. Джоба должна подтягивать данные из githuib
2. Джоба должна генерировать отчёт allure
3. Джоба должна принимать в качестве параметров:
Адрес executor (selenoid, browserstack, ip)
Адрес приложения opencart
Количество потоков
Браузер
Версию браузера
2.4 Желательно запускать тесты в docker (опционально)

Критерии оценки:
Автотесты запускаются через Jenkins.
Отчётность генерируется по результатам прогона
