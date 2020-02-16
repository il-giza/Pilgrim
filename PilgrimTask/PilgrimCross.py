class PilgrimCross():
    """Класс Перекресток. 
    Будем двигаться по перекресткам.
    
    Переменные класса отвечают за параметры города:
    min_x, max_x = 1, 5         - Размер города с запада на восток
    min_y, max_y = 1, 5         - Размер города с севера на юг 
    finish_cross = (5,5)        - Конечная точка пути 
    stop_cross = [(1,1), (2,1)] - Эти перекрестки уже пройдены и в силу правил города по ним уже нельзя двигаться. 
    
    Атрибуты класса:
    id = 0                - Пусть у объекта будет id, так легче будет отслеживать последовательность шагов 
    name = 'X'            - Имя объекта - сюда пишем направление света
    x, y = 3, 1           - Начальные координаты пути
    balance = -4          - Начальный баланс.  
    parent = False        - Ссылка на родителя (предыдущий перекресток)  
    street = (None, None) - Здесь название улицы, которая находится между перекрестками. Пишем в виде кортежа.
    free_step             - Массив названий доступных направлений движения
    next                  - Перекресток имеет свой генератор разрешенных направлений
    finish                - Состояние объекта. True - поломник дошел до конечной точки с балансом >= 0, иначе - False.
    """

    min_x, max_x = 1, 5
    min_y, max_y = 1, 5
    finish_cross = (5,5)
    stop_cross = [(1,1), (2,1)]
    
    def __init__(self, id = 0, name = 'X', x = 3, y = 1, balance = -4, parent = False, street = (None, None)):
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.balance = balance
        self.parent = parent
        self.street = street
        self.free_step = self.test_step()[1]        
        self.next = self.next_step()
        if (x,y) == self.finish_cross and self.balance >= 0:
            self.finish = True
        else:
            self.finish = False

    def test_street(self, street):
        """Проверяем, были ли данная улица уже пройдена поломником. Пробегаем по всем родительским объектам"""
        if self.street == street:
            return True
        if self.parent:
            return self.parent.test_street(street)
        else:
            return False
            
    def go_W(self):
        """Шаг на запад. Создание объекта на западе."""
        return PilgrimCross(self.id+1, 'W', self.x-1, self.y, self.balance + 2, self, street = (self.x-0.5, self.y))

    def go_E(self):
        """Шаг на восток. Создание объекта на востоке."""
        return PilgrimCross(self.id+1, 'E', self.x+1, self.y, self.balance - 2, self, street = (self.x+0.5, self.y))
        
    def go_N(self):
        """Шаг на север. Создание объекта на севере."""
        return PilgrimCross(self.id+1, 'N', self.x, self.y-1, self.balance / 2, self, street = (self.x, self.y-0.5))
        
    def go_S(self):
        """Шаг на юг. Создание объекта на юге."""
        return PilgrimCross(self.id+1, 'S', self.x, self.y+1, self.balance * 2, self, street = (self.x, self.y+0.5))

    def test_step(self):
        """Создаем картеж массивов функций и названий доступных вариантов шагов. Проверяем:
        1. граничное условие
        2. условие того, что по этой улице еще не проходили
        3. запретные перекрестки
        Возвращаем массив функций
        """
        free_step_func = []
        free_step_name = []
       
        if not(self.x == self.min_x or self.test_street((self.x-0.5, self.y)) or (self.x-1, self.y) in self.stop_cross):
            free_step_func.append(self.go_W)
            free_step_name.append('W')
        if not(self.x == self.max_x or self.test_street((self.x+0.5, self.y)) or (self.x+1, self.y) in self.stop_cross):
            free_step_func.append(self.go_E)
            free_step_name.append('E')
        if not(self.y == self.min_y or self.test_street((self.x, self.y-0.5)) or (self.x, self.y-1) in self.stop_cross):
            free_step_func.append(self.go_N)
            free_step_name.append('N')
        if not(self.y == self.max_y or self.test_street((self.x, self.y+0.5)) or (self.x, self.y+1) in self.stop_cross):
            free_step_func.append(self.go_S)
            free_step_name.append('S')
            
        return (free_step_func, free_step_name)
    
    def next_step(self):
        """На основе массива доступных вариантов шагов создаем генератор"""
        for i in self.test_step()[0]:
            yield i
    
    def get_next_cross(self):
        """Здесь возвращаем следующее значение генератора"""
        return self.next.__next__()()
    
    def show_path(self):
        """Возвращаем пройденный путь. Пробегаем всех родителей и пишем в массив"""
        path = []
        path.append((self.id, self.name, [self.x, self.y], self.street, self.balance))
        if self.parent:
            path += self.parent.show_path()
        return path
        
    def get_pid(self):
        """Возвращаем id родителя"""
        if self.parent:
            return self.parent.id
        else:
            return -1
    
    def show_info(self):
        """Покажем описание перекрестка"""
        print('id', self.id,
              ' pid', self.get_pid(),
              ' name:', self.name, 
              ' (x,y) =' , (self.x, self.y), 
              ' balance:', self.balance, 
              ' street:', self.street, 
              ' free_step:', self.free_step)
        
    def __call__(self):
        """Покажем описание перекрестка"""
        self.show_info()