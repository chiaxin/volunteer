import maya.cmds as mc
import findDuplicatedTexturePath

class VolunteerUI:
    Win = 'VolunteerWin'
    Uit = 'VolunteerUit'
    Title = 'Volunteer Misc Tools'
    widthHeight = (270, 240)
    def __init__(self):
        pass

    def build(self):
        self.destroy()
        if mc.uiTemplate(self.Uit, q=True, ex=True):
            mc.deleteUI(self.Uit, uit=True)
        mc.uiTemplate(self.Uit)
        mc.button(dt=self.Uit, w=150, h=36)
        mc.text(dt=self.Uit, font='fixedWidthFont')
        self.Win = mc.window(self.Win, wh=self.widthHeight, title=self.Title)
        mc.setUITemplate(self.Uit, pushTemplate=True)
        mc.columnLayout()
        mc.button(l='Find Duplicated Texture', c=lambda x: findDuplicatedTexturePath.doIt())
        mc.setParent('..')
        mc.setUITemplate(popTemplate=True)

    def destroy(self):
        if mc.window(self.Win, q=True, ex=True):
            mc.deleteUI(self.Win)

    def show(self):
        mc.showWindow(self.Win)
        mc.window(self.Win, e=True, wh=self.widthHeight)

def volunteer(*args, **kwargs):
    ui = VolunteerUI()
    ui.build()
    ui.show()
