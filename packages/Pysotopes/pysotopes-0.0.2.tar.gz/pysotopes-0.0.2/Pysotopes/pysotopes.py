import tkinter


class app():
    def __init__(self, app_name: str, app_size: str, style_book) -> None:
        self.app = tkinter.Tk()

        if app_name:
            self.app.title(app_name)
        if app_size: 
            self.app.geometry(app_size)

        self.style_book = style_book

        self.widgetsLib = app_widgets(self.app, self.style_book)

        self.components = {}
        

    def wrapUp(self):
        self.app.mainloop()

    def widgets(self):
        return self.widgetsLib
    
    def get_style_book(self) -> object:
        return self.style_book
    
    def get_raw_app(self):
        return self.app
    
    def island(self, appWidget):
        def pack_to_main():
            widgets_to_pack = appWidget() #returns a list of tuples which include a tkinter widget and a placing method
            for widgetTuple in widgets_to_pack: #get the list and iterating over the func
                widgetComponent, placing_method = widgetTuple
                #the function provided returns one of appWidget (class)'s method
                #and the method of appWidget's class returns the tkinter widget and placing properties
                widgetComponent.place(placing_method)
        return pack_to_main
    
    
class island_frame():
    def __init__(self, mainApp: app, properties: dict):
        self.frame = tkinter.Frame(mainApp.get_raw_app(), properties)
        self.stylebook = mainApp.get_style_book()
        self.widgetsLib = app_widgets(self.frame, self.stylebook)

    def island_frame(self, appWidget):
        def pack_to_island_part():
            widgets_to_pack = appWidget()
            for widget_tuple in widgets_to_pack:
                widget_component, placing_method = widget_tuple
                widget_component.place(placing_method)
            return self.get_frame
        return pack_to_island_part
    
    def get_frame(self, packing_properties):
        return self.frame, packing_properties
    
    def get_raw_frame(self):
        return self.frame

        

class app_widgets():
    def __init__(self, parent, style_book):
        self.parent = parent
        self.style_book = style_book
        self.named_widget_lib = {}

    def text(self, properties: dict, packing_properties: dict):
        add_to_named_list = False
        try:
            if properties.get("style"):
                style = self.style_book.get_all_style()[properties["style"]]
                properties.pop("style")
                properties = properties | style
            elif properties.get("iden"):
                key = properties["iden"]
                properties.pop("iden")
                add_to_named_list = True
        except KeyError:
            pass

        print(add_to_named_list)

        returning_text = tkinter.Label(self.parent, properties), packing_properties

        if add_to_named_list:
            self.named_widget_lib[key] = returning_text[0]
            
        return returning_text

    def button(self, properties, packing_properties):
        add_to_named_list = False
        try:
            if properties.get("style"):
                style = self.style_book.get_all_style()[properties["style"]]
                properties.pop("style")
                properties = properties | style
            elif properties.get("iden"):
                key = properties["iden"]
                properties.pop("iden")
                add_to_named_list = True
        except KeyError:
            pass

        returning_button = tkinter.Button(self.parent, properties), packing_properties
        
        if add_to_named_list:
            self.named_widget_lib[key] = returning_button[0]
            

        return returning_button
    
    def inputText(self, properties: dict, packing_properties: dict):
        add_to_named_list = False
        try:
            if properties.get("style"):
                style = self.style_book.get_all_style()[properties["style"]]
                properties.pop("style")
                properties = properties | style
            elif properties.get("iden"):
                key = properties["iden"]
                properties.pop("iden")
                add_to_named_list = True
        except KeyError:
            pass
        
        print(add_to_named_list)

        returning_entry = tkinter.Entry(self.parent, properties), packing_properties

        if add_to_named_list:
            self.named_widget_lib[key] = returning_entry[0]
            
        return returning_entry
    
    def get_named_widgets(self, key: str) -> tkinter.Widget | None:
        try:
            return self.named_widget_lib[key]
        except KeyError:
            return None


    
class stylebook():
    def __init__(self):
        self.styles = {}

    def add_to_style(self, style_name, style: dict):
        self.styles[style_name] = style
        return self

    def get_all_style(self) ->  dict:
        return self.styles


class atom():
    def __init__(self, data):
        self.data = data
        if type(data) == str:
            self.state = tkinter.StringVar(value = data)
            print("value ot data was str")
        elif type(data) == int:
            print("value ot data was int")
            self.state = tkinter.IntVar(value = data)

    def get(self):
        return self.data
    
    def set(self, new_data):
        self.state.set(new_data)

    def link_to_widget(self):
        return self.state

    def onChange(self, callback_func):
        self.state.trace_add("write", callback_func)

    def onRead(self, callback_func):
        self.state.trace_add("read", callback_func)

    def onDelete(self, callback_func):
        self.state.trace_add("unset", callback_func)

#TODO make the frame height and width changeable