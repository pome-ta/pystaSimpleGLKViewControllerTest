import ctypes
import time
import colorsys

from objc_util import c, ObjCClass, create_objc_class, on_main_thread, UIApplication, ObjCInstance
import ui

#import pdbg


GLKView = ObjCClass('GLKView')
GLKViewController = ObjCClass('GLKViewController')
UINavigationController = ObjCClass('UINavigationController')
UIBarButtonItem = ObjCClass('UIBarButtonItem')
EAGLContext = ObjCClass('EAGLContext')

glClearColor = c.glClearColor
glClearColor.restype = None
glClearColor.argtypes = [
  ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float
]
glClear = c.glClear
glClear.restype = None
glClear.argtypes = [ctypes.c_uint]
GL_COLOR_BUFFER_BIT = 0x00004000


def glkView_drawInRect_(_self, _cmd, _view, rect):
  r, g, b = colorsys.hsv_to_rgb((time.time() * 0.1) % 1.0, 1, 1)
  glClearColor(r, g, b, 1.0)
  glClear(GL_COLOR_BUFFER_BIT)
  

MyGLViewDelegate = create_objc_class(
  'MyGLViewDelegate',
  methods=[glkView_drawInRect_],
  protocols=['GLKViewDelegate'])


view = ui.View()#frame=(0,0,600,600))

@on_main_thread
def main():
  context = EAGLContext.alloc().initWithAPI_(2).autorelease()
  #glview = GLKView.alloc().initWithFrame_(((0, 0), (320, 320))).autorelease()
  glview = GLKView.alloc().initWithFrame_(((0, 0), (100, 100))).autorelease()
  glview.setAutoresizingMask_((1 << 1) | (1 << 4))
  delegate = MyGLViewDelegate.alloc().init()
  glview.setDelegate_(delegate)
  glview.setContext_(context)
  glview.setEnableSetNeedsDisplay_(False)
  glvc = GLKViewController.alloc().initWithNibName_bundle_(None, None).autorelease()
  glvc.setTitle_('GLKit Demo')
  glvc.setView_(glview)
  view.objc_instance.addSubview_(glview)
  
  view.present(style='panel') #must be presented for nextResponder to work
  #pdbg.state(view.objc_instance)
  view.objc_instance.nextResponder().addChildViewController_(glvc)
  

if __name__ == '__main__':
  main()
