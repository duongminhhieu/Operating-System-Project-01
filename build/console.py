'''
    cd: đi vào folder tiếp theo, có thể cd a b c
    cat: mở file
    cd: .. trở về folder trước đó
    cd: \ trở về root
    ls: in ra cây thư mục
    exit
'''
import os
from pattern.composite import *
from constant.command import *

class Console:
    def __init__(self, root:CItem):
        self.root:CItem = root
        self.rootName = root.name

        self.currentRoot = self.root
        self.currentRootPathPath = ''
        self.stack = [f'{root.name}:\\']
        self.stackTrigger = stack
        
        self.file = ['File:\\']
        self.fileTrigger = file
        
        self.currentStack = self.stack
        self.currentTrigger = self.stackTrigger

        self.isInFile = False
    def switch(self):
        if self.isInFile:
            self.currentStack = self.file
            self.currentTrigger = self.fileTrigger
        else:
            self.currentStack = self.stack
            self.currentTrigger = self.stackTrigger

    def setupRoot(self):
        currentRootPath = ''
        for stack in self.currentStack:
            currentRootPath += stack
        self.currentRootPath = currentRootPath
    def cd(self, expression:list[str]):
        if len(expression) == 0:
            return
        if expression[0] == '..' and len(self.currentStack) > 1:
            self.currentStack.pop()
            self.setupRoot()
            self.currentRoot = self.root.findByPath(self.currentRootPath[0:-1])
            return
        elif expression[0] == '\\':
            self.currentStack = [f'{self.rootName}:\\']
            self.currentRoot = self.root
            return
        elif len(expression[0].split('.')) > 1:
            return
        
        directory = self.currentRootPath
        folder:CItem = self.currentRoot
        for express in expression:
            directory += express
            folder:CItem = folder.findByPath(directory)
            if folder is None:
                return

        [self.currentStack.append(f'{express}\\') for express in expression]
        self.currentRoot = folder
    def cat(self, fileName):
        self.isInFile = True
        path = f'{self.currentRootPath}{fileName}'

        file:CFile = self.currentRoot.findByPath(path)
        if file is None:
            return
        self.currentRoot = file
        self.currentRoot.printContent()

        self.switch()

    def detail(self):
        self.currentRoot.printDetail()

    def ls(self):
        self.currentRoot.printCurrentItem()

    def exit(self):
        if self.isInFile is True:
            self.isInFile = False
            self.switch()
            self.setupRoot()

            self.currentRoot = self.root.findByPath(self.currentRootPath[0:-1])
        else:
            os.close()

    def _root(self):
        self.currentRoot.print()

    def help(self):
        print(  '--help:    in ra các lệnh hướng dẫn\n' +
                '--cd:      đi vào hoặc ra thư mục\n' +
                '--ls:      lấy các tập tin đang có trong thư mục\n' + 
                '--cls:     xóa màn hình\n' +
                '--root:    lấy cây thư mục\n' +
                '--cat:     đi vào file\n' + 
                '--detail:  lấy chi tiết một tập tin\n' +
                '--exit:    thoát khỏi file hoặc chương trình'
            )

    def trigger(self, command):
        if command not in self.currentTrigger:
            return False
        return True

    def cls(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def windowShell(self):
        running = True
        self.cls()
        self.help()
        print('\n')
        while running:
            self.setupRoot()

            expression = input(f'{self.currentRootPath[0:-1]}>')

            try:
                commands = expression.index('"')
                commands = expression.strip().split('"')
                commands.remove('')
            except ValueError:
                commands = expression.strip().split(' ')

            command = commands[0].strip()
            express = commands[1:]

            trigger = self.trigger(command)

            if trigger is False:
                continue
            
            if command == 'cd':
                self.cd(express)
            elif command == 'cat':
                self.cat(express[0])
            elif command == 'detail':
                self.detail()
            elif command == 'cls':
                self.cls()
            elif command == 'ls':
                self.ls()
            elif command == 'help':
                self.help()
            elif command == 'exit':
                self.exit()
            elif command == 'root':
                self._root()
            else:
                print(f'Command {command} was not support')

            # input('')

        


            


