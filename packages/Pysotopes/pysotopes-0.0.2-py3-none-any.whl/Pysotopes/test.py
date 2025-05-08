from pysotopes import app, stylebook,island_frame

styles = stylebook()

myApp = app(app_name = "my app", app_size = "400x400", style_book = styles)
widget = myApp.widgets()

@myApp.island
def mainApp():
    return [
        title()({"relx": 0.5, "rely" :  0.5, "anchor" :"center"})
    ]

def get_elements():
    target_text = widget.get_named_widgets("Grah")
    target_button = widget.get_named_widgets("myBtn")
    target_input = widget.get_named_widgets("inputt")

    print(target_text, target_button, target_input)
    print("AH")


my_frame = island_frame(myApp, {"height" : 300, "width" : 300, "bg" : "red"})

@my_frame.island_frame
def title():
    return [
        widget.text({"text" : "hi", "iden" :"Grah"}, {"x" : 200, "y": 200}),
        widget.button({"text" : "OH HI", "iden" : "myBtn", "command" : get_elements}, {"x" : 200, "y": 250}),
        widget.inputText({"iden" : "inputt"}, {"x" : 200, "y": 300})
    ]

mainApp()

myApp.wrapUp()
