import pygame


class View:
    def __init__(self, name, width=300, height=300):
        self.name = name
        self.color_bg = (38, 70, 83)
        self.color_bg2 = (42, 157, 143)
        self.rock = (231, 111, 81)
        self.player = (233, 196, 106)
        self.font_size = 48
        self.small_font_size = 36
        self.font = pygame.font.SysFont(None, self.font_size)
        self.font_small = pygame.font.SysFont(None, self.small_font_size)
        self.screen = pygame.display.set_mode([width, height])
        self.padding_left = 10
        pygame.display.set_caption(name)

    def render(self, state={}, mouse =(0,0)):
        self.draw_ui(state, mouse)
        pygame.display.flip()

    def draw_ui(self, state, mouse):
        processing = state.get("processing", "---")
        status = state.get("status", "---")
        sensors = state.get("sensors", [["---", "---"]])
        progres = state.get("progres", "0%")
        self.screen.fill(self.color_bg)

        line_pos = self.padding_left

        self.print_text(self.name, self.color_bg2, self.padding_left, line_pos)
        line_pos += self.font_size

        self.print_text("Status:", self.color_bg2,
                        self.padding_left, line_pos, self.font_small)
        self.print_text(status, self.player, self.padding_left +
                        200, line_pos, self.font_small)
        line_pos += self.small_font_size

        self.print_text("Processed:", self.color_bg2,
                        self.padding_left, line_pos, self.font_small)
        self.print_text(progres, self.rock, self.padding_left +
                        200, line_pos, self.font_small)
        line_pos += self.small_font_size

        self.print_text(processing, self.rock, self.padding_left,
                        line_pos, self.font_small)
        line_pos += self.small_font_size + self.small_font_size/3

        self.print_text("Sensors:", self.color_bg2,
                        self.padding_left, line_pos, self.font_small)
        line_pos += self.small_font_size

        for sensor in sensors:
            self.print_text(sensor[0], self.color_bg2,
                            self.padding_left, line_pos, self.font_small)
            self.print_text(
                sensor[1], self.player, self.padding_left+200, line_pos, self.font_small)
            line_pos += self.small_font_size

        self.additional_ui(state,line_pos,mouse)
    
    def additional_ui(self, state,line_pos,mouse):
        return

    def print_text(self, text, color, x, y, font=None):
        font = font if font else self.font
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))




