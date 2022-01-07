#!/usr/local/bin/python3
# -*- coding: utf-8 -*-  
""" 
Created on Wed Jun 28 00:33:41 2017 
 
@author: dc 
"""  
  
  
import numpy as np  
import curses  
from random import randrange, choice  
from collections import defaultdict  
  
# 建立输入-动作映射表  
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']  
  
letter_codes = [ord(ch) for ch in 'WASDRQwasdrq' ]  
  
actions_dict = dict(zip(letter_codes,actions * 2))  
  
def invert(qipan):  
      
    return [row[::-1] for row in qipan]  
  
def tran(qipan):  
      
    return list(np.array(qipan).T)  
  
class GameField(object):  
      
    def __init__(self, height = 4, width = 4, win_value = 2048):  
          
        self.height = height  
          
        self.width = width  
          
        self.score = 0  
          
        self.highscore = 0  
          
        self.win_value = win_value  
          
        self.win = 0  
          
        self.gameover = 0  
          
        self.field = [[0 for i in range(self.height) ] for j in range(self.width)]   
          
    def spawn(self):  
          
        new_element = 4 if randrange(100) > 89 else 2  
          
        (ii,jj) = choice([(i,j) for i in range(self.height) for j in range(self.width) if self.field[i][j] == 0])  
          
        self.field[ii][jj] = new_element  
      
    def get_field(self):  
          
        #计算得到随机产生的初始状态下的field  
        self.field = [[0 for i in range(self.width) ] for j in range(self.height)]  
          
        num1 = 4 if randrange(1,100) > 89 else 2  
          
        num2 = 2 if num1 == 4 else 4                     
          
        (i1, j1) = choice([(i, j) for i in range(self.height) for j in range(self.width) if self.field[i][j]==0])  
          
        (i2, j2) = choice([(i, j) for i in range(self.height) for j in range(self.width) if self.field[i][j]==0])  
          
        self.field[i1][j1] = num1  
               
        self.field[i2][j2] = num2  
  
          
    def draw(self, screen):  
           
        help_string1 = 'W(up) S(down) A(left) D(right)'  
        help_string2 = '      R(restart) Q(exit)'  
        gameover_string = '       GAME OVER'  
        win_string = '         You Win'  
           
        def draw_line():  
               
            line = '+' + ('+------' * self.width + '+')[1:]   
              
            separator = defaultdict(lambda : line)  
              
            if not hasattr(draw_line, "counter"):  
                  
                draw_line.counter = 0  
                  
            screen.addstr(separator[draw_line.counter] + '\n')  
              
            draw_line.counter += 1  
  
            #screen.addstr('+' + "------+" * 4 + '\n')  
           
        def draw_nums(row_num):  
               
            #给定一行（默认4个）数字，如[0， 0， 0， 4]，以列表存放，该函数将其画在screen上  
            screen.addstr(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row_num) + '|'  + '\n')  
                  
        #开始draw  
        screen.clear()  
          
        screen.addstr('SCORE: 0' +  '\n')  
          
        for row in self.field:  
              
            draw_line()  
  
            draw_nums(row)  
          
        draw_line()  
          
        if self.win ==1:  
              
            screen.addstr(win_string + '\n')  
          
        elif self.gameover == 1:  
              
            screen.addstr(gameover_string + '\n')  
              
        else:  
              
            screen.addstr(help_string1 +  '\n')  
          
        screen.addstr(help_string2 +  '\n')  
          
        return True  
                  
      
    def get_action(self, keyboard):  
          
        char = 'N'  
          
        while char not in actions_dict:  
              
            char = keyboard.getch()  
              
        return actions_dict[char]  
      
    def is_move_possible(self, move):  
          
        def left_row_move_possible(row):  
              
            def point_changeable(i):  
                  
                if i+1<len(row) and row[i] == row[i+1]:  
                      
                    return True  
                  
                if row[i] == 0:  
                      
                    return True  
                  
                else:  
                  
                    return False  
              
            return any([point_changeable(i) for i in range(len(row))])  
          
        Changeable_dict = {}  
          
        Changeable_dict['Left'] = lambda field : any([left_row_move_possible(row) for row in field])  
          
        Changeable_dict['Right'] = lambda field : Changeable_dict['Left'](invert(field))  
                  
        Changeable_dict['Up'] = lambda field: Changeable_dict['Left'](tran(field))  
  
        Changeable_dict['Down'] = lambda field : Changeable_dict['Up'](invert(field))  
          
        if move in Changeable_dict:  
              
            return Changeable_dict[move](self.field)  
          
          
        return False  
      
    def move(self, direction):  
          
        def left_row_move(row):  
              
            def squeeze(row):  
                  
                newrow = [i for i in row if i !=0]  
                  
                newrow += [0 for i in row if i == 0]  
                  
                return newrow  
                  
            def merge(row):  
                  
                pair = False  
                  
                newrow = []  
                  
                for i in range(len(row)):  
                      
                    if pair == True:  
                          
                        newrow.append(row[i] *2)  
                      
                        pair = False  
                      
                    else:  
                          
                        if i+1 < len(row) and row[i] == row[i+1]:  
                              
                            pair = True  
                              
                            newrow.append(0)  
                          
                        else:  
                              
                            newrow.append(row[i])  
                  
                assert len(newrow) == len(row)  
                  
                return newrow  
              
            return squeeze(merge(squeeze(row)))  
          
        #建立操作为key，对应函数输出为值的字典  
        moves = {}  
          
        moves['Left'] = lambda field : [left_row_move(row) for row in field]  
          
        moves['Right'] = lambda field : invert(moves['Left'](invert(field)))  
          
        moves['Up'] = lambda field : tran(moves['Left'](tran(field)))  
          
        moves['Down'] = lambda field : invert(moves['Up'](invert(field)))  
          
        if direction in moves:  
              
            if self.is_move_possible(direction):  
                  
                self.field = moves[direction](self.field)  
                  
                #操作完后要加入新的两个随机的2或4？  
                try:  
                    self.spawn()  
                    self.spawn()  
                  
                except IndexError:  
                      
                    return False  
                      
                return True  
              
            else:  
                  
                return False  
          
        return False  
          
              
    def is_win(self):  
          
        return any(any(num >= self.win_value for num in row) for row in self.field)  
  
    def is_lose(self):  
          
        return not any(self.is_move_possible(move) for move in actions)  
      
                         
