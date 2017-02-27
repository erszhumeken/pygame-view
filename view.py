# view module - convenience methods for pygame.display - CC0
# https://github.com/cosmologicon/pygame-view

from __future__ import division
import pygame, math

WINDOW_FLAGS = 0
FULLSCREEN_FLAGS = pygame.HWSURFACE | pygame.DOUBLEBUF

size0 = None
_height = None
_fullscreen = False
_forceres = False
_EMPTY_SENTINEL = ()
def set_mode(size0 = None, height = _EMPTY_SENTINEL, fullscreen = None, forceres = None):
	global _height, _fullscreen, _forceres
	if size0 is not None:
		_set_size0(size0)
	if height is not _EMPTY_SENTINEL:
		_height = height
	if fullscreen is not None:
		_fullscreen = fullscreen
	if forceres is not None:
		_forceres = forceres
	_update()

def _set_size0(r):
	global size0
	w, h = r
	size0 = int(w), int(h)

def toggle_fullscreen():
	set_mode(fullscreen = not _fullscreen)

def _update():
	if size0 is None:
		raise ValueError("view.size0 must be set")
	w0, h0 = size0
	if _forceres or not _fullscreen:
		w, h = size0 if _height is None else (int(round(w0 * _height / h0)), _height)
	else:
		w, h = _get_max_fullscreen_size(size0)
	flags = FULLSCREEN_FLAGS | pygame.FULLSCREEN if _fullscreen else WINDOW_FLAGS
	pygame.display.set_mode((w, h), flags)
	_setattrs()

def _get_max_fullscreen_size(size0):
	w0, h0 = size0
	modes = pygame.display.list_modes()
	if not modes:
		raise ValueError("No fullscreen display modes available.")
	# Being a little overly cautious here and not assuming that there's a single
	# aspect ratio that's at least as large as all the others in both dimensions.
	return max(
		min((w, int(round(w * h0 / w0))), (int(round(h * w0 / h0)), h))
		for w, h in modes
	)

def T(x, *args):
	if args:
		return [T(a) for a in (x,) + args]
	if isinstance(x, pygame.Rect):
		return pygame.Rect([T(a) for a in x])
	try:
		return [T(a) for a in x]
	except TypeError:
		return int((math.ceil if x > 0 else math.floor)(x * h / h0))

def _setattrs():
	global screen, rect, rect0
	rect0 = pygame.Rect((0, 0, size0[0], size0[1]))
	screen = pygame.display.get_surface()
	rect = screen.get_rect()
	rectattrs = ["x", "y", "top", "left", "bottom", "right",
		"topleft", "bottomleft", "topright", "bottomright",
		"midtop", "midleft", "midbottom", "midright",
		"center", "centerx", "centery", "size", "width", "height", "w", "h"]
	for attr in rectattrs:
		globals()[attr] = getattr(rect, attr)
		globals()[attr + "0"] = getattr(rect0, attr)

