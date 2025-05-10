import pygame
import copy
from .style import *
from .utils import *
from .window import Window
from .animations import *
from .widgets import *

class NevuInfo:
    VERSION = 0.02
    RELEASE = "Alpha"
    AUTHOR = "Golem bebrov"
    AUTHORMAIL = "bebrovgolem@gmail.com"
    

class Menu:

    def __init__(self,window:Window,size,style:StyleManager=default_style): 
        """
        Initializes a new instance of the Menu class.

        Parameters:
        window (Window): The window associated with the menu.
        size (list[int, int]): The size of the menu.
        style (Style, optional): The style of the menu. Defaults to default_style.
        """
        self.window = window
        self.window_surface = None
        self._resize_ratio = [1,1]
        
        self.size_original = size
        self.size = size
        
        self._coordinatesMW = [0,0]
        self.coordinates = [0,0]
        
        self.style = style
        self.cached_image = None
        self._changed = True
        self._global_changed = True
        
        self._update_surface()
        
        if not self.window:
            self.window_surface = self.window
            self.window = None
            return
        self.isrelativeplaced = False
        self.relx = None
        self.rely = None
        self.first_window_size = self.window.size
        self.first_size = size
        self.first_coordinates = [0,0]
        self.window.add_event(Event(Event.RESIZE,self._resize_with_ratio))
        self._layout = None
        self._enabled = True
        self._update_image()
        self._opened_menu = None
        if isinstance(self.style.bgcolor,Gradient):
            self.gradient_surf = pygame.Surface(self.size)
            self.style.bgcolor.apply_gradient(self.gradient_surf)
    @property
    def enabled(self) -> bool: return self._enabled
    @enabled.setter
    def enabled(self, value: bool): self._enabled = value
    @property
    def coordinatesMW(self) -> list[int,int]: return self._coordinatesMW
    @coordinatesMW.setter
    def coordinatesMW(self,coordinates:list[int,int]): self._coordinatesMW = [coordinates[0]*self._resize_ratio[0]+self.window._offset[0],coordinates[1]*self._resize_ratio[1]+self.window._offset[1]]
    def coordinatesMW_update(self): self.coordinatesMW = self.coordinates
    @property
    def opened(self):
        if self._opened_menu: return True
        return False
    def open(self,menu,style:Style=None,*args):
        """
        Opens a new menu and stores it in the Menu object.
        Args:
            menu (Menu): The menu to open.
            style (Style, optional): The style to apply to the menu. Defaults to None.
            *args: Additional menus to store and render.
        """
        self._opened_menu = menu
        self._args_menus_to_draw = []
        for item in args: self._args_menus_to_draw.append(item)
        if style: self._opened_menu.apply_style_to_all(style)
        self._opened_menu._resize_with_ratio(self._resize_ratio)
    def close(self):
        """
        Closes the currently opened menu and resets the opened Menu object. \n
        <b>Works only if inside this menu is opened another menu</b>
        """
        self._opened_menu = None
    def _update_surface(self):
        if self.style.radius > 0 or self.style.bgcolor==Color_Type.TRANSPARENT:self.surface = pygame.Surface([self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]],pygame.SRCALPHA|pygame.HWSURFACE | pygame.DOUBLEBUF)
        else: self.surface = pygame.Surface([self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]],pygame.HWSURFACE | pygame.DOUBLEBUF)
        if self.style.transparency: self.surface.set_alpha(self.style.transparency)
        else: self.surface.set_alpha(None)
    def resize(self,size:list[int,int]):
        self._changed = True
        self._resize_ratio = [size[0]/self.size_original[0],size[1]/self.size_original[1]]
        self.coordinatesMW_update()
        self._update_surface()
        
        if self._layout:self._layout.resize(self._resize_ratio)
        if self.style.transparency:self.surface.set_alpha(self.style.transparency)
        self._update_image()
        print(self._resize_ratio)

    def _resize_with_ratio(self,ratio:list[int,int]):
        self._changed = True
        self._resize_ratio = ratio
        self._update_surface()
        self.coordinatesMW_update()
        if self.style.transparency:self.surface.set_alpha(self.style.transparency)
        if self._layout:self._layout.resize(self._resize_ratio)
        self._update_image()
    @property
    def style(self) -> Style:
        return self._style()
    @style.setter
    def style(self,style:StyleManager):
        self._style = copy.copy(style)
        if isinstance(self._style, StyleManager):
            self._style.select(StyleType.STILL)
        self._update_image()
    def _update_image(self):
        if self.style.bgimage:
            self.cached_image = pygame.transform.scale(pygame.image.load(self.style.bgimage),((self.size[0])*self._resize_ratio[0],(self.size[1])*self._resize_ratio[1]))
        else:
            self.cached_image = None
    def apply_style_to_childs(self,style:Style):
        self._changed = True
        self.style = style
        if self._layout: self._layout.apply_style_to_childs(style)
    @property
    def layout(self):
        return self._layout
    @layout.setter
    def layout(self,layout):
        if layout._can_be_main_layout:
            layout.coordinates = (self.size[0]/2-layout.size[0]/2,self.size[1]/2-layout.size[1]/2)
            layout.connect_to_menu(self)
            self._layout = layout
        else: raise Exception("this Layout can't be main")
    def _set_layout_coordinates(self,layout):
        layout.coordinates = [self.size[0]/2-layout.size[0]/2,self.size[1]/2-layout.size[1]/2]
    def set_coordinates(self,x:int,y:int):
        """
        Set coordinates of the menu. If the menu is set to open at the start of the program, the first coordinates are saved and used to open the menu at its first position.

        Parameters
        ----------
        x : int
            The x-coordinate of the menu.
        y : int
            The y-coordinate of the menu.
        """
    
        self.coordinates = [x,y]
        self.coordinatesMW_update()
        
        self.isrelativeplaced = False
        self.relx = None
        self.rely = None
        
        self.first_coordinates = self.coordinates
    def set_coordinates_relative(self,relx:int,rely:int):
        """
        Set coordinates of the menu relative to the window size. The coordinates are specified in percentages (from 0 to 100) and the menu is placed at the center of the window.

        Parameters
        ----------
        relx : int
            The x-coordinate of the menu in percentage of the window width.
        rely : int
            The y-coordinate of the menu in percentage of the window height.
        """
        self.coordinates = [(self.window.size[0]-self.window._crop_width_offset)/100*relx-self.size[0]/2,(self.window.size[1]-self.window._crop_height_offset)/100*rely-self.size[1]/2]
        self.coordinatesMW_update()
        self.isrelativeplaced = True
        self.relx = relx
        self.rely = rely
        self.first_coordinates = self.coordinates
    def draw(self):
        if not self.enabled: return
        self.surface.fill((0,0,0,0))
        rect_val = [self.coordinatesMW,self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]]
        if self._global_changed  or True:
            if not self.cached_image:
                if isinstance(self.style.bgcolor,Gradient):
                    if self._changed:
                        self._update_surface()
                        self.gradient_surf = pygame.Surface([self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]])
                        self.style.bgcolor.apply_gradient(self.gradient_surf)
                        print("generated Gradient")
                        self._changed = False
                    self.surface.blit(self.gradient_surf,[0,0])
                elif self.style.bgcolor == Color_Type.TRANSPARENT: self.surface.fill((0,0,0,0))
                else: self.surface.fill(self.style.bgcolor)
            else:
                self.surface.blit(self.cached_image,(0,0))
        self._layout.draw()
        if self.style.width > 0:
            pygame.draw.rect(self.surface,self.style.bordercolor,[0,0,rect_val[1],rect_val[2]],int(self.style.width*(self._resize_ratio[0]+self._resize_ratio[1])/2) if int(self.style.width*(self._resize_ratio[0]+self._resize_ratio[1])/2)>0 else 1,border_radius=int(self.style.radius*(self._resize_ratio[0]+self._resize_ratio[1])/2))
        if self.style.radius > 0:
            self.surface = RoundedSurface.create(self.surface,int(self.style.radius*(self._resize_ratio[0]+self._resize_ratio[1])/2))
        self.window.surface.blit(self.surface,rect_val[0])
        #Opened Menu
        if self._opened_menu:
            for item in self._args_menus_to_draw: item.draw()
            self._opened_menu.draw()
    def update(self):
        if not self.enabled: return
        if self._opened_menu:
            self._opened_menu.update()
            return
        if self._layout: self._layout.update()
        self._global_changed = self.layout._is_changed
    def get_rect(self)->pygame.Rect:
        """
        Returns a pygame.Rect representing the Menu's position and size in window coordinates.

        Returns:
            pygame.Rect: a pygame.Rect representing the Menu's position and size in window coordinates
        """
        return pygame.Rect(self.coordinatesMW[0],self.coordinatesMW[1],self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1])
    @opened.setter
    def opened(self, value:bool): self._opened = value
