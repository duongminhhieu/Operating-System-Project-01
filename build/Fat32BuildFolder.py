from fileHandler.Fat32File import *
import sys 
import os


class BuildFat32:
    def __init__(self, current_dir, fat32File):
        self.current_dir = current_dir
        #self.current_dir: AbstractDirectory = None 
        self.fat32File = fat32File
        self.dir_hist = []
    

    
    def generate_table_view(self):
        """
        Hàm để tạo ra một bảng thống kê tập tin
        """
        entry_info_list = []
        max_width = dict()

        def update_max_width(key, value):
            if key not in max_width:
                max_width[key] = len(str(value)) + 4
            elif max_width[key] < len(str(value)): 
                max_width[key] = len(str(value)) + 4

        for entry in self.current_dir.subentries:
            entry_info = {
                'name': entry.name, 
                'size': 0 if isinstance(entry, AbstractDirectory) else entry.size, 
                'attr': entry.describe_attr(),
                'sector': '' if len(entry.sectors) == 0 else entry.sectors[0]
            }
            if entry_info['name'] in ('.', '..'):
                continue
            
            entry_info_list.append(entry_info)

            update_max_width('name', entry_info['name'])
            update_max_width('attr', entry_info['attr'])
            update_max_width('sector', entry_info['sector'])

            if isinstance(entry, AbstractFile):
                update_max_width('size', entry.size)
            else:
                update_max_width('size', 5)
        
        format_str = '{0: <%d} {1: <%d} {2: <%d} {3: <%d}\n' % (
            max_width['name'], max_width['size'], max_width['attr'], max_width['sector'])

        print_str = ''
        print_str += format_str.format('name', 'size', 'attr', 'sector')
        for entry in entry_info_list:
            print_str += format_str.format(entry['name'], entry['size'], entry['attr'], entry['sector'])

        return print_str
    
    def list_entries(self):
        """
        Handler function for 'ls'
        """
        assert self.current_dir != None, 'An error occurred. Pointer to current directory is null'
        self.current_dir.build_tree()

        table = self.generate_table_view()
        print(table)
    
    def history_list(self):
        """
        Handler funciton for 'history list'
        """
        if len(self.dir_hist) == 0:
            print('History is empty')
            return 

        for entry in self.dir_hist:
            print(entry.name)

    def history_go_back(self):
        """
        Handler function for 'history pop'
        """
        if len(self.dir_hist) == 0:
            print('History is empty')
            return 

        last_entry = self.dir_hist[-1]
        self.dir_hist.pop()
        self.current_dir = last_entry

    def go_into_subdir(self, subdir_name):
        """
        Handler function for 'cd'
        """
        for entry in self.current_dir.subentries: 
            if entry.name == subdir_name:
                if isinstance(entry, AbstractFile):
                    print('Cannot cd into a file!')
                else:
                    self.dir_hist.append(self.current_dir)
                    self.current_dir = entry 
                    return
        print('Bad command or filename:', subdir_name)


    def show_help(self):
        print(  '--help:    in ra các lệnh hướng dẫn\n' +
                '--cd:      đi vào hoặc ra thư mục\n' +
                '--ls:      lấy các tập tin đang có trong thư mục\n' + 
                '--cls:     xóa màn hình\n' +
                '--root:    lấy cây thư mục\n' +
                '--cat:     đi vào file\n' + 
                '--detail:  lấy chi tiết một tập tin\n' +
                '--exit:    thoát khỏi file hoặc chương trình'
            )

    def show_tree(self):
        # TODO: implement tree command
        pass

    def dump_file(self, filename):
        for file in self.current_dir.subentries:
            if file.name == filename:
                binary_data: bytes = file.dump_binary_data()
                filename = os.path.join('extracted', filename)
                with open(filename, mode='wb') as out_file:
                    print('Dumping', file.size, 'bytes to', filename, '...')
                    out_file.write(binary_data)
                    print('Done.')
                return 
        raise FileNotFoundError('Bad filename: ' + filename)

    def read_text_file(self, filename):
        assert filename != None, 'Filename not specified.'

        for file in self.current_dir.subentries:
            if file.name == filename:
                binary_data: bytes = file.dump_binary_data()
                string_data = binary_data.decode('utf8')
                print('\n', string_data, '\n')
                return 
        raise FileNotFoundError('Bad filename: ' + filename)

    def start_shell(self):
        if self.current_dir == None: 
            return
        
        print('Type help for help.')
        while True: 
            try:
                user_inp = input('%s> ' % self.current_dir.name)

                # Parse command
                user_inp_lst = user_inp.split(' ', 1)
                if (len(user_inp_lst)) == 0:
                    return

                command_verb = user_inp_lst[0]
                if len(user_inp_lst) == 1:
                    command_arg = None 
                else: 
                    command_arg = user_inp_lst[1]
                
                # Process command
                if command_verb == 'help':
                    self.show_help()
                elif command_verb == 'cd':
                    self.go_into_subdir(command_arg)
                elif command_verb == 'ls':

                    self.list_entries()
                elif command_verb == 'dump':
                    self.dump_file(command_arg)
                elif command_verb == 'cat':
                    self.read_text_file(command_arg)
                elif command_verb == 'history':
                    if command_arg == 'list':
                        self.history_list()
                    elif command_arg == 'pop':
                        self.history_go_back()
                    else:
                        print('Action not supported. Type help for help.')
                elif command_verb == 'cd..':
                    self.history_go_back()
                elif command_verb == 'tree':
                    raise NotImplementedError('Command not implemented!')
                elif command_verb == 'exit':
                    return
                else: 
                    print('Bad command: %s. Type help for help.' % command_verb)
            except Exception as e:
                print('An error occurred:', e)
                    