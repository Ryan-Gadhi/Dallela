import PySimpleGUI as sg

unit = 10


qt = sg.Text('qt')
layout = [

    # adds BHGE Image, and white space to push the image to the right
    [sg.Text(" "*unit*12+'.',text_color='white'), sg.Image(filename='bhge.png', data=None, background_color=None, size=(None, None), pad=None, key=None,
              tooltip=None, right_click_menu=None, visible=True, enable_events=False)],

    # adds Daleela word
    [sg.Text('Daleela', size=(6*unit, 1), font=("Helvetica", int( 2.5 * unit)), text_color='green')],

    # adds comments after Daleela
    [sg.Text('Baker Hughes voice assistant', size=(6 * unit, 1), font=("Helvetica", int(1.5 * unit)))],

    # adds white text to push the image down
    [sg.Text('background', size=(6 * unit, 1), font=("Helvetica", int(5 * unit)), text_color='white')],

    # the listen button
    [sg.Button(button_text='Listen', button_color=('black', 'white'),size=(unit*2,int(unit/2) ))],

    # daleela sound should be diplayed here
    [sg.Text('hh', size=(6 * unit, 1), font=("Helvetica", int(1.5 * unit)))]


]

event, values  = sg.Window('Baker Hughes', layout, auto_size_text=True, background_color='white',default_element_size=(10, 1),size=(600,600)).Read()

print(values)