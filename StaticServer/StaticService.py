import os

os.system('python3 -m SimpleTornadoServer 8081')


'''
方法一：system调用

    #仅仅在一个子终端运行系统命令，而不能获取命令执行后的返回信息
    import os
    os.system('ls')

方法二：popen()函数

    import os
    os.popen('ls').readlines() #这个返回值是一个list

方法三.使用模块 subprocess

    import subprocess
    subprocess.call('ls') #可以直接call()调用


    #也可以使用subprocess.Popen
    p = subprocess.Popen('ls', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
    print(line)

'''