def main(screen):  
      
    def init():  
          
        field.get_field()  
          
        #field.draw(screen)  
      
        return "Game"           
      
    #注意在main函数中实例化一个field之后，main函数中再定义的函数就可以用field这个变量了。  
    def not_game(state):  
          
        if state == 'Win':  
              
            field.win = 1  
              
        if state == 'Gameover':  
          
            field.gameover = 1  
          
        #else:  
            #视作游戏崩溃，crash  
            #field.gameover = 1  
              
        field.draw(screen)  
          
        notgame_action = field.get_action(screen)  
          
        responses = defaultdict(lambda: state)  
          
        responses['Restart'], responses['Exit'] = 'Init', 'Exit'  
          
        return responses[notgame_action]  
  
    def game():  
          
        field.draw(screen)  
          
        game_action = field.get_action(screen)  
          
        #每一次game()处理先获取操作并根据操作来执行  
        if  game_action == 'Restart':  
              
            return 'Init'  
              
        if game_action == 'Exit':  
              
            return 'Exit'  
              
        if field.move(game_action):  
              
            if field.is_win():  
                  
                return 'Win'  
                  
            if field.is_lose():  
                  
                return 'Gameover'  
        else:  
              
            if field.is_lose():  
                  
                return 'Gameover'  
                  
        return 'Game'  
      
  
    #main()函数开始：  
      
    field = GameField()  
      
    # 建立状态-操作字典  
    state_actions = {  
        'Init' : init,  
        'Win' : lambda: not_game('Win'),  
        'Gameover': lambda: not_game('Gameover'),  
        'Game': game                              
        }  
  
    state = 'Init'  
      
    curses.use_default_colors()  
      
      
    while(state != 'Exit'):  
          
        state = state_actions[state]()  
      
  
curses.wrapper(main)           

