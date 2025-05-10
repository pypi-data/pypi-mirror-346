import pygame
import numpy as np
import copy
import math
from PIL import Image
from .style import Gradient, Style, StyleType, StyleManager, Align, default_style
from .utils import mouse, RoundedSurface, Event, time
from .color import Color_Type, ColorType
from .animations import AnimationManager
#print
class NevuObject:
    def __init__(self,size,style:StyleManager=default_style,freedom=False): 
        self._style = None
        self._resize_ratio = [1,1]
        self._debug = False
        self.size_original = size
        self.size = list(size)
        self.coordinates = [0,0]
        self.master_coordinates = [0,0]
        self.constant_style = None
        self.style = style
        self._freedom = freedom
        self._text = ""
        self._words_split = False
        self.first_update_fuctions = []
        self._first_update = True
        self.hovered = False
        self._anim_coordinates = [0,0]
        self._anim_coordinates_initial = [0,0]
        self._anim_coordinates_additional = [0,0]
        self._anim_opacity = None
        self._anim_opacity_value = None
        self._anim_rotation = 0
        self._anim_rotation_value = 0

        self.animation_manager = AnimationManager()
        self._events = []
        
        self.__is_render = True
        self.__is_active = True
        self._is_changed = True
        
        self.x = 0 #ONLY FOR GRID LAYOUT
        self.y = 0 #ONLY FOR GRID LAYOUT
    def relx(self,num) -> int|float:
        return num*self._resize_ratio[0]
    def rely(self,num) -> int|float:
        return num*self._resize_ratio[1]
    def relm(self,num) -> int|float:
        return num*((self._resize_ratio[0]+self._resize_ratio[1])/2)
    def rel(self,mass) -> list:
        return [mass[0]*self._resize_ratio[0],mass[1]*self._resize_ratio[1]]
    def add_event(self,event:Event): self._events.append(event)
    def add_on_first_update(self,function): self.first_update_fuctions.append(function)
    def enable_render(self):
        self.__is_render = True
        self._is_changed = True
        self.unrendered = True
    def disable_render(self):
        self.__is_render = False
        self._is_changed = True
    @property
    def render(self): return self.__is_render
    @render.setter
    def render(self,value:bool):
        self.unrendered = True
        self.__is_render = value
        self._is_changed = True
    def activate(self):
        self.__is_active = True
        self._is_changed = True
    def disactivate(self):
        self.__is_active = False
        self._is_changed = True
    def _style_manager_select(self, type:StyleType):
        if not isinstance(self._style, StyleManager): return
        if self._style._selected != type:
            self._style.select(type)
            self._is_changed = True
            self.cached_gradient = None
            if isinstance(self, Widget):
                self._update_image()
    @property
    def active(self): return self.__is_active
    @active.setter
    def active(self,value:bool):
        if not self.__is_active != value:
            self.__is_active = value
            self._is_changed = True
    def _event_cycle(self,type:int,*args, **kwargs):
            for event in self._events:
                if event.type == type: event(*args, **kwargs)
    def update(self):
        if self._first_update:
            self._check_for_collide()
            self._first_update = False
            self._is_changed = True
            for item in self.first_update_fuctions: item()

        if isinstance(self, Widget):
            self._check_for_collide()

        self.animation_manager.update()
        if self.animation_manager.anim_position:
            self._anim_coordinates_initial = self.animation_manager.anim_position

        if self.animation_manager.anim_opacity:
            self._anim_opacity_value = self.animation_manager.anim_opacity
        if self._anim_opacity_value != self._anim_opacity:
            self._anim_opacity = self._anim_opacity_value

        self._update_anim_coordinates()
        self._event_cycle(Event.UPDATE)
    def _update_anim_coordinates(self):
        for i in range(2): self._anim_coordinates[i] = self._anim_coordinates_additional[i] + self._anim_coordinates_initial[i]
    def _check_for_collide(self):
        if isinstance(self._style, Style):
            if self.get_rect().collidepoint(mouse.pos):
                self.hovered = True
            else:
                self.hovered = False
            return
        try:
            is_colliding = self.get_rect().collidepoint(mouse.pos)
            new_hovered_state = is_colliding
            current_selected_style = self._style._selected
            new_style_selection = current_selected_style

            if is_colliding:
                if mouse.left_down:
                    new_style_selection = StyleType.CLICK
                    print("click", self)
                else:
                    new_style_selection = StyleType.HOVER
            else:
                new_style_selection = StyleType.STILL

            state_changed = (self.hovered != new_hovered_state) or (current_selected_style != new_style_selection)

            self.hovered = new_hovered_state
            self._style_manager_select(new_style_selection)
            
            if state_changed:
                self._is_changed = True
        except Exception as e:
            print(e, self)
    def get_rect(self):
        return pygame.Rect(
            self.master_coordinates[0] + self._anim_coordinates[0],
            self.master_coordinates[1] + self._anim_coordinates[1],
            *self.rel(self.size)
        )
    def get_font(self):
        if self.style.fontname == "Arial": renderFont = pygame.font.SysFont(self.style.fontname,int(self.style.fontsize*self._resize_ratio[1]))
        else: renderFont = pygame.font.Font(self.style.fontname,int(self.style.fontsize*self._resize_ratio[1]))
        return renderFont
