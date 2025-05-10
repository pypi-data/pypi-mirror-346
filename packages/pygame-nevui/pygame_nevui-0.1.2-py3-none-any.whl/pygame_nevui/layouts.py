import pygame
import numpy as np
import copy
from .style import Style,Align,Color_Type,default_style,default_style_manager, StyleType
from .utils import Input_Type, InputType, mouse, time
from .widgets import Widget, NevuObject, Label, CheckBox, GifWidget, ImageWidget, Input
from .menu import Menu


class LayoutType(NevuObject):

    def __init__(self, size: list[int,int], style: Style =  default_style_manager):
        super().__init__(size, style)
        self.freedom_widgets = []
        self.widgets = []
        self._borders = False

        self.menu = None
        self.layout = None
        self.surface = None
        
        self.first_parent_menu = Menu(None,(100,100),default_style_manager)
        self.all_layouts_coords = [0,0]
        self._can_be_main_layout = True

        self.border_name = " "
    @property
    def borders(self):return self._borders
    @borders.setter
    def borders(self,bool:bool): self._borders = bool
    def set_self(self,layout): self = layout
    @property
    def border_name(self) -> str: return self.border_name
    @border_name.setter
    def border_name(self, name: str):
        self._border_name = name
        if self.first_parent_menu:
            try:
                self.border_font = pygame.sysfont.SysFont("Arial", int(self.first_parent_menu._style.fontsize*self._resize_ratio[1]))
                self.border_font_surface = self.border_font.render(self._border_name, True, (255,255,255))
            except: pass
    def resize(self,_resize_ratio):
        self._resize_ratio = _resize_ratio
        for widget in self.widgets:
            widget.resize(self._resize_ratio)
        for widget in self.freedom_widgets:
            widget.resize(self._resize_ratio)
        self.border_name = self._border_name
    def is_layout(self,item: Widget) -> bool:
        if isinstance(item,LayoutType): return True
        return False
    def _event_on_add_widget(self):
        pass
    def add_widget(self,widget:Widget):
        if isinstance(widget,LayoutType):widget.connect_to_layout(self)
        elif hasattr(widget,"_freedom"):
            if widget._freedom:self.freedom_widgets.append(widget)
            else:self.widgets.append(widget)
            return
        self.widgets.append(widget)
        self._can_change_widgets = [widget if hasattr(widget,"is_changed") else None for widget in self.widgets]
    def apply_style_to_childs(self,style:Style):
        for widget in self.widgets:
            if not hasattr(widget,"menu"): widget.style = style
            else: widget.apply_style_to_childs(style)
    def draw(self):
        if self.borders and hasattr(self, "border_font_surface"):
            chc = [1,1] if self.layout!=None else self._resize_ratio
            self.surface.blit(self.border_font_surface, [self.coordinates[0]*chc[0], self.coordinates[1]*chc[1]-self.border_font_surface.get_height()])
            pygame.draw.rect(self.surface,(255,255,255),[self.coordinates[0]*chc[0], self.coordinates[1]*chc[1],int(self.size[0]*self._resize_ratio[0]),int(self.size[1]*self._resize_ratio[1])],1)
        for widget in self.freedom_widgets:
            widget.draw()
            self.surface.blit(widget.surface,[int(widget.coordinates[0])*self._resize_ratio[0],int(widget.coordinates[1])*self._resize_ratio[1]])
    def update(self,*args):
        #print(self.all_layouts_coords)
        super().update()
        if self.menu:self.surface = self.menu.surface;self.all_layouts_coords = [0,0]
        elif self.layout:self.surface = self.layout.surface;self.all_layouts_coords = [self.layout.all_layouts_coords[0]+self.coordinates[0],self.layout.all_layouts_coords[1]+self.coordinates[1]];self.first_parent_menu = self.layout.first_parent_menu
        self._is_changed = any([widget._is_changed for widget in self.widgets+self.freedom_widgets])
        for widget in self.freedom_widgets:
            widget.master_coordinates = [widget.coordinates[0]+self.first_parent_menu.coordinatesMW[0],widget.coordinates[1]+self.first_parent_menu.coordinatesMW[1]]
            widget.update()
        self._update_anim_coordinates()
    def connect_to_menu(self,menu:Menu):
        self.menu = menu
        self.surface = self.menu.surface
        self.all_layouts_coords = [0,0]
        self.first_parent_menu = menu
        self.border_name = self._border_name
    def connect_to_layout(self,layout):
        print(self,"connected to",layout)
        self.surface = layout.surface
        self.layout = layout
        self.first_parent_menu = layout.first_parent_menu
        self.all_layouts_coords = [layout.all_layouts_coords[0]+layout.coordinates[0],layout.all_layouts_coords[1]+self.coordinates[1]+layout.coordinates[1]]
        self.border_name = self._border_name
    def get_widget(self,id:int):
        return self.widgets[id]
