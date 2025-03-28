# Класс для получения случайного механика по очереди
class MechanicAssigner:
    def __init__(self):
        self.last_mechanic_index = 0

    async def get_next_mechanic(self, mechanics):
        result = self.last_mechanic_index % (len(mechanics)) + 1
        self.last_mechanic_index += 1
        print(result)
        return result

# Создаем экземпляр класса
mechanic_assigner = MechanicAssigner()
