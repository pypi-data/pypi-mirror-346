import pygame
import copy
import os
#import numba
from .color import Color_Type, Color

class Flow:
    NOFLOW = 0
    FLOW = 1

import numpy as np

class Gradient:
    # Константы направлений остаются без изменений
    TO_RIGHT = 'to right'
    TO_LEFT = 'to left'
    TO_TOP = 'to top'
    TO_BOTTOM = 'to bottom'
    TO_TOP_RIGHT = 'to top right'
    TO_TOP_LEFT = 'to top left'
    TO_BOTTOM_RIGHT = 'to bottom right'
    TO_BOTTOM_LEFT = 'to bottom left'

    CENTER = 'center'
    TOP_CENTER = 'top center'
    TOP_LEFT = 'top left'
    TOP_RIGHT = 'top right'
    BOTTOM_CENTER = 'bottom center'
    BOTTOM_LEFT = 'bottom left'
    BOTTOM_RIGHT = 'bottom right'

    def __init__(self, colors, type='linear', direction=TO_RIGHT, transparency=None):
        self.colors = self._validate_colors(colors)
        self.type = type
        self.direction = direction
        self._validate_type_direction()
        self.transparency = transparency

    def _validate_type_direction(self):
        linear_directions = [
            Gradient.TO_RIGHT, Gradient.TO_LEFT, Gradient.TO_TOP, Gradient.TO_BOTTOM,
            Gradient.TO_TOP_RIGHT, Gradient.TO_TOP_LEFT, Gradient.TO_BOTTOM_RIGHT, Gradient.TO_BOTTOM_LEFT
        ]
        radial_directions = [
            Gradient.CENTER, Gradient.TOP_CENTER, Gradient.TOP_LEFT, Gradient.TOP_RIGHT,
            Gradient.BOTTOM_CENTER, Gradient.BOTTOM_LEFT, Gradient.BOTTOM_RIGHT
        ]
        if self.type not in ['linear', 'radial']:
            raise ValueError(f"Gradient type '{self.type}' is not supported. Choose 'linear' or 'radial'.")
        if self.type == 'linear':
            if self.direction not in linear_directions and not (isinstance(self.direction, str) and self.direction.endswith('deg')):
                raise ValueError(f"Linear gradient direction '{self.direction}' is not supported.")
        elif self.type == 'radial':
            if self.direction not in radial_directions:
                raise ValueError(f"Radial gradient direction '{self.direction}' is not supported.")

    def with_transparency(self, transparency):
        return Gradient(self.colors, self.type, self.direction, transparency)

    def apply_gradient(self, surface):

        had_srcalpha = bool(surface.get_flags() & pygame.SRCALPHA)

        if self.type == 'linear':
            surface = self._apply_linear_gradient(surface, pygame) 
        elif self.type == 'radial':
            surface = self._apply_radial_gradient(surface, pygame) 

        if had_srcalpha:
            alpha_array = pygame.surfarray.pixels_alpha(surface)
            alpha_array[:] = 255 
            del alpha_array
        
        if self.transparency is not None:
            surface.set_alpha(self.transparency) 
        return surface

    def _apply_linear_gradient(self, surface, pygame_module):
        width, height = surface.get_size()
        if len(self.colors) < 2:
            raise ValueError("Градиент должен содержать как минимум два цвета.")
        
        steps = 256
        precomputed_colors_np = np.array(
            [self._get_color_at_progress(i / (steps - 1)) for i in range(steps)],
            dtype=np.uint8
        )
        
        array = pygame_module.surfarray.pixels3d(surface)
        
        if self.direction in [Gradient.TO_BOTTOM, Gradient.TO_TOP]:
            if height > 0:
                if height > 1:
                    progress_y = np.linspace(0, 1, height, endpoint=True)
                else:
                    progress_y = np.array([0.0])

                if self.direction == Gradient.TO_TOP:
                    progress_y = 1 - progress_y
                
                indices = np.clip((progress_y * (steps - 1)), 0, steps - 1).astype(int)
                colors_for_rows = precomputed_colors_np[indices]
                array[:, :, :] = colors_for_rows[np.newaxis, :, :]

        elif self.direction in [Gradient.TO_RIGHT, Gradient.TO_LEFT]:
            if width > 0:
                if width > 1:
                    progress_x = np.linspace(0, 1, width, endpoint=True)
                else:
                    progress_x = np.array([0.0])

                if self.direction == Gradient.TO_LEFT:
                    progress_x = 1 - progress_x

                indices = np.clip((progress_x * (steps - 1)), 0, steps - 1).astype(int)
                colors_for_cols = precomputed_colors_np[indices]
                array[:, :, :] = colors_for_cols[:, np.newaxis, :]
            
        elif self.direction in [Gradient.TO_BOTTOM_RIGHT, Gradient.TO_TOP_LEFT, Gradient.TO_BOTTOM_LEFT, Gradient.TO_TOP_RIGHT]:
            if width > 0 and height > 0:
                x_coords_vec = np.arange(width)
                y_coords_vec = np.arange(height)
                xx, yy = np.meshgrid(x_coords_vec, y_coords_vec, indexing='ij')

                diag_w = float(width - 1)
                diag_h = float(height - 1)
                
                diag_length_sq = diag_w**2 + diag_h**2
                progress = np.zeros_like(xx, dtype=float)

                if diag_length_sq > 0:
                    diag_length = np.sqrt(diag_length_sq)
                    norm_factor = 2 * diag_length # Using the normalization from original _get_progress
                    if norm_factor > 0:
                        if self.direction == Gradient.TO_BOTTOM_RIGHT:
                            progress = (xx + yy) / norm_factor
                        elif self.direction == Gradient.TO_TOP_LEFT:
                            progress = (diag_w - xx + diag_h - yy) / norm_factor
                        elif self.direction == Gradient.TO_BOTTOM_LEFT:
                            progress = (diag_w - xx + yy) / norm_factor
                        elif self.direction == Gradient.TO_TOP_RIGHT:
                            progress = (xx + diag_h - yy) / norm_factor
                
                indices = np.clip((progress * (steps - 1)), 0, steps - 1).astype(int)
                array[:, :, :] = precomputed_colors_np[indices]
        
        del array
        return surface

    def _get_progress(self, x, y, width, height):
        """Вычисляет прогресс для диагональных направлений."""
        if self.direction == Gradient.TO_BOTTOM_RIGHT:
            diag_length = ((width - 1)**2 + (height - 1)**2)**0.5
            return (x + y) / (2 * diag_length) if diag_length else 0
        elif self.direction == Gradient.TO_TOP_LEFT:
            diag_length = ((width - 1)**2 + (height - 1)**2)**0.5
            return ((width - 1 - x) + (height - 1 - y)) / (2 * diag_length) if diag_length else 0
        elif self.direction == Gradient.TO_BOTTOM_LEFT:
            diag_length = ((width - 1)**2 + (height - 1)**2)**0.5
            return ((width - 1 - x) + y) / (2 * diag_length) if diag_length else 0
        elif self.direction == Gradient.TO_TOP_RIGHT:
            diag_length = ((width - 1)**2 + (height - 1)**2)**0.5
            return (x + (height - 1 - y)) / (2 * diag_length) if diag_length else 0
        else:
            raise ValueError(f"Неподдерживаемое направление градиента: {self.direction}")

    def _get_color_at_progress(self, progress):
        if len(self.colors) == 1:
            return self.colors[0]
        
        num_segments = len(self.colors) - 1
        segment = progress * num_segments
        index = int(segment)
        
        if index >= num_segments:
            return self.colors[-1]
        
        local_progress = segment - index
        color1 = self.colors[index]
        color2 = self.colors[index + 1]
        return self._interpolate_color(color1, color2, local_progress)

    def _get_radial_center(self, width, height):
        if self.direction == Gradient.CENTER:
            return (width // 2, height // 2)
        elif self.direction == Gradient.TOP_CENTER:
            return (width // 2, 0)
        elif self.direction == Gradient.TOP_LEFT:
            return (0, 0)
        elif self.direction == Gradient.TOP_RIGHT:
            return (width - 1, 0)
        elif self.direction == Gradient.BOTTOM_CENTER:
            return (width // 2, height - 1)
        elif self.direction == Gradient.BOTTOM_LEFT:
            return (0, height - 1)
        elif self.direction == Gradient.BOTTOM_RIGHT:
            return (width - 1, height - 1)
        else:
            raise ValueError(f"Unsupported radial direction: {self.direction}")

    def _apply_radial_gradient(self, surface, pygame_module):
        width, height = surface.get_size()
        if width == 0 or height == 0:
            return surface

        steps = 256
        precomputed_colors_np = np.array(
            [self._get_color_at_progress(i / (steps - 1)) for i in range(steps)],
            dtype=np.uint8
        )
        
        center_x, center_y = self._get_radial_center(width, height)
        
        corners = np.array([(0, 0), (width - 1, 0), (width - 1, height - 1), (0, height - 1)], dtype=float)
        center_coords = np.array([float(center_x), float(center_y)])
        
        if width == 1 and height == 1:
             max_radius = 0.0
        else:
             distances_to_corners_sq = np.sum((corners - center_coords)**2, axis=1)
             max_radius = np.sqrt(np.max(distances_to_corners_sq))

        if max_radius == 0:
            # self.colors[0] is guaranteed to exist if _validate_colors ensures non-empty
            # and precomputed_colors_np[0] will be that color.
            surface.fill(tuple(precomputed_colors_np[0]))
            return surface

        array = pygame_module.surfarray.pixels3d(surface)

        x_coords_vec = np.arange(width)
        y_coords_vec = np.arange(height)
        xx, yy = np.meshgrid(x_coords_vec, y_coords_vec, indexing='ij')

        distance_sq = (xx - center_x)**2 + (yy - center_y)**2
        distance = np.sqrt(distance_sq)
        
        progress = np.minimum(distance / max_radius, 1.0)
        
        indices = np.clip((progress * (steps - 1)), 0, steps - 1).astype(int)
        
        array[:, :, :] = precomputed_colors_np[indices]
        
        del array
        return surface

    def _validate_colors(self, colors):
        if not isinstance(colors, (list, tuple)):
            raise ValueError("Цвета градиента должны быть списком или кортежем.")

        validated_colors = []
        for color in colors:
            if isinstance(color, str):
                # Предполагается, что класс Color существует и доступен.
                # Для запуска этого кода автономно, определите класс Color 
                # или убедитесь, что он импортирован.
                # color_tuple = getattr(Color, color.upper(), None)
                # Временно для автономности (если класс Color не определен):
                try:
                    # Попытка получить доступ к Color, как в оригинальном коде
                    color_tuple = getattr(Color, color.upper(), None) # type: ignore 
                except NameError:
                    raise NameError("Класс 'Color' не определен. Он необходим для обработки строковых названий цветов.")

                if color_tuple and isinstance(color_tuple, tuple) and len(color_tuple) == 3:
                    validated_colors.append(color_tuple)
                else:
                    raise ValueError(f"Неподдерживаемое название цвета: '{color}'. Используйте кортеж RGB или имя цвета из класса Color.")
            elif isinstance(color, (tuple, list)) and len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color):
                validated_colors.append(tuple(color))
            else:
                raise ValueError("Каждый цвет должен быть кортежем из 3 целых чисел (RGB) или допустимым названием цвета.")
        if not validated_colors:
            raise ValueError("Список цветов не может быть пустым.")
        return validated_colors

    def _interpolate_color(self, color1, color2, progress):
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        r = int(r1 + (r2 - r1) * progress)
        g = int(g1 + (g2 - g1) * progress)
        b = int(b1 + (b2 - b1) * progress)
        return (r, g, b)

    def invert(self, new_direction=None):
        if new_direction is None:
            if self.type == 'linear':
                if isinstance(self.direction, str) and self.direction.endswith('deg'):
                    try:
                        angle = int(self.direction[:-3])
                    except ValueError:
                        raise ValueError("Некорректный формат угла.")
                    new_angle = (angle + 180) % 360
                    new_direction = f"{new_angle}deg"
                else:
                    mapping = {
                        Gradient.TO_RIGHT: Gradient.TO_LEFT,
                        Gradient.TO_LEFT: Gradient.TO_RIGHT,
                        Gradient.TO_TOP: Gradient.TO_BOTTOM,
                        Gradient.TO_BOTTOM: Gradient.TO_TOP,
                        Gradient.TO_TOP_RIGHT: Gradient.TO_BOTTOM_LEFT,
                        Gradient.TO_BOTTOM_LEFT: Gradient.TO_TOP_RIGHT,
                        Gradient.TO_TOP_LEFT: Gradient.TO_BOTTOM_RIGHT,
                        Gradient.TO_BOTTOM_RIGHT: Gradient.TO_TOP_LEFT
                    }
                    new_direction = mapping.get(self.direction)
                    if new_direction is None:
                        raise ValueError(f"Не поддерживается инвертирование направления: {self.direction}")
            elif self.type == 'radial':
                mapping = {
                    Gradient.CENTER: Gradient.CENTER,
                    Gradient.TOP_CENTER: Gradient.BOTTOM_CENTER,
                    Gradient.BOTTOM_CENTER: Gradient.TOP_CENTER,
                    Gradient.TOP_LEFT: Gradient.BOTTOM_RIGHT,
                    Gradient.BOTTOM_RIGHT: Gradient.TOP_LEFT,
                    Gradient.TOP_RIGHT: Gradient.BOTTOM_LEFT,
                    Gradient.BOTTOM_LEFT: Gradient.TOP_RIGHT
                }
                new_direction = mapping.get(self.direction)
                if new_direction is None:
                    raise ValueError(f"Не поддерживается инвертирование направления: {self.direction}")
        return Gradient(self.colors, self.type, new_direction)
class Align():
    CENTER = 101010
    LEFT = 111111
    RIGHT = 121212
    TOP = 123122
    BOTTOM = 233121

class ParseError(ValueError):
    def __init__(self, message = ""):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return rf"Error happened through parsing of Style: {self.message}" if self.message.strip() != "" else "Unknown Error happened through parsing of Style!"


class Style:
    def __init__(self, raise_errors: bool = True, **style_params):
        self.__kwargs = style_params
        self.__raise_errors = raise_errors

        self.bgcolor = (120,120,120)
        self.bordercolor = (0,0,0)
        self.fontcolor = (60,60,60)
        self.secondarycolor = (120,30,30)

        self.fontname = None
        self.fontsize = 16

        self.textalign_x = Align.CENTER
        self.textalign_y = Align.CENTER

        self.bgimage = None

        self.width = 1
        self.radius = 0
        self.margin = 0
        self.padding = 0
        self.transparency = None

        self._init_parse_dict()
        self.main_parsing(style_params, raise_errors)
    def _init_parse_dict(self):
        bgcolorbase = [self.parse_color_gradient, "bgcolor", "Invalid Bgcolor set!"]
        bdcolorbase = [self.parse_color_gradient, "bordercolor", "Invalid Bordercolor set!"]
        fontcolorbase = [self.parse_color, "fontcolor", "Invalid Fontcolor set!"]
        fontnamebase = [self.parse_string, "fontname", "Invalid Fontname set!"]
        fontsizebase = [self.parse_int, "fontsize", "Invalid Fontsize set!"]
        widthbase = [self.parse_int, "width", "Invalid Width set!"]
        radbase = [self.parse_int, "radius", "Invalid Radius set!"]
        margbase = [self.parse_int, "margin", "Invalid Margin set!"]
        paddingbase = [self.parse_int, "padding", "Invalid Padding set!"]
        scolorbase = [self.parse_color, "secondarycolor", "Invalid Secondarycolor set!"]
        bgimagebase = [self.parse_path, "bgimage", "Invalid Bgimage path!"]
        talignxbase = [self.parse_int, "textalign_x", "Invalid Text x align set!"]
        talignybase = [self.parse_int, "textalign_y", "Invalid Text y align set!"]
        transparencybase = [lambda value:self.parse_int(value, [0,255]), "transparency", "Invalid Transparency set!"]

        self.parse_dict = {
            "bgcolor": bgcolorbase,
            "backgroundcolor": bgcolorbase,

            "bdcolor": bdcolorbase,
            "bordercolor": bdcolorbase,

            "color": fontcolorbase,
            "fontcolor": fontcolorbase,
            "fncolor": fontcolorbase,

            "font": fontnamebase,
            "fontfamily": fontnamebase,
            "fontname": fontnamebase,

            "fsize": fontsizebase,
            "fontsize": fontsizebase,

            "width": widthbase,
            "borderwidth": widthbase,
            "thickness": widthbase,

            "borderradius": radbase,
            "radius": radbase,
            "rad": radbase,
            "r": radbase,

            "margin": margbase,
            "marg": margbase,
            "m": margbase,

            "padding": paddingbase,
            "pad": paddingbase,
            "p": paddingbase,

            "secondarycolor": scolorbase,
            "secolor": scolorbase,
            "scolor": scolorbase,

            "bgimage": bgimagebase,
            "bgimg": bgimagebase,
            "backgroundimage": bgimagebase,
            "backgroundimg": bgimagebase,
            "image": bgimagebase,
            "img": bgimagebase,

            "text_align_x": talignxbase,
            "textalign_x": talignxbase,
            "talign_x": talignxbase,

            "text_align_y": talignybase,
            "textalign_y": talignybase,
            "talign_y": talignybase,
            
            "transparency": transparencybase,
            "tr": transparencybase
        }

    def _raise_parse_error(self, text: str):
        raise ParseError(text)

    def main_parsing(self, style_params: dict, raise_error: bool = True):
        if raise_error: errorhandle = self._raise_parse_error
        else: errorhandle = print
        for param, value in style_params.items():
            param = param.lower()
            item = self.parse_dict.get(param, None)
            if item:
                condition = item[0]
                attr = item[1]
                errormessage = item[2]
                result = condition(value)
                if result == True:
                    setattr(self, attr, value)
                elif result:
                    setattr(self, attr, result)
                else: errorhandle(errormessage+f" ({value})")
            else:
                errorhandle(f"unsupported parameter - {param}.")

    def parse_string(self, value: str):
        return isinstance(value, str)

    def parse_color(self, value: tuple | list | int):
        if (not isinstance(value, (tuple, list)) or not (2 < len(value) < 5) or not all(isinstance(i, int) and (0 <= i <= 255) for i in value)) and not value == Color_Type.TRANSPARENT:
            if isinstance(value, str):
                color = Color.get_all_colors().get(value.upper())
                if color:
                    return color
            return False
        return True

    def parse_color_gradient(self, value: tuple | list | int | Gradient):
        result = self.parse_color(value)
        if result: return result
        elif isinstance(value, Gradient): return True
        return False

    def parse_path(self, value: str):
        try: return (isinstance(value, str) and value.strip() != "" and os.path.exists(value)) or value == None
        except: 
            if value != None: return False
            return True

    def parse_int(self, value: int, supported_range: list[int, int] = None):
        if supported_range:
            minimal = int(min(supported_range))
            maximal = int(max(supported_range))
            return isinstance(value, int) and minimal <= value <= maximal
        return isinstance(value, int)

    @property
    def initial_copy(self): return Style(self.__kwargs)

    @property
    def copy(self): return copy.deepcopy(self)

    def __call__(self, **additional_params):
        selfcopy = self.copy
        selfcopy.main_parsing(additional_params)
        return selfcopy

    def __str__(self):
        return ", ".join([f"{item}: {value}" for item, value in self.__kwargs.items()])

    def reset(self):
        self = Style(raise_errors = self.__raise_errors, **self.__kwargs)





class StyleType:
    STILL = "__Still"
    HOVER = "__Hover"
    CLICK = "__Click"


class StyleManager:
    def __init__(self, still_style: Style = None, hover_style:Style = None, click_style: Style = None, **additional_styles:list[str, Style]):
        self._style_dict = {}
        self._selected = StyleType.STILL
        if still_style: self.add(StyleType.STILL, still_style)
        else: self.add(StyleType.STILL, Style())
        if hover_style: self.add(StyleType.HOVER, hover_style)
        else: self.add(StyleType.HOVER, Style())
        if click_style: self.add(StyleType.CLICK, click_style)
        else: self.add(StyleType.CLICK, Style())
        for name, value in additional_styles.items():
            self.add(name, value)

    def add(self, name: str, style: Style):
        self._style_dict[name] = style

    def get(self, name: str):
        style = self._style_dict.get(name, default_style())
        return style
    def select(self, name: str):
        check = self._style_dict.get(name)
        if check: self._selected = name
    def change(self, **kwargs): #[Name: kwargs]
        for name, parameters in kwargs.items():
            item = self._style_dict.get(name)
            if item:
                item = item(**parameters)
                self._style_dict[name] = item
    def changed(self, **kwargs):
        selfcopy = copy.deepcopy(self)
        selfcopy.change(**kwargs)
        return selfcopy
    def change_with(self, name: str, **kwargs):
        style = self._style_dict.get(name)
        if style:
            style = style(**kwargs)
            self._style_dict[name] = style
    def changed_with(self, name: str, **kwargs):
        selfcopy = copy.deepcopy(self)
        selfcopy.change_with(name, **kwargs)
        return selfcopy
    def change_all(self, **kwargs):
        for name, item in self._style_dict.items():
            if item:
                it = item(**kwargs)
                self._style_dict[name] = it
    def changed_all(self, **kwargs):
        selfcopy = copy.deepcopy(self)
        selfcopy.change_all(**kwargs)
        return selfcopy
                
        
    def __call__(self): return self._style_dict.get(self._selected)
    
default_style_manager = StyleManager()
default_style = Style()
    
class Theme:
    DEFAULT = Style()
    FIRE = Style(bgcolor=Color.ORANGERED, fontcolor=Color.YELLOW, bordercolor=Color.RED)
    CRIMSON = Style(bgcolor=Color.MAROON, fontcolor=Color.WHITE, bordercolor=Color.RED) 
    ROSE = Style(bgcolor=Color.MISTYROSE, fontcolor=Color.MAROON, bordercolor=Color.PINK)
    DARK = Style(bgcolor=Color.DARKGRAY, fontcolor=Color.LIGHTGRAY, bordercolor=Color.LIGHTGRAY)
    LIGHT = Style(bgcolor=Color.LIGHTGRAY, fontcolor=Color.DARKGRAY, bordercolor=Color.DARKGRAY)
    CUSTOM = Style(bgcolor=Color.BEIGE, fontcolor=Color.MAROON, bordercolor=Color.MAROON)
    PASTEL = Style(bgcolor=Color.LAVENDERBLUSH, fontcolor=Color.PURPLE, bordercolor=Color.PINK)
    VIBRANT = Style(bgcolor=Color.CYAN, fontcolor=Color.MAGENTA, bordercolor=Color.YELLOW)
    NATURE = Style(bgcolor=Color.PALEGREEN, fontcolor=Color.BROWN, bordercolor=Color.OLIVE)
    RETRO = Style(bgcolor=Color.LIGHTYELLOW, fontcolor=Color.BLUE, bordercolor=Color.RED)
    MINIMALIST = Style(bgcolor=Color.WHITE, fontcolor=Color.BLACK, bordercolor=Color.SILVER, borderradius=50)
    FUTURISTIC = Style(bgcolor=Color.NAVY, fontcolor=Color.AQUA, bordercolor=Color.LIME)
    WARM = Style(bgcolor=Color.PEACHPUFF, fontcolor=Color.CHOCOLATE, bordercolor=Color.ORANGE)
    COOL = Style(bgcolor=Color.LAVENDER, fontcolor=Color.TEAL, bordercolor=Color.SILVERGRAY)
    MONOCHROME = Style(bgcolor=Color.LIGHTBLACK, fontcolor=Color.SILVER, bordercolor=Color.GRAY)
    GOLD = Style(bgcolor=Color.LIGHTYELLOW, fontcolor=Color.MAROON, bordercolor=Color.GOLD)
    DEEPBLUE = Style(bgcolor=Color.NAVY, fontcolor=Color.LIGHTGRAY, bordercolor=Color.BLUE)
    FORESTGREEN = Style(bgcolor=Color.OLIVE, fontcolor=Color.LIGHTYELLOW, bordercolor=Color.GREEN)
    SUNSETORANGE = Style(bgcolor=Color.ORANGERED, fontcolor=Color.LIGHTYELLOW, bordercolor=Color.ORANGE)
class xTheme():
    PASTEL_RAINBOW = Style(bgcolor=Gradient(colors=[(240, 224, 255), (132, 112, 255)], type='linear', direction=Gradient.TO_BOTTOM), fontcolor=(255, 0, 255), bordercolor=(255, 192, 203))
    NEON = Style(bgcolor=Gradient(colors=[(0, 0, 0), (255, 0, 255)], type='linear', direction=Gradient.TO_BOTTOM), fontcolor=(255, 0, 255), bordercolor=(0, 255, 255),borderradius=10)
    OCEAN_BLUE = Style(bgcolor=Gradient(colors=[(240, 248, 255), (0, 70, 120)], type='linear', direction=Gradient.TO_BOTTOM), fontcolor=(0, 70, 120), bordercolor=(70, 130, 180)) 
    GRAYSCALE = Style(bgcolor=Gradient(colors=[(220, 220, 220), (80, 80, 80)], type='linear', direction=Gradient.TO_BOTTOM), fontcolor=(80, 80, 80), bordercolor=(150, 150, 150))
    SPRING = Style(bgcolor=Gradient(colors=[(245, 255, 245), (0, 100, 0)], type='linear', direction=Gradient.TO_BOTTOM), fontcolor=(0, 100, 0), bordercolor=(144, 238, 144)) 
    AUTUMN = Style(bgcolor=Gradient(colors=[(253, 245, 230), (160, 82, 45)], type='linear', direction=Gradient.TO_BOTTOM), fontcolor=(160, 82, 45), bordercolor=(255, 140, 0)) 
    WINTER = Style(bgcolor=Gradient(colors=[(248, 248, 255), (70, 130, 180)], type='linear', direction=Gradient.TO_BOTTOM), fontcolor=(70, 130, 180), bordercolor=(176, 196, 222)) 
    CYBERPUNK = Style(
        bgcolor=Gradient(colors=[(20, 20, 20), (50, 0, 60)],type='linear',direction=Gradient.TO_BOTTOM),
        fontcolor=(255, 0, 100),
        bordercolor=(0, 255, 200),
        borderradius=10,
        borderwidth=1,
        fontsize=22
    )
    MATERIAL_LIGHT = Style(
        bgcolor=(250, 250, 250),  
        fontcolor=(33, 33, 33),   
        bordercolor=(200, 200, 200), 
        borderradius=4,
        borderwidth=1,
        fontsize=20
    )
    
    MATERIAL_DARK = Style(
        bgcolor=(33, 33, 33),            
        fontcolor=(255, 255, 255),
        bordercolor=(60, 60, 60), 
        borderradius=2,
        borderwidth=1,
        fontsize=17
    )
    SUNSET = Style(
        bgcolor=Gradient(colors=[(255, 94, 77), (255, 195, 113)], type='linear', direction=Gradient.TO_BOTTOM),
        fontcolor=(255, 255, 255),
        bordercolor=(200, 100, 50),
        borderradius=10,
        borderwidth=2,
        fontsize=22
    )
    TROPICAL = Style(
        bgcolor=Gradient(colors=[(64, 224, 208), (32, 178, 170)], type='linear', direction=Gradient.TO_RIGHT),
        fontcolor=(10, 10, 10),
        bordercolor=(0, 128, 128),
        borderradius=5,
        borderwidth=2,
        fontsize=20
    )
    MYSTIC = Style(
        bgcolor=Gradient(colors=[(72, 61, 139), (123, 104, 238)], type='linear', direction=Gradient.TO_BOTTOM),
        fontcolor=(230, 230, 250),
        bordercolor=(75, 0, 130),
        borderradius=8,
        borderwidth=2,
        fontsize=21
    )
    VINTAGE = Style(
        bgcolor=Gradient(colors=[(222, 184, 135), (210, 180, 140)], type='linear', direction=Gradient.TO_RIGHT),
        fontcolor=(101, 67, 33),
        bordercolor=(160, 82, 45),
        borderradius=12,
        borderwidth=3,
        fontsize=20
    )
    AURORA = Style(
        bgcolor=Gradient(colors=[(0, 255, 255), (255, 0, 255), (0, 0, 139)], type='radial', direction=Gradient.CENTER),
        fontcolor=(255, 255, 255),
        bordercolor=(138, 43, 226),
        borderradius=15,
        borderwidth=3,
        fontsize=23
    )
    GALACTIC = Style(
        bgcolor=Gradient(colors=[(10, 10, 30), (30, 30, 60)], type='linear', direction=Gradient.TO_RIGHT),
        fontcolor=(57, 255, 20),
        bordercolor=(57, 100, 20),
        borderradius=8,
        borderwidth=1,
        fontsize=20
    )
    ELEGANT = Style(
        bgcolor=Gradient(colors=[(245, 245, 245), (220, 220, 220)], type='linear', direction=Gradient.TO_BOTTOM),
        fontcolor=(0, 0, 0),
        bordercolor=(211, 211, 211),
        borderradius=20,
        borderwidth=1,
        fontsize=22
    )
    DREAMY = Style(
        bgcolor=Gradient(colors=[(255, 182, 193), (255, 240, 245)], type='linear', direction=Gradient.TO_TOP),
        fontcolor=(199, 21, 133),
        bordercolor=(255, 105, 180),
        borderradius=15,
        borderwidth=2,
        fontsize=21
    )
    RED = Style(
        bgcolor=Gradient(
            colors=[(230, 50, 50), (255, 120, 80)], 
            type='linear',
            direction=Gradient.TO_BOTTOM
        ),
        fontcolor=(255, 255, 255),     
        bordercolor=(220, 20, 60),      
        borderradius=10,               
        borderwidth=2,
        fontsize=22
    )