class Grid(LayoutType):
    def __init__(self, size: list[int,int], x: int = 1, y: int = 1):
        super().__init__(size)
        self.grid_x = x
        self.grid_y = y
        self.cell_height = self.size[1]/self.grid_y
        self.cell_width = self.size[0]/self.grid_x
    def resize(self, _resize_ratio:list[float,float]): super().resize(_resize_ratio)
    def update(self, *args):
        super().update()
        for widget in self.widgets:
            widget.coordinates = [self.coordinates[0]+self.relx(widget.x*self.cell_width)+ (self.relx(self.cell_width) - widget.size[0])/2+self.relx(widget._anim_coordinates[0]),
                                  self.coordinates[1]+self.rely(widget.y*self.cell_height)+(self.rely(self.cell_height) - widget.size[1])/2+self.rely(widget._anim_coordinates[1])]
            widget.master_coordinates = [widget.coordinates[0]+self.first_parent_menu.coordinatesMW[0],widget.coordinates[1]+self.first_parent_menu.coordinatesMW[1]]
            try:widget.update(self.first_parent_menu.window.last_events)
            except:widget.update([])
    def add_widget(self, widget: Widget, x: int, y: int):
        if x > self.grid_x or y > self.grid_y: raise Exception("Grid index out of range x:{x},y:{y}".format(x=x,y=y))
        elif x<1 or y<1: raise Exception("Grid index out of range x:{x},y:{y}".format(x=x,y=y))
        for _widget in self.widgets: 
            if _widget.x == x-1 and _widget.y == y-1: raise Exception("Grid index aready in use in x:{x},y:{y}".format(x=x,y=y))
        widget.x = x-1
        widget.y = y-1
        super().add_widget(widget)
        if self.layout: self.layout._event_on_add_widget()
    def draw(self):
        super().draw()
        for widget in self.widgets:
            widget.draw()
            if not self.is_layout(widget): self.surface.blit(widget.surface,[int(widget.coordinates[0]),int(widget.coordinates[1])])
    def get_row(self, x: int) -> list[Widget]:
        needed = []
        for widget in self.widgets:
            if widget.x == x: needed.append(widget)
        return needed
    def get_column(self, y: int) -> list[Widget]:
        needed = []
        for widget in self.widgets:
            if widget.y == y: needed.append(widget)
        return needed
    def get_widget(self, x: int, y: int) -> Widget:
        w = None
        for widget in self.widgets:
            if widget.x == x-1 and widget.y == y-1:
                w = widget
                return w
    def overwrite_widget(self, x: int, y: int, widget: Widget) -> bool:
        for _widget in self.widgets:
            if _widget.x == x-1 and _widget.y == y-1:
                self.widgets.remove(_widget)
                self.add_widget(widget,x,y)
                return True
        return False