class DropDownMenu(Menu):
    @property
    def opened(self): return self._opened
    @opened.setter
    def opened(self,value:bool):
        self._opened = value
    def __init__(self, window:Window, size:list[int,int], style:Style=default_style,side:Align=Align.TOP,opened:bool=False,button_size:list[int,int]=None):
        super().__init__(window, size, style)
        self.side = side
        if not button_size:
            sz =[self.size[0]/3,self.size[0]/3]
        else:
            sz = button_size
        self.button = Button(self.toogle_self,"",sz,self.style)
        self.button.add_event(Event(Event.RENDER,lambda:self.draw_arrow(self.button.surface,self.style.bordercolor)))
        self.opened = opened
        self.transitioning = False
        self.animation_manager = AnimationManager()
        if self.side == Align.TOP:
            end = [self.coordinates[0],self.coordinates[1]-self.size[1]]
        elif self.side == Align.BOTTOM:
            end = [self.coordinates[0],self.coordinates[1]+self.size[1]]
        elif self.side == Align.LEFT:
            end = [self.coordinates[0]-self.size[0],self.coordinates[1]]
        elif self.side == Align.RIGHT:
            end = [self.coordinates[0]+self.size[0],self.coordinates[1]]
        self.end = end
        self.animation_speed = 1
    def draw_arrow(self, surface:pygame.Surface, color:list[int,int,int]|list[int,int,int,int], padding:int=1.1):
        surf_width = surface.get_width()
        surf_height = surface.get_height()
        arrow_width = surf_width / padding
        arrow_height = surf_height / padding
        margin_w = (surf_width - arrow_width) / 2
        margin_h = (surf_height - arrow_height) / 2
        left = margin_w
        top = margin_h
        right = margin_w + arrow_width
        bottom = margin_h + arrow_height
        center_x = margin_w + arrow_width / 2
        center_y = margin_h + arrow_height / 2
        points = None
        if self.side == Align.TOP:
            if self.opened: points = [(left, bottom), (center_x, top), (right, bottom)]
            else: points = [(left, top), (center_x, bottom), (right, top)]
        elif self.side == Align.BOTTOM:
            if self.opened: points = [(left, top), (center_x, bottom), (right, top)]
            else: points = [(left, bottom), (center_x, top), (right, bottom)]
        elif self.side == Align.LEFT:
            if self.opened: points = [(right, top), (left, center_y), (right, bottom)]
            else: points = [(left, top), (right, center_y), (left, bottom)]
        elif self.side == Align.RIGHT:
            if self.opened: points = [(left, top), (right, center_y), (left, bottom)]
            else: points = [(right, top), (left, center_y), (right, bottom)]

        if points:
            pygame.draw.polygon(surface, color, points)
        self.button._is_changed = True
    def toogle_self(self):
        print("toogled")
        if self.transitioning: return
        self.animation_manager = AnimationManager()
        if self.opened:
            self.opened = False
            if self.side == Align.TOP:
                end = [self.coordinatesMW[0],self.coordinatesMW[1]-self.size[1]]
            elif self.side == Align.BOTTOM:
                end = [self.coordinatesMW[0],self.coordinatesMW[1]+self.size[1]]
            elif self.side == Align.LEFT:
                end = [self.coordinatesMW[0]-self.size[0],self.coordinatesMW[1]]
            elif self.side == Align.RIGHT:
                end = [self.coordinatesMW[0]+self.size[0],self.coordinatesMW[1]]
            self.end = end
            anim_transitioning = AnimationEaseInOut(0.5*self.animation_speed,self.coordinatesMW,end,AnimationType.POSITION)
            anim_opac = AnimationLinear(0.25*self.animation_speed,255,0,AnimationType.OPACITY)
            self.animation_manager.add_start_animation(anim_transitioning)
            self.animation_manager.add_start_animation(anim_opac)
            self.transitioning = True
        else:
            self.opened = True
            if self.side == Align.TOP:
                start = [self.coordinatesMW[0],self.coordinatesMW[1]-self.size[1]]
            elif self.side == Align.BOTTOM:
                start = [self.coordinatesMW[0],self.coordinatesMW[1]+self.size[1]]
            elif self.side == Align.LEFT:
                start = [self.coordinatesMW[0]-self.size[0],self.coordinatesMW[1]]
            elif self.side == Align.RIGHT:
                start = [self.coordinatesMW[0]+self.size[0],self.coordinatesMW[1]]
            anim_transitioning = AnimationEaseInOut(0.5*self.animation_speed,start,self.coordinatesMW,AnimationType.POSITION)
            anim_opac = AnimationLinear(0.5*self.animation_speed,0,255,AnimationType.OPACITY)
            self.animation_manager.add_start_animation(anim_transitioning)
            self.animation_manager.add_start_animation(anim_opac)
            self.transitioning = True
        self.animation_manager.update()

    def draw(self):
        customval = [0,0]
        if self.animation_manager.anim_opacity:
            self.surface.set_alpha(self.animation_manager.anim_opacity)
        if self.transitioning:
            customval = self.animation_manager.anim_position
            rect_val = [customval,self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]]
        elif self.opened:
            rect_val = [self.coordinatesMW,self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]]
        else:
            rect_val = [self.end,self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]]
            self.button.draw()
            self.window.surface.blit(self.button.surface,self.button.coordinates)
            return
        self.surface.fill(self.style.bgcolor)
        self._layout.draw()
        if self.style.width > 0:
            pygame.draw.rect(self.surface,self.style.bordercolor,[0,0,rect_val[1],rect_val[2]],int(self.style.width*(self._resize_ratio[0]+self._resize_ratio[1])/2) if int(self.style.width*(self._resize_ratio[0]+self._resize_ratio[1])/2)>0 else 1,border_radius=int(self.style.radius*(self._resize_ratio[0]+self._resize_ratio[1])/2))
        if self.style.radius > 0:
            self.surface = RoundedSurface.create(self.surface,int(self.style.radius*(self._resize_ratio[0]+self._resize_ratio[1])/2))
        if rect_val[0]:
            self.window.surface.blit(self.surface,[int(rect_val[0][0]),int(rect_val[0][1])])
        self.button.draw()

        self.window.surface.blit(self.button.surface,self.button.coordinates)
    def update(self):
        self.animation_manager.update()
        if not self.animation_manager.start and self.transitioning:
            self.transitioning = False
        if self.transitioning:
            if self.animation_manager.anim_position:
                bcoords = self.animation_manager.anim_position
            else:
                bcoords = [-999,-999]
        elif self.opened:
            bcoords = self.coordinatesMW
        else:
            bcoords = self.end
        if self.side == Align.TOP:
            coords = [bcoords[0] + self.size[0] / 2-self.button.size[0]/2, bcoords[1] + self.size[1]]
        elif self.side == Align.BOTTOM:
            coords = [bcoords[0] + self.size[0] / 2-self.button.size[0]/2, bcoords[1]-self.button.size[1]]
        elif self.side == Align.LEFT:
            coords = [bcoords[0] + self.size[0], bcoords[1] + self.size[1] / 2-self.button.size[1]/2]
        elif self.side == Align.RIGHT:
            coords = [bcoords[0]-self.button.size[0], bcoords[1] + self.size[1] / 2-self.button.size[1]/2]
        self.button.coordinates = coords
        self.button.master_coordinates = self.button.coordinates
        #print(self.button.master_coordinates,mouse.pos)
        self.button.update()
        if self.opened:
            super().update()
        
