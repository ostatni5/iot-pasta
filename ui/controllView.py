from ui.button import Button
from ui.view import View


class ControllView(View):
    def __init__(self, name, width=300, height=300):
        super(ControllView, self).__init__(name, width, height)
        self.button_on = Button(self,0,0,100,36,"ON")

    def additional_ui(self, state,line_pos,mouse):
        self.button_on.y =line_pos
        line_pos+= 30
        self.button_on.hovered = self.button_on.inside(mouse[0],mouse[1])
        self.button_on.draw()