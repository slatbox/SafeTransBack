import PySimpleGUI as sg
from client import Client
from protocal import Proto
import os
sg.theme('Dark Grey 13') 

class Frontend:
    def __init__(self) -> None:
        self.client = Client()
    def login(self):

        layout = [[sg.Text('用户名'),sg.Input()],
                  [sg.Text('密码 '),sg.Input()],
                  [sg.OK(), sg.Cancel()]]

        window = sg.Window('用户登录', layout)

        event, values = window.read()
        result = self.client.login(values[0],values[1])
        if result == False:
            sg.popup_error('用户名或密码错误')
        window.close()
        return result
    
    def util(self):
        # GUI布局
        files = self.client.getFileList().split(',')
        self.file_list = sg.Listbox(values=files,size=(50, 6))
        layout = [
            [sg.Text('安全文件传输客户端', font=('Helvetica', 10), size=(50, 1))],
            [self.file_list],
            [sg.Button('上传'), sg.Button('下载'),sg.Button('刷新')],
        ]
        # 创建GUI窗口
        window = sg.Window('简易安全传输客户端', layout)
        # 主循环
        while True:
            event, values = window.read()
            # print(values)
            # 关闭窗口
            if event == sg.WIN_CLOSED:
                window.close()
                break
            
            # 上传文件
            elif event == '上传':
                file_path=sg.popup_get_file('选择上传的文件',  title="上传文件")
                cmd_size = Proto.getCmdLen()
                file_size = os.path.getsize(file_path)
                orgin_file_size = file_size
                file_name = os.path.basename(file_path)
                cur_size = 0
                header,info = self.client.send(Proto.createReq(Proto.CMD_UPLOAD,file_name.encode()))
                with open(file_path,'rb') as f:
                    while True:
                        content = f.read(1024 - cmd_size)
                        state = Proto.CMD_FILE_SUCCESS if file_size > 1024 - cmd_size else Proto.CMD_UPLOAD_END
                        rep = Proto.createReq(state,content)
                        self.client.client.send(rep)
                        file_size -= len(content)
                        cur_size += len(content)
                        sg.one_line_progress_meter('上传进度',cur_size , orgin_file_size, file_name,'正在上传')
                        if file_size <= 0:
                            break
                sg.popup_notify('下载成功')
                event = 'null'

            # 下载文件
            elif event == '下载':
                file_name = values[0][0]
                state,data = self.client.download(file_name)
                file_len = int(data)
                cur_len = 0
                with open('download/'+file_name,'wb') as f:
                    while True:
                        state,data = self.client.recv()
                        f.write(data)
                        cur_len += len(data)
                        sg.one_line_progress_meter('下载进度',cur_len , file_len,file_name,'正在下载')
                        if state == Proto.STATE_END:
                            break
                sg.popup_notify('下载成功')
                event = 'null'
            elif event == '刷新':
                self.file_list.update(values=self.client.getFileList().split(','))
            else:
                event = 'null'
            
    
    
if __name__ == '__main__':
    front_end = Frontend()
    result = front_end.login()
    if result == True:
        front_end.util()
    