from old_version.ui.button import Button
from old_version.ui.view import View


class ControllView(View):
    def __init__(self, name, width=300, height=300):
        super().__init__(name, width, height)
        self.button_on = Button(self,0,0,100,36,"ON")
        self.button_pasta = Button(self,120,0,100,36,"PASTA")

    def additional_ui(self, state,line_pos,mouse):
        self.button_on.y =line_pos
        self.button_pasta.y =line_pos
        line_pos+= 30
        
        self.button_on.hovered = self.button_on.inside(mouse[0],mouse[1])
        self.button_on.draw()

        self.button_pasta.hovered = self.button_pasta.inside(mouse[0],mouse[1])
        self.button_pasta.draw()