class CheckBoxGrid(Grid):
    def __init__(self, size:list[int,int], x:int=1, y:int=1 ,multiple=False,named=False):
        super().__init__(size, x, y*2 if named else y)
        self._named = named
        self.selected = -1
        self.widgets_last_id = 0
        self.multiple = multiple
    def draw(self): 
        super().draw()
        for i in range(0,len(self.widgets)-1):
            widget = self.widgets[i]
            widget._is_changed = True
            if i == self.selected: widget.draw(True)
            if not hasattr(widget,"menu"):
                self.surface.blit(widget.surface,[int(widget.coordinates[0]),int(widget.coordinates[1])])
    def apply_style_to_childs(self, style:Style):
        for widget in self.widgets:
            if not hasattr(widget,"menu"):
                if isinstance(widget,CheckBox):
                    widget.style = style
            else: widget.apply_style_to_childs(style)
    def add_widget(self, widget:Widget, x:int, y:int,name:str=None):
        if not isinstance(widget,CheckBox):
            if name != "SYSTEM_NEEDS":raise Exception("Widget must be CheckBox")
            else:name = None
        if name:
            if self._named:
                self.add_widget(Label((self.cell_width*self._resize_ratio[0],300*self._resize_ratio[1]),name,default_style_manager(bgcolor=Color_Type.TRANSPARENT,bordercolor=Color_Type.TRANSPARENT)),x,y*2-1,name="SYSTEM_NEEDS")
                y*=2
        super().add_widget(widget, x, y)
        if hasattr(widget,"connect_to_dot_group"):
            widget.connect_to_dot_group(self,self.widgets_last_id)
            self.widgets_last_id += 1
            
    @property
    def active(self):
        m = []
        for dot in self.widgets:
            if isinstance(dot,CheckBox):
                if dot.is_active: m.append(dot)
        return m
    @active.setter
    def active(self, id: int) -> list[CheckBox]|CheckBox|None:
        if not self.multiple:
            for dot in self.widgets:
                if isinstance(dot,CheckBox): dot.is_active = False
        for dot in self.widgets:
            if isinstance(dot,CheckBox):
                if dot._id == id:
                    if self.multiple:
                        if not dot.is_active: dot.is_active = True
                        else: dot.is_active = False
                    else: dot.is_active = True
    @property
    def active_state(self) -> list[object]|object|None:
        m = []
        for dot in self.widgets:
            if isinstance(dot,CheckBox):
                if dot.is_active: m.append(dot.state)
        if len(m)>1: return m
        elif len(m) == 1: return m[0]
        else: return None
    @active_state.setter
    def active_state(self,value,id:int=None):
        for dot in self.widgets:
            if isinstance(dot,CheckBox):
                if dot.is_active:
                    if dot._id == id or id == None: dot.state = value
    @property
    def inactive(self) -> list[CheckBox]|CheckBox|None:
        m = []
        for dot in self.widgets:
            if not dot.is_active:
                if isinstance(dot,CheckBox): m.append(dot)
        if len(m)>1: return m
        elif len(m) == 1: return m[0]
        else: return None
    
    @property
    def inactive_state(self) -> list[object]|object|None:
        m = []
        for dot in self.widgets:
            if not dot.is_active:
                if isinstance(dot,CheckBox): m.append(dot.state)
        if len(m)>1: return m
        elif len(m) == 1: return m[0]
        else: return None

