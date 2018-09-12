# USML test task

Для нахождения минимального пути по всем точкам графа использовался метод поиска ближайших соседий.
Изначально матрица расстояний анализируется и если находятся ребра, которые выгоднее обойти, то они помечаются как разрыв.
Данный подход использовался в том случае, если матрица расстояний симметричная, в противном случае поиск возможного пути осуществляется начиная с каждого соседа.

