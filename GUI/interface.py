import PySimpleGUI as sg

unit = 10

layout = [
    [sg.Text(" "*unit*12+'.',text_color='white'), sg.Image(filename='bhge.png', data=None, background_color=None, size=(None, None), pad=None, key=None,
              tooltip=None, right_click_menu=None, visible=True, enable_events=False)],

    [sg.Text('Daleela', size=(6*unit, 1), font=("Helvetica", int( 2.5 * unit)), text_color='green')],
    [sg.Text('Baker Hughes voice assistant', size=(6 * unit, 1), font=("Helvetica", int(1.5 * unit)))],

    [sg.Text('background', size=(6 * unit, 1), font=("Helvetica", int(5 * unit)), text_color='white')],
    [sg.Button('Listen', button_color=('black', 'white'),size=(unit*2,int(unit/2) ))],

    [sg.InputText()],
    [sg.Text('Choose Source and Destination Folders', size=(35, 1))]
]

event, values  = sg.Window('Baker Hughes', layout, auto_size_text=True, default_element_size=(10, 1),size=(600,600)).Read()