class ColorPickerGrid(Grid):
    def __init__(self, amount_of_colors: int = 3, item_size: int = 50, y_size: int = 50, margin:int = 0, title: str = "", 
                 color_widget_style: Style = default_style_manager, title_label_style: Style = default_style_manager, on_change_function=None):
        if amount_of_colors <= 0: raise Exception("Amount of colors must be greater than 0")
        if item_size <= 0: raise Exception("Item size must be greater than 0")
        if margin < 0: raise Exception("Margin must be greater or equal to 0")
        self._widget_line = 1
        if title.strip() != "": self._widget_line = 2
        self.size = (amount_of_colors*item_size+margin*(amount_of_colors-1), y_size*self._widget_line+margin*(self._widget_line-1))
        self.on_change_function = on_change_function  
        super().__init__(self.size,amount_of_colors,self._widget_line)
        for i in range(amount_of_colors): 
            self.add_widget(Input((item_size,y_size),color_widget_style(text_align_x=Align.CENTER),"","0",None,Input_Type.NUMBERS,on_change_function=self._return_colors,max_characters=3),i+1,self._widget_line)
        if self._widget_line == 2:
            if amount_of_colors % 2 == 0: offset = 0.5
            else: offset = 1
            self.label = Label((self.size[0],y_size),title,title_label_style(text_align_x=Align.CENTER))
            self.add_widget(self.label,amount_of_colors//2+offset,1)
    def _return_colors(self,*args):
        c = self.get_color()
        if self.on_change_function: self.on_change_function(c)
    def get_color(self) -> tuple:
        c = []
        for widget in self.widgets: 
            if isinstance(widget,Input): c.append(int(widget.text))
        return tuple(c)
    def set_color(self, color: tuple|list):
        for i in range(len(color)):
            if i == len(self.widgets): break
            self.widgets[i].text = str(color[i])
class Pages(LayoutType):
    def __init__(self, size: list|tuple):
        super().__init__(size)
        self.selected_page = None
        self.selected_page_id = 0
    def add_widget(self, widget: LayoutType):
        if not self.is_layout(widget): raise Exception("Widget must be Layout")
        super().add_widget(widget)
        if self.layout: self.layout._event_on_add_widget()
        if not self.selected_page:
            self.selected_page = widget
            self.selected_page_id = 0
    def draw(self):
        super().draw()
        pygame.draw.line(self.surface,(0,0,0),[self.coordinates[0]+self.relx(20),self.coordinates[1]+self.rely(20)],[self.coordinates[0]+self.relx(40),self.coordinates[1]+self.rely(20)],2)
        pygame.draw.line(self.surface,(0,0,0),[self.coordinates[0]+self.relx(20),self.coordinates[1]+self.rely(20)],[self.coordinates[0]+self.relx(20),self.coordinates[1]+self.rely(40)],2)
        
        self.widgets[self.selected_page_id].draw()
        for i in range(len(self.widgets)):
            if i != self.selected_page_id: pygame.draw.circle(self.surface,(0,0,0),[self.coordinates[0]+self.relx(20+i*20),self.coordinates[1]+self.rely(self.size[1]-10)],self.relm(5))
            else: pygame.draw.circle(self.surface,(255,0,0),[self.coordinates[0]+self.relx(20+i*20),self.coordinates[1]+self.rely(self.size[1]-10)],self.relm(5))
    def move_by_point(self, point: int):
        self.selected_page_id += point
        if self.selected_page_id < 0: self.selected_page_id = len(self.widgets)-1
        self.selected_page = self.widgets[self.selected_page_id]
        if self.selected_page_id >= len(self.widgets): self.selected_page_id = 0
        self.selected_page = self.widgets[self.selected_page_id]
    def update(self, *args):
        super().update()
        if mouse.left_fdown:
            rectleft = pygame.Rect(self.coordinates[0]+(self.first_parent_menu.coordinatesMW[0]),self.coordinates[1]+self.first_parent_menu.coordinatesMW[1],self.relx(self.size[0]/10),self.rely(self.size[1]))
            rectright = pygame.Rect(self.coordinates[0]+self.relx(self.size[0]-self.size[0]/10)+self.first_parent_menu.coordinatesMW[0],self.coordinates[1]+self.first_parent_menu.coordinatesMW[1],self.relx(self.size[0]/10),self.rely(self.size[1]))
            if rectleft.collidepoint(mouse.pos): self.move_by_point(-1)
            if rectright.collidepoint(mouse.pos): self.move_by_point(1)

        self.widgets[self.selected_page_id].coordinates = [self.coordinates[0]+self.relx(self.size[0]/2-self.widgets[self.selected_page_id].size[0]/2),
                                                           self.coordinates[1]+self.rely(self.size[1]/2-self.widgets[self.selected_page_id].size[1]/2),]
        self.widgets[self.selected_page_id].first_parent_menu = self.first_parent_menu
        self.widgets[self.selected_page_id].update()
    def get_selected(self): return self.widgets[self.selected_page_id]
class Gallery_Pages(Pages):
    def __init__(self, size: list|tuple):
        super().__init__(size)
    def add_widget(self, widget: Widget):
        if self.is_layout(widget): raise Exception("Widget must not be Layout, layout creates automatically")
        if isinstance(widget,ImageWidget) or isinstance(widget,GifWidget):
            g = Grid(self.size)
            g.add_widget(widget,1,1)
            super().add_widget(g)

class Infinite_Scroll(LayoutType):
    """
    Implements an infinite scrolling layout to display widgets that exceed the visible area.

    This layout allows for displaying a long list or a large number of widgets
    that do not fit within the given layout size by using scroll bars for navigation.

    It supports both vertical and horizontal scrolling (though horizontal scrolling
    might be less developed at the moment) and allows adding widgets
    with different alignment options.

    **Nested Class:**

    * `Scroll_Bar`:  The scroll bar widget that controls the visibility and position
                      of the scrollable area.

    **Key Features:**

    * **Infinite Scrolling:** Displays content exceeding layout bounds using scrollbars.
    * **Vertical and Horizontal Scrolling:** Supports scrolling in both directions.
    * **Widget Management:** Adding and managing widgets within the scrollable area.
    * **Widget Alignment:**  Allows aligning widgets to the left, center, or right.
    * **Interactivity:** Scroll control via mouse interaction.

    **Usage Example:**

    ```python
    # Example requires definitions for LayoutType, Widget, default_style_manager, Align and pygame

    # Creating an infinite scroll layout
    infinite_scroll_layout = Infinite_Scroll((300, 200))

    # Adding widgets
    # ... (Add widgets to infinite_scroll_layout) ...
    ```
    """
    class Scroll_Bar(Widget):
        def __init__(self, size: list|tuple, style: Style, minval:int, maxval: int, scrsizet:int, scrsizeb:int, t, master = None):
            super().__init__(size, style)
            self.minval = minval
            self.maxval = maxval
            self.percentage = 0
            self.scroll = False
            self.scroll_sizeT = scrsizet
            self.scroll_sizeB = scrsizeb
            self.type = t
            self.master = master
        def update(self,*args):
            if self.type == 1:rect = pygame.Rect(self.master_coordinates[0],self.scroll_sizeT,self.size[0]*self._resize_ratio[0],self.scroll_sizeB*self._resize_ratio[1])
            elif self.type == 2:rect = pygame.Rect(self.scroll_sizeT*self._resize_ratio[0],self.master_coordinates[1],self.scroll_sizeB*self._resize_ratio[0],self.size[1]*self._resize_ratio[1])
            if mouse.left_fdown:
                if rect.collidepoint(mouse.pos):self.scroll = True
                else:self.scroll = False
            if mouse.left_up:self.scroll = False
            if self.scroll:self.coordinates[1] = mouse.pos[1]-self.master_coordinates[1]+self.coordinates[1]
            try:self.percentage = self.coordinates[1]/(self.scroll_sizeB*self._resize_ratio[1])*100
            except:self.percentage = 0
            if self.percentage > 100:self.percentage = 100
            elif self.percentage < 0:self.percentage = 0
            if self.coordinates[1]<0:self.coordinates[1] = 0
            elif self.coordinates[1]>(self.scroll_sizeT+self.scroll_sizeB-self.size[1]*2)*self._resize_ratio[1]:self.coordinates[1] = (self.scroll_sizeT+self.scroll_sizeB-self.size[1]*2)*self._resize_ratio[1]
        
        def set_mv_mx_val(self, minval: int, maxval: int, scrsizet: int, scrsizeb: int):
            self.scroll_sizeT = scrsizet
            self.scroll_sizeB = scrsizeb
            self.minval = minval
            self.maxval = maxval
        def draw(self):
            super().draw()
    def __init__(self,size: list|tuple, draw_scrool_area:bool = False, scrollbar_style: Style = default_style_manager):
        super().__init__(size)
        self.scrollbar_style = scrollbar_style
        self.__init_scroll_bars__()
        self.max_x = 0
        self.max_y = 0
        self.padding = 30
        self.widgets_alignment = []
        self.original_size = copy.copy(self.size)
        self.actual_max_y = 1
        self.first_update_fuctions.append(self.__first_update_bars__)
        self.draw_scrool_area = draw_scrool_area
        
    def _event_on_add_widget(self):
        self.__init_scroll_bars__()
        self.__first_update_bars__()
        self.max_y = self.padding
        self.max_x = self.original_size[0] if self.original_size != self.size else self.size[0]
        for widget in self.widgets: self.max_y += self.rely(widget.size[1])+self.padding
        self.actual_max_y = self.max_y - self.rely(self.size[1])
    def __first_update_bars__(self):
        self.scroll_bar_y.set_mv_mx_val(self.coordinates[1],self.max_y,self.coordinates[1]+self.first_parent_menu.coordinatesMW[1],self.size[1])
        self.scroll_bar_x.set_mv_mx_val(self.coordinates[0]-self.max_x/2,self.coordinates[0]+self.max_x/2,self.coordinates[0]+self.first_parent_menu.coordinatesMW[0],self.size[0])
    def __init_scroll_bars__(self):
        self.scroll_bar_y = self.Scroll_Bar([self.size[0]/40,self.size[1]/20],default_style_manager.changed_with(StyleType.STILL,bgcolor=(100,100,100)),0,0,0,0,1,self)
        self.scroll_bar_y.style = self.scrollbar_style
        self.scroll_bar_x = self.Scroll_Bar([self.size[0]/20,self.size[1]/40],default_style_manager.changed_with(StyleType.STILL,bgcolor=(100,100,100)),0,0,0,0,2,self)
    def connect_to_layout(self, layout: LayoutType):
        super().connect_to_layout(layout)
        self.__init_scroll_bars__()
    def connect_to_menu(self, menu: Menu):
        super().connect_to_menu(menu)
        adjust = False
        if menu.size[0] < self.size[0]:
            self.size[0] = menu.size[0]
            adjust = True
        if menu.size[1] < self.size[1]:
            self.size[1] = menu.size[1]
            adjust = True
        if adjust:
            self.menu._set_layout_coordinates(self)
        self.__init_scroll_bars__()
        self.scroll_bar_y.style = menu.style
    def draw(self):
        for widget in self.widgets:
            if widget.coordinates[0]> self.coordinates[0]+self.size[0] or widget.coordinates[1]-widget.size[1] >self.coordinates[1]+self.size[1] or widget.coordinates[1]+widget.size[1]<self.coordinates[1]:
                continue
            widget.draw()
            if not self.is_layout(widget) and self.surface:
                self.surface.blit(widget.surface,[widget.coordinates[0],widget.coordinates[1]])
        if self.actual_max_y > 0:
            self.scroll_bar_y.draw()
            if self.surface: self.surface.blit(self.scroll_bar_y.surface,self.scroll_bar_y.coordinates)
        if self.original_size[0] != self.size[0] or True:
            self.scroll_bar_x.draw()
            if self.surface: self.surface.blit(self.scroll_bar_x.surface,self.scroll_bar_x.coordinates)
        super().draw()
    def update(self, *args):
        super().update()
        percentage = self.scroll_bar_y.percentage
        offset = self.actual_max_y/100*percentage
        ypad = self.padding
        for i in range(len(self.widgets)):
            widget = self.widgets[i]
            align = self.widgets_alignment[i]
            if align == Align.LEFT:
                new_x = self.coordinates[0] + self.relx(self.padding+widget._anim_coordinates[0])                          
            if align == Align.RIGHT:
                new_x = self.coordinates[0] + self.relx(self.size[0] - widget.size[0] + widget._anim_coordinates[0] - self.padding)
            if align == Align.CENTER:
                new_x = self.coordinates[0] + self.relx((self.size[0] / 2 - widget.size[0] / 2)+widget._anim_coordinates[0])  
            new_y = self.coordinates[1] + ypad - self.rely(offset + widget._anim_coordinates[1])
            widget.coordinates = [new_x, new_y]
            widget.master_coordinates = [widget.coordinates[0] + self.first_parent_menu.coordinatesMW[0] ,widget.coordinates[1] + self.first_parent_menu.coordinatesMW[1]]
            crd = widget.coordinates[1] + self.rely(offset)
            ypad = crd + self.rely(widget.size[1] - widget._anim_coordinates[1] + self.padding)
            if self.first_parent_menu.window: widget.update(self.first_parent_menu.window.last_events)
            else: widget.update([])
        if self.actual_max_y>0:
            self.scroll_bar_y.coordinates = np.array([self.coordinates[0]+(self.size[0]-self.scroll_bar_y.size[0])*self._resize_ratio[0], self.scroll_bar_y.coordinates[1]],dtype=np.float64)
            self.scroll_bar_y.master_coordinates = np.array([self.scroll_bar_y.coordinates[0]+self.first_parent_menu.coordinatesMW[0], self.scroll_bar_y.coordinates[1]+self.first_parent_menu.coordinatesMW[1]],dtype=np.float64)
            self.scroll_bar_y.update()
        if self.original_size[0] != self.size[0] or True:
            self.scroll_bar_x.coordinates = np.array([self.coordinates[0], self.scroll_bar_x.coordinates[1]+(self.size[1]-self.scroll_bar_x.size[1])*self._resize_ratio[1]],dtype=np.float64)
            self.scroll_bar_x.master_coordinates = np.array([self.scroll_bar_x.coordinates[0]+self.first_parent_menu.coordinatesMW[0], self.scroll_bar_x.coordinates[1]+self.first_parent_menu.coordinatesMW[1]],dtype=np.float64)
            self.scroll_bar_x.update()
    def resize(self, _resize_ratio: list):
        super().resize(_resize_ratio)
        self.scroll_bar_y.resize(_resize_ratio)
        self.scroll_bar_y.coordinates[1] = self.rely(self.scroll_bar_y.size[1])
    def add_widget(self, widget,alignment: Align = Align.LEFT):
        super().add_widget(widget)
        self.max_y = self.padding
        self.max_x = self.original_size[0] if self.original_size != self.size else self.size[0]
        for widget in self.widgets: 
            self.max_y += self.rely(widget.size[1])+self.padding
        self.actual_max_y = self.max_y - self.size[1]
        self.widgets_alignment.append(alignment)
        if self.layout: self.layout._event_on_add_widget()
    def clear(self):
        self.widgets.clear()
        self.widgets_alignment.clear()
        self.max_x = 0
        self.max_y = self.padding
        self.actual_max_y = 0
    def apply_style_to_childs(self, style:Style):
        super().apply_style_to_childs(style)
        self.scroll_bar_y.style = style
#print
class Appending_Layout_Type(LayoutType):
    def __init__(self, content: list[list] = [], style = default_style_manager):
        self._margin = 20
        super().__init__((self.margin,0),style)
        self.widgets_alignment = []
        self._can_be_main_layout = True
        if len(content) == 0: return
        for item in content:
            item,align = item
            self.add_widget(item,align)
    def add_widget(self, widget: Widget|LayoutType, alignment:Align = Align.CENTER):
        super().add_widget(widget)
        self.widgets_alignment.append(alignment)
        self._recalculate_size()
        if self.layout: self.layout._event_on_add_widget()
    def insert_widget(self, widget: Widget|LayoutType, id:int=-1):
        try:
            self.widgets.insert(id,widget)
            self.widgets_alignment.insert(id,Align.CENTER)
            self._recalculate_size()
            if self.layout: self.layout._event_on_add_widget()
        except Exception as e: raise e #TODO
    def connect_to_layout(self, layout :LayoutType):
        super().connect_to_layout(layout)
        self._recalculate_widget_coordinates()
    def connect_to_menu(self, menu: Menu):
        super().connect_to_menu(menu)
        self._recalculate_widget_coordinates() 
    def _event_on_add_widget(self):
        self._recalculate_size()
        if self.layout: self.layout._event_on_add_widget()
    def update(self, *args):
        super().update()
        self._recalculate_widget_coordinates()
        for widget in self.widgets:
            if self.first_parent_menu.window: widget.update(self.first_parent_menu.window.last_events)
            else: widget.update([])
    def draw(self):
        super().draw()
        for widget in self.widgets:
            widget.draw()
            if not self.is_layout(widget) and self.surface: self.surface.blit(widget.surface,[int(widget.coordinates[0]),int(widget.coordinates[1])])
    @property
    def margin(self): return self._margin
    @margin.setter
    def margin(self,val):
        self._margin = val
        self._recalculate_size()
        
class Appending_Layout_H(Appending_Layout_Type):
    def _recalculate_size(self):
        self.size[0] = sum(widget.size[0]+self._margin for widget in self.widgets) if len(self.widgets) > 0 else 0
        self.size[1] = max(x.size[1] for x in self.widgets) if len(self.widgets) > 0 else 0
    def _recalculate_widget_coordinates(self):
        m = self.relx(self.margin)
        current_x = 0 
        for i in range(len(self.widgets)):
            widget = self.widgets[i]
            alignment = self.widgets_alignment[i]
            widget_local_x = current_x + m/2
            widget.coordinates[0] = self.coordinates[0] + widget_local_x + self.relx(widget._anim_coordinates[0])
            if alignment == Align.CENTER:
                widget.coordinates[1] = self.coordinates[1] + self.rely(self.size[1] / 2 - widget.size[1] / 2 + widget._anim_coordinates[1])
            elif alignment == Align.LEFT:
                widget.coordinates[1] = self.coordinates[1]+ self.rely(widget._anim_coordinates[1])
            elif alignment == Align.RIGHT:
                widget.coordinates[1] = self.coordinates[1] + self.rely(self.size[1] - widget.size[1]+widget._anim_coordinates[1])
            widget.master_coordinates = [widget.coordinates[0]+self.first_parent_menu.coordinatesMW[0],widget.coordinates[1]+self.first_parent_menu.coordinatesMW[1]]
            current_x += self.relx(widget.size[0] + self.margin)

class Appending_Layout_V(Appending_Layout_Type):
    def _recalculate_size(self):
        self.size[1] = sum(widget.size[1]+self._margin for widget in self.widgets) if len(self.widgets) > 0 else 0
        self.size[0] = max(x.size[0] for x in self.widgets) if len(self.widgets) > 0 else 0
    def _recalculate_widget_coordinates(self):
        m = self.rely(self.margin)
        current_y = 0
        for i in range(len(self.widgets)):
            widget = self.widgets[i]
            alignment = self.widgets_alignment[i]
            widget_local_y = current_y + m 
            widget.coordinates[1] = self.coordinates[1] + widget_local_y+ self.rely(widget._anim_coordinates[1])
            if alignment == Align.CENTER:
                widget.coordinates[0] = self.coordinates[0] + self.relx(self.size[0] / 2 - widget.size[0] / 2+ widget._anim_coordinates[0])
            elif alignment == Align.LEFT:
                widget.coordinates[0] = self.coordinates[0]+ self.relx(widget._anim_coordinates[0])
            elif alignment == Align.RIGHT:
                widget.coordinates[0] = self.coordinates[0] + self.relx(self.size[0] - widget.size[0]+widget._anim_coordinates[0])
            widget.master_coordinates = [widget.coordinates[0]+self.first_parent_menu.coordinatesMW[0],widget.coordinates[1]+self.first_parent_menu.coordinatesMW[1]]
            current_y += self.rely(widget.size[1] + self.margin)