class Widget(NevuObject):
    def __init__(self,size,style:StyleManager,freedom=False):
        self.surface = pygame.Surface(size,flags=pygame.SRCALPHA | pygame.HWSURFACE | pygame.DOUBLEBUF)
        super().__init__(size,style,freedom)
        self.cached_image = None
        self._hovered = False
        self._surface_copy_for_rotation = self.surface
        self._text_baked = None
        self._text_surface = None
        self._text_rect = None
        
        self.unrendered = False
        self.cached_gradient = None
        
        if isinstance(self.style.bgcolor, Gradient): self._draw_gradient()
    def _draw_gradient(self):
        self.cached_gradient = pygame.Surface(self.rel(self.size), flags=pygame.SRCALPHA)
        if self.style.transparency: self.cached_gradient = self.style.bgcolor.with_transparency(self.style.transparency).apply_gradient(self.cached_gradient)
        else: self.cached_gradient =  self.style.bgcolor.apply_gradient(self.cached_gradient)
    def _update_image(self,style=None):
        try:
            if not style: style = self.style
            if not style.bgimage: return
            img = pygame.image.load(style.bgimage)
            img.convert_alpha()
            self.cached_image = pygame.transform.scale(img,(self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]))
        except: self.cached_image = None
        self.surface.convert_alpha()
    def resize(self,_resize_ratio):
        self.cached_gradient = None
        self._is_changed = True
        self._resize_ratio = _resize_ratio
        self.surface = pygame.Surface([int(self.size[0]*self._resize_ratio[0]),int(self.size[1]*self._resize_ratio[1])],flags=pygame.SRCALPHA|pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._event_cycle(Event.RESIZE)
        self._update_image()
    @property
    def style(self):
        return self._style()
    @style.setter
    def style(self,style:StyleManager):
        self.cached_gradient = None
        self._style = copy.deepcopy(style)
        self._style_manager_select(StyleType.STILL)
        self._is_changed = True
        self._update_image()
    def draw(self):
        TRANSPARENT = (0,0,0,0)
        if not self.render:
            if self.unrendered: self.surface.fill(TRANSPARENT)
            return
        self._event_cycle(Event.DRAW)
        if self._is_changed:
            if type(self) == Widget: self._is_changed = False
            self.surface.fill(TRANSPARENT)
            if self._anim_opacity: self.surface.set_alpha(self._anim_opacity)
            if not self.cached_image:
                if self.animation_manager.anim_rotation: self.surface = pygame.transform.rotate(self.surface, -self.animation_manager.anim_rotation)
                if isinstance(self.style.bgcolor, Gradient):
                    if not isinstance(self.cached_gradient, pygame.Surface): self._draw_gradient()
                    self.surface.blit(self.cached_gradient, (0, 0))

                elif self.style.bgcolor ==Color_Type.TRANSPARENT: self.surface.fill(TRANSPARENT)
                else: self.surface.fill(self.style.bgcolor)
            else: self.surface.blit(self.cached_image,(0,0))
            if self.style.width > 0:
                if not self.style.bordercolor == Color_Type.TRANSPARENT:
                    surf = pygame.Surface(self.surface.get_size(),flags=pygame.SRCALPHA|pygame.HWSURFACE | pygame.DOUBLEBUF)
                    if self.style.transparency: surf.set_alpha(self.style.transparency)
                    pygame.draw.rect(surf,self.style.bordercolor,[0,0,*self.rel(self.size)],self.style.width,border_radius=int(self.relm(self.style.radius)))
                    self.surface.blit(surf,(0,0))
            if self.style.radius > 0: self.surface = RoundedSurface.create(self.surface,int(self.relm(self.style.radius)))
            if type(self) == Widget:
                if self.animation_manager.anim_rotation: self.surface = pygame.transform.rotate(self.surface, self.animation_manager.anim_rotation)
    @property
    def hovered(self): return self._hovered
    @hovered.setter
    def hovered(self, value):
        if not hasattr(self, "_hovered"): self._hovered = False
        if self._hovered != value:
            self._hovered = value
            self._is_changed = True
    def update(self,*args):
        super().update()
        #if self.animation_manager.anim_rotation:
        #    if self._anim_rotation_value != int(self.animation_manager.anim_rotation):
        #        center = pygame.Rect([int(self.coordinates[0]),int(self.coordinates[1])], self._surface_copy_for_rotation.get_size()).center
        #        self._anim_rotation_value = int(self.animation_manager.anim_rotation)
        #        self.surface = pygame.transform.rotate(self._surface_copy_for_rotation, self._anim_rotation_value)
        #        coordinates = list(self.surface.get_rect(center=center).topleft)
        #        for i in range(2): self._anim_coordinates_additional[i] = coordinates[i] - self.coordinates[i]
        #        self._is_changed = True                                                                                    #TODO unstable version, need to be fixed
        self._update_anim_coordinates()
        self._event_cycle(Event.UPDATE)
    def bake_text(self,text,unlimited_y=False,words_indent=False,alignx=Align.CENTER,aligny=Align.CENTER,continuous=False):
        if continuous:
            self._bake_text_single_continuous(text)
            return
        renderFont = self.get_font() 
        is_popped  =False
        line_height = renderFont.size("a")[1]
        words = list(text)
        marg = ""
        if words_indent:
            words = text.strip().split()
            marg = " "
        lines = []
        current_line = ""
        ifnn = False
        for word in words:
            if word == '\n':
                ifnn = True
            try:
                w = word[0]+word[1]
                if w == '\ '.strip()+"n":
                    ifnn = True
            except:
                pass
            if ifnn:
                lines.append(current_line)
                current_line = ""
                test_line = ""
                text_size = 0
                ifnn = False
                continue
            test_line = current_line + word + marg
            text_size = renderFont.size(test_line)
            if text_size[0] > self.size[0]*self._resize_ratio[0]:
                lines.append(current_line)
                current_line = word + marg
            else:
                current_line = test_line
        lines.append(current_line)
        if not unlimited_y:
            while len(lines) * line_height > self.size[1] * self._resize_ratio[1]:
                lines.pop(-1)
                is_popped = True
        self._text_baked = "\n".join(lines)
        if is_popped:
            if not unlimited_y:
                self._text_baked = self._text_baked[:-3] + "..."
                justify_y = False
            else:
                justify_y = True
        else:
            justify_y = False
        self._text_surface = renderFont.render(self._text_baked, True, self.style.fontcolor)
        container_rect = self.surface.get_rect()
        text_rect = self._text_surface.get_rect()
        if alignx == Align.LEFT: text_rect.left = container_rect.left
        elif alignx == Align.CENTER: text_rect.centerx = container_rect.centerx
        elif alignx == Align.RIGHT: text_rect.right = container_rect.right
        if aligny == Align.TOP: text_rect.top = container_rect.top
        elif aligny == Align.CENTER: text_rect.centery = container_rect.centery
        elif aligny == Align.BOTTOM: text_rect.bottom = container_rect.bottom
        self._text_rect = text_rect
    def _bake_text_single_continuous(self, text):
        renderFont = self.get_font()
        self.font_size = renderFont.size(text)
        self._text_surface = renderFont.render(self._entered_text, True, self.style.fontcolor)
        if not self.font_size[0]+self.relx(10) >= self.relx(self.size[0]): self._text_rect = self._text_surface.get_rect(left = self.relx(10), centery=self.surface.get_height() / 2)
        else: self._text_rect = self._text_surface.get_rect(right = self.relx(self.surface.get_width()-10), centery=self.surface.get_height()/2)
    @property
    def styletype(self): return type(self._style)
class Empty_Widget(Widget):
    def __init__(self, size):
        self._hovered = False
        super().__init__(size, default_style)
    def draw(self):
        pass

class Tooltip(Widget):
    def __init__(self,text,style=default_style):
        self.text = text
        self.style = style
        self.size = (200,400)
        self.bake_text(self.text,False,True,self.style.textalign_x,self.style.textalign_y)
        raise Exception("Tooltip is not implemented yet, wait till 0.05")
    def draw(self):
        pass #TODO in version 0.05
    
class Label(Widget):
    def __init__(self,size,text,style:StyleManager,freedom=False,words_indent = False):
        text = str(text)
        self._hovered = False
        super().__init__(size,style,freedom)
        self._text = "" 
        self.first_update_fuctions = []
        self._words_split = words_indent
        self.style = style
        self._is_changed = True
        self.text = text 
    @property
    def hovered(self): return self._hovered
    @hovered.setter
    def hovered(self,value:bool):
        if self.hovered == value and not self._first_update: return
        self._hovered = value
        self._update_image(self.style)
        self._is_changed = True
        self.bake_text(self._text,False,self._words_split,self.style.textalign_x,self.style.textalign_y)
        self.first_update_fuctions.append(lambda: self.bake_text(self._text,False,self._words_split,self.style.textalign_x,self.style.textalign_y))
    def _update_image(self,*args):
        style = self.style
        try:
            if not style.bgimage: return
            img = pygame.image.load(style.bgimage)
            img.convert_alpha()
            self.cached_image = pygame.transform.scale(img,(self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]))
        except:
            self.cached_image = None
        self.surface.convert_alpha()
    @property
    def text(self):
        return self._text
    @text.setter
    def text(self,text:str):
        self._is_changed = True
        self._text = text
        self.bake_text(text,False,self._words_split,self.style.textalign_x,self.style.textalign_y)
    def resize(self, _resize_ratio):
        self._is_changed = True
        super().resize(_resize_ratio)
        self.bake_text(self._text,False,self._words_split,self.style.textalign_x,self.style.textalign_y)
    @property
    def style(self):
        return self._style()
    @style.setter
    def style(self,style:StyleManager):
       # if self._style.bgcolor != style.bgcolor:
        self.cached_gradient = None
        self._is_changed = True
        self._style = copy.deepcopy(style)
        self._style_manager_select(StyleType.STILL)
        self._update_image()
        #if self._first_update: self.add_on_first_update(lambda:[self._first_set_style(style),print("JOPAA 2")])
        if hasattr(self,'_text'):
            self.bake_text(self._text)
    def draw(self):
        super().draw()
        if not self.render: return
        if self._is_changed:
            self._is_changed = False
            self.surface.blit(self._text_surface, self._text_rect)
            if self.animation_manager.anim_rotation: self.surface = pygame.transform.rotate(self.surface, self.animation_manager.anim_rotation)
        self._event_cycle(Event.RENDER)

