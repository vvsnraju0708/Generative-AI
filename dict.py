import keyboard

my_dict = {}

Key = ''
value = ''
flag = True  
# my_dict[Key] = value
def prress(event):
    global flag
    if event.name == 'k':
        flag = False
        print(my_dict)
    if event.name == 'c':
        print('working')
        flag = False   
        
     
while flag:
    key = input()
    value = input()

    my_dict[key] = value
    
    if keyboard.is_pressed("c"):
        break
    
keyboard.on_press(prress)


# keyboard.on_press(prress)

keyboard.wait('esc')