class ContextMenu(Menu):
    _opened_context = False
    def __init__(self, window, size, style = default_style):
        super().__init__(window, size, style)
        self._close_context()
    def _open_context(self,coordinates):
        self.set_coordinates(coordinates[0]-self.window._crop_width_offset,coordinates[1]-self.window._crop_width_offset)
        self._opened_context = True
    def apply(self):
        self.window._selected_context_menu = self
    def _close_context(self):
        self._opened_context = False
        self.set_coordinates(-self.size[0],-self.size[1])
    def draw(self):
        if self._opened_context: super().draw()
    def update(self):
        if self._opened_context: super().update()
class Group():
    def __init__(self,items=[]):
        self.items = items
        self._enabled = True
        self._opened_menu = None
        self._args_menus_to_draw = []
        self._resize_ratio = [0,0]
    def update(self):
        if not self._enabled:
            return
        if self._opened_menu:
            self._opened_menu.update()
            return
        for item in self.items:
            item.update()
    def draw(self):
        if not self._enabled:
            return
        for item in self.items:
            item.draw()
        if self._opened_menu:
            for item2 in self._args_menus_to_draw:
                item2.draw()
            self._opened_menu.draw()
    def step(self):
        if not self._enabled:
            return
        for item in self.items:
            item.update()
            item.draw()
    @property
    def opened(self):
        if self._opened_menu: return True
        return False
    def enable(self):
        self._enabled = True
    def disable(self):
        self._enabled = False
    def toogle(self):
        self._enabled = not self._enabled
    def open(self,menu,style:Style=None,*args):
        self._opened_menu = menu
        self._args_menus_to_draw = []
        for item in args:
            self._args_menus_to_draw.append(item)
        if style:
            self._opened_menu.apply_style_to_all(style)
        #self._opened_menu._resize_with_ratio(self._resize_ratio)
    def close(self):
        self._opened_menu = None