class Button(Label):
    def __init__(self,function,text:str,size,style:StyleManager=default_style,active:bool = True,throw_errors=False,freedom=False,words_indent=False):
        super().__init__(size,text,style,freedom,words_indent)
        ### Basic variables
        self.function = function
        self.active = active
        self._throw = throw_errors
        
    def update(self,*args):
        #print(f"Button '{self._text}': Hovered={self.hovered}, Mouse LeftUp={mouse.left_up}, Mouse Pos={mouse.pos}, Rect={self.get_rect()}")
        super().update(*args)
        if not self.active or not isinstance(self,Button): return
        if self.hovered and mouse.left_up:
            if self.function:
                try: self.function()
                except Exception as e:
                    print(e)
                    if self._throw: raise e
class CheckBox(Button):
    def __init__(self,on_change_fuction,state,size,style:StyleManager,active:bool = True):
        super().__init__(lambda:on_change_fuction(state) if on_change_fuction else None,"",size,style)
        self._id = None
        self._check_box_group = None
        self.is_active = False
        self.state = state
        self.active = active
        self.count = 0
    def draw(self):
        super().draw()
        if not self.render:
            return
        if self.is_active:
            pygame.draw.rect(self.surface,(200,50,50),[0,0,self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]],border_radius=int(self._style.radius*(self._resize_ratio[0]+self._resize_ratio[1])/2))
        self._event_cycle(Event.RENDER)
        if self._is_changed:
            if self.animation_manager.anim_rotation:
                self.surface = pygame.transform.rotate(self.surface, self.animation_manager.anim_rotation)
            self._is_changed = False
    def _check_for_collide(self):
        if not self.active:
            return
        if self.get_rect().collidepoint(mouse.pos):
            if self.function:
                self.function()
                self.call_dot_group()
            
    def update(self,*args):
        super().update(*args)
        pass
    def connect_to_dot_group(self,dot_group,id):
        self._id = id
        self._check_box_group = dot_group
    def call_dot_group(self):
        self._check_box_group.active = self._id

class ImageWidget(Widget):
    def __init__(self,size,image,style:StyleManager):
        super().__init__(size,style)
        self.image_orig = image
        self.image = self.image_orig
        self.resize([1,1])
    def resize(self, _resize_ratio):
        super().resize(_resize_ratio)
        self.image = pygame.transform.scale(self.image_orig,(self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]))
        
    def draw(self):
        super().draw()
        if not self.render:
            return
        self._event_cycle(Event.DRAW)
        self.surface.blit(self.image,[0,0])
        if self._style().radius > 0:
            self.surface = RoundedSurface.create(self.surface,int(self._style().radius))
        self._event_cycle(Event.RENDER)
        if self._is_changed:
            if self.animation_manager.anim_rotation:
                self.surface = pygame.transform.rotate(self.surface, self.animation_manager.anim_rotation)
class GifWidget(Widget):
    def __init__(self,size,gif_path=None,style:StyleManager=default_style,frame_duration=100):
        """
        Инициализирует виджет для отображения GIF-анимации.

        Args:
            coordinates (list): Координаты виджета [x, y].
            surf (pygame.Surface): Поверхность, на которой будет отображаться виджет.
            size (list, optional): Размеры виджета [ширина, высота]. Defaults to [100, 100].
            radius (int, optional): Радиус скругления углов. Defaults to 0.
            gif_path (str, optional): Путь к GIF-файлу. Defaults to None.
            frame_duration (int, optional): Длительность одного кадра в миллисекундах. Defaults to 100.
        """
        super().__init__(size,style)
        self.gif_path = gif_path
        self.frames = []
        self.frame_index = 0
        self.frame_duration = frame_duration
        self.last_frame_time = 0
        self.original_size = size
        self._load_gif()
        #self.scale([1,1]) # сразу подгоняем кадры
        self.current_time = 0
        self.scaled_frames = None
        self.resize(self._resize_ratio)
    def _load_gif(self):
        """Загружает GIF-анимацию из файла."""
        if self.gif_path:
            try:
                gif = Image.open(self.gif_path)
                for i in range(gif.n_frames):
                    gif.seek(i)
                    frame_rgb = gif.convert('RGB')
                    frame_surface = pygame.image.frombuffer(frame_rgb.tobytes(), frame_rgb.size, 'RGB')
                    self.frames.append(frame_surface)
                
            except FileNotFoundError:
                print(f"Error: GIF file not found at {self.gif_path}")
            except Exception as e:
                print(f"Error loading GIF: {e}")

    def resize(self, _resize_ratio):
        super().resize(_resize_ratio)
        """Изменяет размер GIF-анимации.
        Args:
            _resize_ratio (list, optional): Коэффициент масштабирования [scale_x, scale_y]. Defaults to [1, 1].
        """
        if self.frames:
            self.scaled_frames = [pygame.transform.scale(frame,[self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]]) for frame in self.frames]


    def draw(self):
        """Отрисовывает текущий кадр GIF-анимации."""
        super().draw()
        if not self.render:
            return
        if not self.frames:
            return
        self.current_time += 1*time.delta_time*100
        if self.current_time > self.frame_duration:
             self.frame_index = (self.frame_index + 1) % len(self.frames)
             self.current_time = 0
        if self.scaled_frames:
            frame_to_draw = self.scaled_frames[self.frame_index] if hasattr(self,"scaled_frames") else self.frames[self.frame_index]
            frame_rect = frame_to_draw.get_rect(center=self.coordinates)
            self.surface.blit(frame_to_draw,(0,0))
        self._event_cycle(Event.RENDER)
        if self._is_changed:
            if self.animation_manager.anim_rotation:
                self.surface = pygame.transform.rotate(self.surface, self.animation_manager.anim_rotation)

