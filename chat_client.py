#coding:utf8
import cmd, socket, traceback, threading, time
import sys
class ChatClient(cmd.Cmd):
    ''' chat client '''
    def __init__(self, host='localhost', port=10001):
        cmd.Cmd.__init__(self)
        self.host = host
        self.port = port
        self.sock = ''
        self.prompt =  'chatClient>'
        self.completekey='\n'
        self.name = ''
        
    def do_connect(self, line):#连接到server
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((self.host, self.port))
        s.settimeout(0.1)#设置超时时间 0.1 秒
        print 'you are connected, and you can input your name, example: name Vincent'
        self.sock = s
   
    def do_name(self, line):
        if not self.sock:#先得连接才能执行。
            print 'please connect first'
        line = line.strip()
        self.prompt = '%s>' % line
        self.sock.send('name\t%s' % line)#发送名字
        self.name = line
        #print 'name', line
        t = threading.Thread(target=ChatClient.continue_read, args=(self,))#启动一个子线程、
        t.setDaemon(True)#守护线程在子线程没有执行完的时候程序不会被退出
        t.start()
	'''
		个人理解：
		setDaemon(True)将线程声明为守护线程，必须在start() 方法调用之前设置，如果不设置为守护线程程序会被无限挂起。
		The entire Python program exits when no alive non-daemon threads are left					
		上面这句话的意思是：当没有存活的非守护进程时，整个python程序才会退出。
		也就是说：如果主线程执行完以后,还有其他非守护线程,主线程是不会退出的
		，会被无限挂起；必须将线程声明为守护线程之后，如果队列中的数据运行完了，那么整个程序想什么时候退出就退出，不用等待。
		'''
        
    def do_msg(self, line):
        if not line:
            print 'input error, msg is empty, check it and reinput'
        if line:
            self.sock.send('msg\t%s' % line)
    
    def do_show(self, line):
        if not self.name:
            print 'please set your name first'
        self.sock.send('show\ttmp')#发送show 和tmp
        #print 'show'
        
    def do_pm(self, line):
        if not line:
            print 'input error, msg is empty, check it and reinput'
        if line:
            self.sock.send('pm\t%s' % line)
            
    @staticmethod#不用self  无法访问成员变量 且可以直接调用不用加参数
    def continue_read(chatclient):#接收返回的消息并且打印出来
        while 1:
            try:
                msg = chatclient.sock.recv(1024) #新建对象
                if msg:
                    print msg
                    sys.stdout.write(chatclient.prompt)
                    sys.stdout.flush()
                else:
                    break
            except socket.timeout:
                pass
            except:
                traceback.print_exc()
            time.sleep(1)
        print 'exit thread', threading.currentThread().getName()#查看当前的线程名称
       
    def do_EOF(self, line):#退出
        if self.sock:
            self.sock.close()
        return True
    
    
if __name__=='__main__':
    info='''
        help:
        1.connect         ---  连接到服务器
        2.name [vincent]  ---  用昵称登陆
        3.show            ---  查看当前连接人数
        4.msg [message]   ---  群发消息
        5.pm [vincent] [message]  --- 发送给某人
        '''
    print info
    ChatClient().cmdloop()
