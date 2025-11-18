import random

desk = [None] * 9 # игровая доска
ai_level = 0 # уровень расчета ai

# показ доски
def view_desk():
    print("  0 1 2")
    str_desk = list("-" if x is None else ("X","0")[x] for x in desk)
    for i in range(0,3):
        print(str(i) + " " + " ".join(str_desk[i*3:i*3+3]))

# проверка позиции на победу
def test_win (_gamer:int)->bool:
    global desk
    line = [_gamer, _gamer, _gamer]
    return ( any(desk[i::3] == line for i in range(3)) # столбцы
        or any(desk[i*3:i*3+3] == line for i in range(3)) # строки
        or desk[0::4] == line #диагонали
        or desk[2:7:2] == line )

# шаг игрока
def do_step ( cell:int, _gamer:int)->bool:
    global desk
    if cell > 8 or desk[ cell ] is not None: return False #проверка на корректность хода
    desk[ cell ] = _gamer
    return True

# расчет веса хода для ai
def calc_weight( _gamer:int)->int:
    global ai_level
    global desk

    result = 0
    ai_level += 1

    for i in range(9):
        if desk[ i ] is not None: continue
        desk[ i ] = _gamer
        if test_win(_gamer):
            if _gamer == gamer_h:
                result += -1 # выигрыш человека учитывается но не стопорит ветку
            else:
                result = 1 # выигрышь ai стопорит ветку
                desk[i] = None
                break
        else:
            result += calc_weight( int( not _gamer )) # ветка
        desk[i] = None
    result = round(result / (ai_level * 3),4) # индекс ослабления учета результатов уровня , подобрал
    ai_level -= 1
    return result

#расчет шага ai
def ai_step ():
    global desk

    # словарь по пустым клеткам
    result = {key: 0 for key in range(9) if desk[key] is None}
    print(f"Ход Ai ({ ("X","0")[gamer_ai] })")

    for i in result.keys(): # перебор пустых клеток и расчет веток из них
        desk[i] = gamer_ai # тестовый ход
        if test_win(gamer_ai): # если на первом уровне есть победа ее и возращаем
            desk[i] = None
            return i
        result[i] = calc_weight(gamer_h) # расчет ветки
        desk[i] = None # возвращаем клетку в исходное

    max_value = max( result.values()) # ищем максимальный коэф
    f_result = list(k for k, v in result.items() if v == max_value) # выбираем всех с максимумом

    return f_result[random.randint(0,len(f_result)-1)] # выбираем случайную из равных

#ход человека
def h_step():
    i_step = input( f"Ваш ход ({ ("X","0")[gamer_h] }):" )
    return int( i_step[0] ) * 3 + int( i_step[1] )

def view():
    print("  0 1 2")
    str_desk = list("-" if x == None else ("X","0")[x] for x in desk)
    for i in range(0,3):
        print(str(i) + " " + " ".join(str_desk[i*3:i*3+3]))

gamer_h = random.randint(0, 1)
gamer_ai = int(not gamer_h)

print("Игра КРЕСТИКИ-НОЛИКИ")
print("====================================")
print(f" Ходы вводить в формате номер строки\n"
    f"затем номер столбца без разделителей\n")

curr_gamer = 0
view()

while True:
    print(f"===================")

    cell = h_step() if curr_gamer == gamer_h else ai_step()

    if not do_step(cell,curr_gamer):
        print("Неверный ход, попробуйте снова")
        continue

    view()
    if test_win(curr_gamer):
        print("\n*********************")
        if curr_gamer == gamer_h:
            print("   Вы победили")
        else:
            print("   Победил Ai")
        print("*********************")
        break

    if not None in desk:
        print("\nИгра закончена, вся клетки заполнены")
        break

    curr_gamer = int(not curr_gamer)