class Input(Widget):
    def __init__(self, size, style, default: str = "", placeholder: str = "", blacklist=None,
                 whitelist=None, on_change_function=None, multiple=False, active=True,
                 allow_paste=True, words_indent=False, max_characters=None):
        super().__init__(size, style)
        self._entered_text = ""
        self.selected = False
        self.blacklist = blacklist
        self.whitelist = whitelist
        self.placeholder = placeholder
        self._on_change_fun = on_change_function
        self.active = active
        self.iy = multiple
        self.paste = allow_paste
        self._wordssplit = words_indent
        self.max_characters = max_characters
        self._text_scroll_offset = 0
        self._text_scroll_offset_y = 0
        self.max_scroll_y = 0
        self._cursor_place = 0
        self._text_surface = None
        self._text_rect = pygame.Rect(0,0,0,0)
        self.left_margin = 10
        self.right_margin = 10
        self.top_margin = 5
        self.bottom_margin = 5
        self._init_cursor()
        self.text = default
    def _init_cursor(self):
        if not hasattr(self,"_resize_ratio"): self._resize_ratio = [1,1]
        if not hasattr(self, 'style'): return
        try: font_height = self._get_line_height()
        except (pygame.error, AttributeError): font_height = self.size[1] * self._resize_ratio[1] * 0.8
        cursor_width = max(1, int(self.size[0]*0.01*self._resize_ratio[0]))
        self.cursor = pygame.Surface((cursor_width, font_height))
        try: self.cursor.fill(self.style.secondarycolor)
        except AttributeError: self.cursor.fill((0,0,0))
    def _get_line_height(self):
        try:
            if not hasattr(self, 'style') or not self.style.fontname: raise AttributeError("Font not ready")
            return self.get_font().get_height()
        except (pygame.error, AttributeError):
            fallback_height = self.size[1] * self._resize_ratio[1] - self.top_margin - self.bottom_margin
            return max(5, int(fallback_height * 0.8))
    def _get_cursor_line_col(self):
        if not self._entered_text: return 0, 0
        lines = self._entered_text.split('\n')
        abs_pos = self._cursor_place
        current_pos = 0
        for i, line in enumerate(lines):
            line_len = len(line)
            if abs_pos <= current_pos + line_len:
                col = abs_pos - current_pos
                return i, col
            current_pos += line_len + 1
        last_line_index = len(lines) - 1
        last_line_len = len(lines[last_line_index]) if last_line_index >= 0 else 0
        return last_line_index, last_line_len
    def _get_abs_pos_from_line_col(self, target_line_index, target_col_index):
        lines = self._entered_text.split('\n')
        target_line_index = max(0, min(target_line_index, len(lines) - 1))
        abs_pos = 0
        for i in range(target_line_index): abs_pos += len(lines[i]) + 1
        current_line_len = len(lines[target_line_index]) if target_line_index < len(lines) else 0
        target_col_index = max(0, min(target_col_index, current_line_len))
        abs_pos += target_col_index
        return abs_pos
    def _update_scroll_offset(self):
        if not hasattr(self,'style'): return
        if not hasattr(self, 'surface'): return
        try:
            renderFont = self.get_font()
            cursor_line_idx, cursor_col_idx = self._get_cursor_line_col()
            lines = self._entered_text.split('\n')
            cursor_line_text = lines[cursor_line_idx] if cursor_line_idx < len(lines) else ""
            text_before_cursor_in_line = cursor_line_text[:cursor_col_idx]
            ideal_cursor_x_offset = renderFont.size(text_before_cursor_in_line)[0]
            full_line_width = renderFont.size(cursor_line_text)[0]
        except (pygame.error, AttributeError, IndexError): return
        l_margin = self.left_margin * self._resize_ratio[0]
        r_margin = self.right_margin * self._resize_ratio[0]
        visible_width = self.surface.get_width() - l_margin - r_margin
        
        if visible_width < 1: visible_width = 1
        cursor_pos_relative_to_visible_start = ideal_cursor_x_offset - self._text_scroll_offset
        if cursor_pos_relative_to_visible_start < 0: self._text_scroll_offset = ideal_cursor_x_offset
        elif cursor_pos_relative_to_visible_start > visible_width: self._text_scroll_offset = ideal_cursor_x_offset - visible_width

        max_scroll_x = max(0, full_line_width - visible_width)
        self._text_scroll_offset = max(0, min(self._text_scroll_offset, max_scroll_x))
        self._is_changed = True
    def _update_scroll_offset_y(self):
        if not self.iy or not hasattr(self, 'style'): return
        if not self._text_surface: return
        try:
            line_height = self._get_line_height()
            cursor_line, _ = self._get_cursor_line_col()
            ideal_cursor_y_offset = cursor_line * line_height
            total_text_height = self._text_surface.get_height()
        except (pygame.error, AttributeError, IndexError): return
        t_margin = self.top_margin * self._resize_ratio[1]
        b_margin = self.bottom_margin * self._resize_ratio[1]
        visible_height = self.surface.get_height() - t_margin - b_margin
        if visible_height < 1 : visible_height = 1
        self.max_scroll_y = max(0, total_text_height - visible_height)
        if ideal_cursor_y_offset < self._text_scroll_offset_y: self._text_scroll_offset_y = ideal_cursor_y_offset
        elif ideal_cursor_y_offset + line_height > self._text_scroll_offset_y + visible_height: self._text_scroll_offset_y = ideal_cursor_y_offset + line_height - visible_height
        self._text_scroll_offset_y = max(0, min(self._text_scroll_offset_y, self.max_scroll_y))
        self._is_changed = True
    def bake_text(self, text, unlimited_y=False, words_indent=False, alignx=Align.LEFT, aligny=Align.TOP, continuous=False, multiline_mode=False):
        if not hasattr(self, 'style') or not hasattr(self, 'surface'): return
        renderFont = self.get_font()
        line_height = self._get_line_height()
        if continuous:
            try: self._text_surface = renderFont.render(text, True, self.style.fontcolor)
            except (pygame.error, AttributeError): self._text_surface = None
            return
        if multiline_mode:
            lines = text.split('\n')
            if not lines: self._text_surface = pygame.Surface((1, line_height), pygame.SRCALPHA); self._text_surface.fill((0,0,0,0)); return
            max_width = 0
            rendered_lines = []
            try:
                for line in lines:
                        line_surface = renderFont.render(line, True, self.style.fontcolor)
                        rendered_lines.append(line_surface)
                        max_width = max(max_width, line_surface.get_width())
            except (pygame.error, AttributeError): self._text_surface = None; return
            total_height = len(lines) * line_height
            self._text_surface = pygame.Surface((max(1, max_width), max(line_height, total_height)), pygame.SRCALPHA)
            self._text_surface.fill((0,0,0,0))

            current_y = 0
            for line_surface in rendered_lines:
                self._text_surface.blit(line_surface, (0, current_y))
                current_y += line_height
            return
        lines = []
        current_line = ""
        max_line_width = self.size[0] * self._resize_ratio[0] - self.left_margin*self._resize_ratio[0] - self.right_margin*self._resize_ratio[0]
        processed_text = text.replace('\r\n', '\n').replace('\r', '\n')
        paragraphs = processed_text.split('\n')
        try:
            for para in paragraphs:
                words = para.split(' ') if words_indent else list(para)
                current_line = ""
                sep = " " if words_indent else ""
                for word in words:
                    test_line = current_line + word + sep
                    if renderFont.size(test_line)[0] <= max_line_width:current_line = test_line
                    else:
                        if current_line: lines.append(current_line.rstrip())
                        current_line = word + sep
                if current_line: lines.append(current_line.rstrip())

            max_visible_lines = int((self.size[1] * self._resize_ratio[1] - self.top_margin*self._resize_ratio[1] - self.bottom_margin*self._resize_ratio[1]) / line_height)
            visible_lines = lines[:max_visible_lines]

            if not visible_lines:
                self._text_surface = pygame.Surface((1, 1), pygame.SRCALPHA); self._text_surface.fill((0,0,0,0))
                self._text_rect = self._text_surface.get_rect(topleft=(self.left_margin*self._resize_ratio[0], self.top_margin*self._resize_ratio[1]))
                return
            max_w = max(renderFont.size(line)[0] for line in visible_lines) if visible_lines else 1
            total_h = len(visible_lines) * line_height
            self._text_surface = pygame.Surface((max(1,max_w), max(1,total_h)), pygame.SRCALPHA)
            self._text_surface.fill((0,0,0,0))
            cury = 0
            for line in visible_lines:
                line_surf = renderFont.render(line, True, self.style.fontcolor)
                self._text_surface.blit(line_surf, (0, cury))
                cury += line_height

            self._text_rect = self._text_surface.get_rect(topleft=(self.left_margin*self._resize_ratio[0], self.top_margin*self._resize_ratio[1]))
        except (pygame.error, AttributeError):
             self._text_surface = None
             self._text_rect = pygame.Rect(0,0,0,0)
    def _right_bake_text(self):
        if not hasattr(self, 'style'): return
        text_to_render = self._entered_text if len(self._entered_text) > 0 else self.placeholder
        if self.iy:
            self.bake_text(text_to_render, multiline_mode=True)
            self._update_scroll_offset_y()
            self._update_scroll_offset()
        else:
            self.bake_text(text_to_render, continuous=True)
            self._update_scroll_offset()
    def resize(self, _resize_ratio):
        super().resize(_resize_ratio)
        self._init_cursor()
        self._right_bake_text()
    @property
    def style(self):
        return self._style()
    @style.setter
    def style(self, style:StyleManager):
        self.cached_gradient = None
        self._is_changed = True
        self._style = copy.deepcopy(style)
        self._style_manager_select(StyleType.STILL)
        self._update_image()
        self.left_margin = getattr(style, 'padding_left', 10)
        self.right_margin = getattr(style, 'padding_right', 10)
        self.top_margin = getattr(style, 'padding_top', 5)
        self.bottom_margin = getattr(style, 'padding_bottom', 5)
        self._init_cursor()
        if hasattr(self,'_entered_text'):
             self._right_bake_text()
    def update(self,events:list[pygame.event.Event]):
        super().update()
        if not self.active:
            if self.selected:
                 self.selected = False
                 self._is_changed = True
            return
        prev_selected = self.selected
        mouse_collided = self.get_rect().collidepoint(mouse.pos)
        self.check_selected(mouse_collided)
        if prev_selected != self.selected and self.selected:
             self._update_scroll_offset()
             self._update_scroll_offset_y()
        elif prev_selected != self.selected and not self.selected:
             self._is_changed = True
        if self.selected:
            text_changed = False
            cursor_moved = False
            for event in events:
                if event.type == pygame.KEYDOWN:
                    initial_cursor_place = self._cursor_place
                    initial_text = self._entered_text
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if self.iy:
                             if self.max_characters is None or len(self._entered_text) < self.max_characters:
                                self._entered_text = self._entered_text[:self._cursor_place] + '\n' + self._entered_text[self._cursor_place:]
                                self._cursor_place += 1
                    elif event.key == pygame.K_UP:
                        if self.iy:
                            current_line, current_col = self._get_cursor_line_col()
                            if current_line > 0:
                                self._cursor_place = self._get_abs_pos_from_line_col(current_line - 1, current_col)
                    elif event.key == pygame.K_DOWN:
                         if self.iy:
                             lines = self._entered_text.split('\n')
                             current_line, current_col = self._get_cursor_line_col()
                             if current_line < len(lines) - 1:
                                 self._cursor_place = self._get_abs_pos_from_line_col(current_line + 1, current_col)
                    elif event.key == pygame.K_RIGHT:
                        self._cursor_place = min(len(self._entered_text),self._cursor_place+1)
                    elif event.key == pygame.K_LEFT:
                        self._cursor_place = max(0,self._cursor_place-1)
                    elif event.key == pygame.K_BACKSPACE:
                        if self._cursor_place > 0:
                            self._entered_text = self._entered_text[:self._cursor_place-1] + self._entered_text[self._cursor_place:]
                            self._cursor_place = max(0,self._cursor_place-1)
                    elif event.key == pygame.K_DELETE:
                         if self._cursor_place < len(self._entered_text):
                              self._entered_text = self._entered_text[:self._cursor_place] + self._entered_text[self._cursor_place+1:]
                    elif event.key == pygame.K_HOME:
                         if self.iy:
                              line_idx, _ = self._get_cursor_line_col()
                              self._cursor_place = self._get_abs_pos_from_line_col(line_idx, 0)
                         else:
                              self._cursor_place = 0
                    elif event.key == pygame.K_END:
                         if self.iy:
                              line_idx, _ = self._get_cursor_line_col()
                              lines = self._entered_text.split('\n')
                              line_len = len(lines[line_idx]) if line_idx < len(lines) else 0
                              self._cursor_place = self._get_abs_pos_from_line_col(line_idx, line_len)
                         else:
                              self._cursor_place = len(self._entered_text)
                    elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                        if self.paste:
                            pasted_text = ""
                            try:
                                pasted_text = pygame.scrap.get(pygame.SCRAP_TEXT)
                                if pasted_text:
                                    pasted_text = pasted_text.decode('utf-8').replace('\x00', '')
                            except (pygame.error, UnicodeDecodeError, TypeError):
                                pasted_text = ""

                            if pasted_text:
                                filtered_text = ""
                                for char in pasted_text:
                                    valid_char = True
                                    if self.blacklist and char in self.blacklist: valid_char = False
                                    if self.whitelist and char not in self.whitelist: valid_char = False
                                    if not self.iy and char in '\r\n': valid_char = False
                                    if valid_char: filtered_text += char

                                if self.max_characters is not None:
                                    available_space = self.max_characters - len(self._entered_text)
                                    filtered_text = filtered_text[:max(0, available_space)]

                                if filtered_text:
                                    self._entered_text = self._entered_text[:self._cursor_place] + filtered_text + self._entered_text[self._cursor_place:]
                                    self._cursor_place += len(filtered_text)

                    elif event.unicode:
                        unicode = event.unicode
                        is_valid_unicode = len(unicode) == 1 and ord(unicode) >= 32 and (unicode != "\x7f")
                        is_newline_ok = self.iy or (unicode not in '\r\n')

                        if is_valid_unicode and is_newline_ok:
                            if self.max_characters is None or len(self._entered_text) < self.max_characters:
                                valid_char = True
                                if self.blacklist and unicode in self.blacklist: valid_char = False
                                if self.whitelist and unicode not in self.whitelist: valid_char = False

                                if valid_char:
                                    self._entered_text = self._entered_text[:self._cursor_place] + unicode + self._entered_text[self._cursor_place:]
                                    self._cursor_place += len(unicode)

                    if self._cursor_place != initial_cursor_place: cursor_moved = True
                    if self._entered_text != initial_text: text_changed = True
                    if text_changed or cursor_moved: self._is_changed = True

                elif event.type == pygame.MOUSEWHEEL:
                    if self.iy and self.selected and mouse_collided:
                         scroll_multiplier = 3
                         line_h = 1
                         try:
                             line_h = self._get_line_height()
                         except: pass
                         scroll_amount = event.y * line_h * scroll_multiplier
                         if not hasattr(self, 'max_scroll_y'): self._update_scroll_offset_y()

                         self._text_scroll_offset_y -= scroll_amount
                         self._text_scroll_offset_y = max(0, min(self._text_scroll_offset_y, getattr(self, 'max_scroll_y', 0)))
                         self._is_changed = True
            if text_changed:
                 self._right_bake_text()
                 if self._on_change_fun:
                     try:
                          self._on_change_fun(self._entered_text)
                     except Exception as e:
                          print(f"Error in Input on_change_function: {e}")
            elif cursor_moved:
                 self._update_scroll_offset()
                 self._update_scroll_offset_y()
    def check_selected(self, collided):
        if collided and mouse.left_fdown:
            if not self.selected:
                 self.selected = True
                 self._is_changed = True
                 try:
                     renderFont = self.get_font()
                     relative_x = mouse.pos[0] - self.master_coordinates[0]
                     relative_y = mouse.pos[1] - self.master_coordinates[1]
                     l_margin = self.left_margin * self._resize_ratio[0]
                     t_margin = self.top_margin * self._resize_ratio[1]

                     if self.iy:
                          line_height = self._get_line_height()
                          if line_height <= 0 : line_height = 1 # Prevent division by zero
                          target_line_idx_float = (relative_y - t_margin + self._text_scroll_offset_y) / line_height
                          target_line_index = max(0, int(target_line_idx_float))

                          lines = self._entered_text.split('\n')
                          target_line_index = min(target_line_index, len(lines) - 1)

                          target_x_in_full_line = relative_x - l_margin + self._text_scroll_offset
                          target_line_text = lines[target_line_index] if target_line_index < len(lines) else ""

                          best_col_index = 0
                          min_diff = float('inf')
                          current_w = 0
                          for i, char in enumerate(target_line_text):
                               char_w = renderFont.size(char)[0]
                               pos_before = current_w
                               pos_after = current_w + char_w
                               diff_before = abs(target_x_in_full_line - pos_before)
                               diff_after = abs(target_x_in_full_line - pos_after)

                               if diff_before <= min_diff:
                                   min_diff = diff_before
                                   best_col_index = i
                               if diff_after < min_diff:
                                    min_diff = diff_after
                                    best_col_index = i + 1
                               current_w += char_w

                          best_col_index = max(0, min(best_col_index, len(target_line_text)))
                          self._cursor_place = self._get_abs_pos_from_line_col(target_line_index, best_col_index)
                     else:
                         target_x_in_full_text = relative_x - l_margin + self._text_scroll_offset
                         best_index = 0
                         min_diff = float('inf')
                         current_w = 0
                         for i, char in enumerate(self._entered_text):
                              char_w = renderFont.size(char)[0]
                              pos_before = current_w
                              pos_after = current_w + char_w
                              diff_before = abs(target_x_in_full_text - pos_before)
                              diff_after = abs(target_x_in_full_text - pos_after)

                              if diff_before <= min_diff:
                                   min_diff = diff_before
                                   best_index = i
                              if diff_after < min_diff:
                                   min_diff = diff_after
                                   best_index = i + 1
                              current_w += char_w

                         best_index = max(0, min(best_index, len(self._entered_text)))
                         self._cursor_place = best_index

                     self._update_scroll_offset()
                     self._update_scroll_offset_y()

                 except (pygame.error, AttributeError, IndexError) as e:
                     pass

        elif not collided and mouse.left_fdown:
            if self.selected:
                 self.selected = False
                 self._is_changed = True
    @property
    def text(self): return self._entered_text
    @text.setter
    def text(self,text:str):
        if not isinstance(text, str): text = str(text)

        original_text = self._entered_text
        if not self.iy:
            text = text.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')

        if self.max_characters is not None:
            text = text[:self.max_characters]

        self._entered_text = text
        self._cursor_place = min(len(self._entered_text), self._cursor_place)
        self._is_changed = True
        self._right_bake_text()

        if self._on_change_fun and original_text != self._entered_text:
            try: self._on_change_fun(self._entered_text)
            except Exception as e: print(f"Error in Input on_change_function (setter): {e}")
    def draw(self):
        super().draw()
        if not self.render: return
        try:
            renderFont = self.get_font()
            font_loaded = True
            line_height = self._get_line_height()
            cursor_height = self.cursor.get_height()
        except (pygame.error, AttributeError):
            font_loaded = False
            line_height = 15 
            cursor_height = 12 
        if not font_loaded: return
        l_margin = self.left_margin * self._resize_ratio[0]
        r_margin = self.right_margin * self._resize_ratio[0]
        t_margin = self.top_margin * self._resize_ratio[1]
        b_margin = self.bottom_margin * self._resize_ratio[1]
        clip_rect = self.surface.get_rect()
        clip_rect.left = l_margin
        clip_rect.top = t_margin
        clip_rect.width = self.surface.get_width() - l_margin - r_margin
        clip_rect.height = self.surface.get_height() - t_margin - b_margin
        if clip_rect.width < 0: clip_rect.width = 0
        if clip_rect.height < 0: clip_rect.height = 0
        if self._text_surface:
            if self.iy:
                self._text_rect = self._text_surface.get_rect(topleft=(l_margin - self._text_scroll_offset, t_margin - self._text_scroll_offset_y))
            else:
                self._text_rect = self._text_surface.get_rect(left=l_margin - self._text_scroll_offset,centery=(t_margin + self.surface.get_height() - b_margin) / 2 )
            original_clip = self.surface.get_clip()
            self.surface.set_clip(clip_rect)
            self.surface.blit(self._text_surface, self._text_rect)
            self.surface.set_clip(original_clip)
        if self.selected:
            cursor_visual_x = 0
            cursor_visual_y = 0
            try:
                if self.iy:
                    cursor_line, cursor_col = self._get_cursor_line_col()
                    lines = self._entered_text.split('\n')
                    line_text = lines[cursor_line] if cursor_line < len(lines) else ""
                    text_before_cursor_in_line = line_text[:cursor_col]
                    cursor_x_offset = renderFont.size(text_before_cursor_in_line)[0]
                    cursor_visual_x = l_margin + cursor_x_offset - self._text_scroll_offset
                    cursor_visual_y = t_margin + (cursor_line * line_height) - self._text_scroll_offset_y
                else:
                    text_before_cursor = self._entered_text[:self._cursor_place]
                    cursor_x_offset = renderFont.size(text_before_cursor)[0]
                    cursor_visual_x = l_margin + cursor_x_offset - self._text_scroll_offset
                    cursor_visual_y = (self.surface.get_height() - cursor_height) / 2

                cursor_draw_rect = self.cursor.get_rect(topleft=(cursor_visual_x, cursor_visual_y))
                if clip_rect.colliderect(cursor_draw_rect):
                    self.surface.blit(self.cursor, cursor_draw_rect.topleft)
            except (pygame.error, AttributeError, IndexError):pass
            self._is_changed = True
        self._event_cycle(Event.RENDER)
        
