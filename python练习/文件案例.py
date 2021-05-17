#1、用户输入目标文件
old_name=input('请输入您要备份的文件名：')
print(old_name)
print(type(old_name))
#2、规划备份文件的名字
index=old_name.rfind('.')
print(index)
print(old_name[:index])
print(old_name[index:])
new_name=old_name[:index]+'[备份]'+old_name[index:]
print(new_name)
#3、备份文件写入名字（数据和原文件一致）
old_f=open(old_name,'r',encoding='UTF-8')
new_f=open(new_name,'w',encoding='UTF-8')
while True:
    con=old_f.read(1024)
    if len(con)==0:
        break
    new_f.write(con)
old_f.close()
new_f.close()
