Интерполирование многочленами
=============================
_Задание к лабораторной работе:_
* Составить программу для построения интерполяционного многочлена Лагранжа (Ньютона). Программа должна работать в двух режимах:
  1. по заданной таблице значений функции определять приближенное значение функции в некоторой точке, вводимой пользователем;
  2. по заданной аналитически функции y = f(x) и массиву значений аргумента (массив читается из файла) вычислить таблицу значений функции. Используя полученную таблицу, построить интерполяционный многочлен после чего нарисовать графики функции y = f(x) и интерполяционного многочлена.
* Исследовать путем проведения вычислительных экспериментов влияние количества и расположения узлов интерполирования, участков интерполирования на величину погрешности интерполирования. В качестве функций, для которых проводится анализ, помимо придуманных Вами функций рекомендуется рассмотреть `y = |x|` при `|x| ≤ 1`, `y = e^(-x^2)` при `|x| ≤ 4`, `y = sin x` при `|x| ≤ π`.