class MusicPlayer(Widget):
    def __init__(self, size, music_path, style: StyleManager = default_style):
        super().__init__(size, style)
        pygame.mixer.init()
        self.music_path = music_path
        self.sound = pygame.mixer.Sound(music_path) 
        self.music_length = self.sound.get_length() * 1000 
        self.channel = None 
        self.start_time = 0 
        self.progress = 0
        self.side_button_size = self.size[1] / 4
        self.progress_bar_height = self.size[1] / 4
        self.cross_image = self.draw_cross()
        self.circle_image = self.draw_circle()
        self.button_image = self.circle_image
        self.button_rect = self.button_image.get_rect(center=(self.side_button_size / 2, self.side_button_size / 2))
        self.time_label = Label((size[0] - self.side_button_size * 2, 20),
                              f"{self.format_time(self.progress)}/{self.format_time(self.music_length)}",
                              style(fontsize=12, bordercolor=Color_Type.TRANSPARENT, bgcolor=Color_Type.TRANSPARENT))
        self.is_playing = False
        self.sinus_margin = 0

    def resize(self, _resize_ratio):
        super().resize(_resize_ratio)
        self.time_label.resize(_resize_ratio)
    def draw_sinusoid(self,size,frequency,margin):
        self.sinus_surf = pygame.Surface(size,pygame.SRCALPHA)
        self.sinus_surf.fill((0,0,0,0))
        for i in range(int(size[0])):
            y = abs(int(size[1] * math.sin(frequency * i+margin))) 
            y = size[1]-y
            print(y)
            pygame.draw.line(self.sinus_surf,(50,50,200),(i,size[1]),(i,y))
            
    def update(self, *args):
        super().update()
        if self.is_playing:
            self.sinus_margin+=1*time.delta_time
        if self.sinus_margin >= 100:
            self.sinus_margin = 0
        self.time_label.coordinates = [(self.size[0] / 2 - self.time_label.size[0] / 2) * self._resize_ratio[0],(self.size[1] - self.time_label.size[1]) * self._resize_ratio[1]]
        if mouse.left_fdown:
            if pygame.Rect([self.master_coordinates[0], self.master_coordinates[1]],[self.side_button_size, self.side_button_size]).collidepoint(mouse.pos):
                self.toggle_play()

        if self.is_playing:
            self.progress = pygame.time.get_ticks() - self.start_time
            if self.progress >= self.music_length:
                self.stop()
            self.time_label.text = f"{self.format_time(self.progress)}/{self.format_time(self.music_length)}"
            self.button_image = self.cross_image 
        else:
            self.button_image = self.circle_image
            if self.progress >= self.music_length:
                self.progress = 0

            self.time_label.text = f"{self.format_time(self.progress)}/{self.format_time(self.music_length)}"
    def format_time(self, milliseconds):
        total_seconds = milliseconds // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02}:{seconds:02}"
    def toggle_play(self):
        if self.is_playing:
            self.pause()
        else:
            self.play()
    def play(self):
            self.channel = self.sound.play(0)
            if self.channel is not None:
                self.start_time = self.progress 
                self.is_playing = True
            else:
                print("Error: Could not obtain a channel to play the sound. Jopa also")
    def pause(self):
        if self.is_playing:
            if self.channel:
                self.channel.pause()
            self.is_playing = False
    def stop(self):
        if self.channel:
            self.channel.stop()
        self.is_playing = False
        self.progress = 0
    def draw_cross(self):
        cross_surface = pygame.Surface((self.side_button_size, self.side_button_size), pygame.SRCALPHA)
        pygame.draw.line(cross_surface, (255, 255, 255), (5, 5), (self.side_button_size - 5, self.side_button_size - 5), 3)
        pygame.draw.line(cross_surface, (255, 255, 255), (self.side_button_size - 5, 5), (5, self.side_button_size - 5), 3)
        return cross_surface

    def draw_circle(self):
        circle_surface = pygame.Surface((self.side_button_size, self.side_button_size), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, (255, 255, 255), (self.side_button_size // 2, self.side_button_size // 2),self.side_button_size // 2 - 5)
        return circle_surface

    def draw(self):
        super().draw()
        self.surface.blit(self.button_image, self.button_rect)
        progress_width = (self.size[0] / 1.2 * (self.progress / self.music_length)) * self._resize_ratio[0] if self.music_length > 0 else 0
        pygame.draw.rect(self.surface, (10, 10, 10),
                         ((self.size[0] - self.size[0] / 1.2) / 2 * self._resize_ratio[0],
                          (self.size[1] / 2 - self.progress_bar_height / 2) * self._resize_ratio[1],
                          self.size[0] / 1.2 * self._resize_ratio[0],
                          self.progress_bar_height * self._resize_ratio[1]), 0, self.style.radius)
        self.draw_sinusoid([progress_width,self.size[1]/17*self._resize_ratio[1]],0.15,self.sinus_margin)
        self.surface.blit(self.sinus_surf,((self.size[0] - self.size[0] / 1.2) / 2 * self._resize_ratio[0],(self.size[1] / 2 - self.sinus_surf.get_height()-self.progress_bar_height / 2) * self._resize_ratio[1]))
        pygame.draw.rect(self.surface, (50, 50, 200),
                         ((self.size[0] - self.size[0] / 1.2) / 2 * self._resize_ratio[0],
                          (self.size[1] / 2 - self.progress_bar_height / 2) * self._resize_ratio[1], progress_width,
                          self.progress_bar_height * self._resize_ratio[1]), 0, -1,0,0,self.style.radius,self.style.radius)

        self.time_label.draw()
        self.surface.blit(self.time_label.surface, self.time_label.coordinates)
        self._event_cycle(Event.RENDER)
        if self._is_changed:
            if self.animation_manager.anim_rotation:
                self.surface = pygame.transform.rotate(self.surface, self.animation_manager.anim_rotation)

class ProgressBar(Widget):
    def __init__(self, size,min_value,max_value,default_value,style: StyleManager=default_style):
        super().__init__(size,style)
        self._min_value = min_value
        self._max_value = max_value
        self.value = default_value
        self.percentage_of_value = self.value
    @property
    def percentage(self):
        return self._percentage
    @percentage.setter
    def percentage(self,value):
        self._percentage = value
        self.value = self._min_value+(self._max_value-self._min_value)*self._percentage
    @percentage.setter
    def percentage_of_value(self,value):
        self._percentage = (value-self._min_value)/(self._max_value-self._min_value)
    @property
    def value(self):
        return self._current_value
    @value.setter
    def value(self,value):
        self._current_value = value
        self.percentage_of_value = value
    def draw(self):
        if not self.render: return
        super().draw()
        pygame.draw.rect(self.surface,self.style.secondarycolor,[1,1,int(self.size[0]*self.percentage*self._resize_ratio[0])-2,int(self.size[1]*self._resize_ratio[1])-2],0,border_radius=int(self.style.radius))
        if self._is_changed:
            if self.animation_manager.anim_rotation:
                self.surface = pygame.transform.rotate(self.surface, self.animation_manager.anim_rotation)
class SliderBar(Widget):
    def __init__(self, begin_val: int, end_val: int, size, style, step: int = 1, freedom=False,default=-999.999123):
        self.button = Button(lambda: None, "", [size[1]/1.2, size[1]/1.2], style, active=False, freedom=False)
        super().__init__(size, style, freedom)
        self.begin_val = begin_val 
        self.end_val = end_val      
        self.step = step          
        self.current_value = begin_val 
        self.is_dragging = False    
        self.slider_pos = 0         
        if default!= -999.999123:
            self.current_value = default
        self._update_slider_position()  
    @property
    def style(self):
        return self._style()
    @style.setter
    def style(self,style:StyleManager):
        self._update_image()
        self.cached_gradient = None
        self._is_changed = True
        self._style = copy.deepcopy(style)
        self.button.style = copy.deepcopy(style)
        self._style_manager_select(StyleType.STILL)
    def _update_slider_position(self):
        """Обновляет позицию ползунка на основе текущего значения"""
        range_val = self.end_val - self.begin_val
        if range_val == 0:
            self.slider_pos = 0
        else:
            self.slider_pos = (self.current_value - self.begin_val) / range_val * self.size[0]

    def _update_value_from_position(self):
        range_val = self.end_val - self.begin_val
        if range_val == 0:
            self.current_value = self.begin_val
        else:
            self.current_value = self.begin_val + (self.slider_pos / self.size[0]) * range_val
            self.current_value = round(self.current_value / self.step) * self.step
            self.current_value = max(self.begin_val, min(self.end_val, self.current_value))

    def update(self, *args):
        super().update(*args)
        if not self.active: return
        if mouse.left_down or mouse.left_fdown:
            if self.get_rect().collidepoint(mouse.pos): self.is_dragging = True
        else: self.is_dragging = False
        if self.is_dragging:
            self._is_changed = True
            relative_x = mouse.pos[0] - self.master_coordinates[0]
            self.slider_pos = max(0, min(self.size[0], relative_x))
            self._update_value_from_position()
            self._update_slider_position()
        self.button.coordinates = [0,0]
        self.button.master_coordinates = [0,0]
        self.button.update()
    def draw(self):
        if not self.render:return
        super().draw()
        #pygame.draw.line(self.surface, self.style.bordercolor,(0, self.size[1] // 2), (self.size[0], self.size[1] // 2), 6)
        slider_rect = pygame.Rect(max(0,min(self.slider_pos - self.button.size[0]/2,self.size[0]-self.button.size[0])),(self.size[1]- self.button.size[1])/2,  self.button.size[0], self.button.size[1])
        #pygame.draw.rect(self.surface, self.style.secondarycolor, slider_rect)
        self.button.draw()
        self.surface.blit(self.button.surface, slider_rect)
        self.bake_text(str(self.current_value), alignx='left', aligny='center')
        self.surface.blit(self._text_surface, self._text_rect)
        if self._is_changed:
            if self.animation_manager.anim_rotation:
                self.surface = pygame.transform.rotate(self.surface, self.animation_manager.anim_rotation)
            self._is_changed = False
        

class ElementSwitcher(Widget):
    def __init__(self, size, elements, style: StyleManager = default_style,on_change_function=None):
        super().__init__(size, style)
        self.elements = elements
        self.current_index = 0
        self.button_padding = 10
        self.arrow_width = 10
        self.bake_text(self.current_element_text())
        self.on_change_function = on_change_function
    def current_element_text(self):
        if not self.elements: return ""
        return f"{self.elements[self.current_index]}"
    def next_element(self):
        self.current_index = (self.current_index + 1) % len(self.elements)
        self.bake_text(self.current_element_text())
        if self.on_change_function: self.on_change_function(self.current_element_text())
    def previous_element(self):
        self.current_index = (self.current_index - 1) % len(self.elements)
        self.bake_text(self.current_element_text())
        if self.on_change_function: self.on_change_function(self.current_element_text())
    def set_index(self,index:int):
        self.current_index = index
        self.bake_text(self.current_element_text())
        if self.on_change_function: self.on_change_function(self.current_element_text())
    @property
    def hovered(self):
        return self._hovered
    @hovered.setter
    def hovered(self,value:bool):
        if hasattr(self, "_hovered") and self.hovered == value:
            return
        self._hovered = value
        if not hasattr(self, "elements"):
            self.add_on_first_update(lambda: self.bake_text(self.current_element_text()))
            return
        self.bake_text(self.current_element_text())

    def update(self, *args):
        super().update(*args)
        if not self.active:
            return
        if mouse.left_up and self.hovered:
            click_pos_relative = np.array(mouse.pos) - self.master_coordinates
            center_x = self.surface.get_width() / 2
            button_width = self._text_rect.width / 2 + self.button_padding + self.arrow_width * 2
            if click_pos_relative[0] < center_x - button_width / 2: self.previous_element()
            elif click_pos_relative[0] > center_x + button_width / 2: self.next_element()

    def draw(self):
        super().draw()
        if not self.render:
            return
        text_center_x = self.surface.get_width() / 2
        text_center_y = self.surface.get_height() / 2
        left_button_center_x = text_center_x - self._text_rect.width / 2 - self.button_padding - self.arrow_width
        right_button_center_x = text_center_x + self._text_rect.width / 2 + self.button_padding + self.arrow_width

        button_center_y = text_center_y
        arrow_color = self.style.fontcolor

        pygame.draw.polygon(self.surface, arrow_color, [
            (left_button_center_x - self.arrow_width, button_center_y),
            (left_button_center_x, button_center_y - self.arrow_width / 2),
            (left_button_center_x, button_center_y + self.arrow_width / 2)])
        pygame.draw.polygon(self.surface, arrow_color, [
            (right_button_center_x + self.arrow_width, button_center_y),
            (right_button_center_x, button_center_y - self.arrow_width / 2),
            (right_button_center_x, button_center_y + self.arrow_width / 2)])

        self.surface.blit(self._text_surface, self._text_rect)
        self._event_cycle(Event.RENDER)
        if self._is_changed:
            if self.animation_manager.anim_rotation:
                self.surface = pygame.transform.rotate(self.surface, self.animation_manager.anim_rotation)

class FileDialog(Button):
    def __init__(self, on_change_function, dialog,text, size, style = default_style, active = True, freedom=False, words_indent=False):
        super().__init__(None, text, size, style, active, False, freedom, words_indent)
        self.on_change_function = on_change_function
        self.dialog = dialog
        self.filepath = None
    def _open_filedialog(self):
        self.filepath = self.dialog()
        
        if self.on_change_function:
            self.on_change_function(self.filepath)
    def update(self,*args):
        super().update(*args)
        if not self.active: return
        if self.hovered and mouse.left_up:
                try: self._open_filedialog()
                except Exception as e:
                    print(e)
class RectCheckBox(Widget):
    def __init__(self, size:int, style: StyleManager = default_style,default=False, freedom=False,on_change_function=None):
        super().__init__([size,size], style,freedom)
        self._toogled = False
        self.function = on_change_function
        self.toogled = default 
    @property
    def toogled(self):
        return self._toogled
    @toogled.setter
    def toogled(self,value:bool):
        self._toogled = value
        if self.function: self.function(value)
        self._is_changed = True
    def draw(self):
        super().draw()
        if self._is_changed:
            if self._toogled:
                cooficient = 1.1
                size = self.size[0]/cooficient
                offset = (self.size[0]-size)/2
                pygame.draw.rect(self.surface,self.style.secondarycolor,[offset,offset,size,size],0,self.style.radius)
            self._is_changed = False
    def update(self,*args):
        super().update(*args)
        if not self.active: return
        if self.hovered and mouse.left_fdown:
            self.toogled = not self.toogled
            