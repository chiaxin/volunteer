import os.path
import collections
import maya.cmds as mc

class TexturePath():
    def __init__(self, node, texture):
        self.node = node
        self.tex = texture
    def __eq__(self, other):
        return self.tex == other.tex
    def __eq__(self, name):
        return self.tex == name
    def __ne__(self, other):
        return self.tex != other.tex
    def __lt__(self, other):
        return self.tex < other.tex
    def __gt__(self, other):
        return self.tex > other.tex
    def __repr__(self):
        return self.node + '@' + self.tex

def removeSetWithChildren(setname):
    children = mc.listConnections(setname, s=True, d=False, type='objectSet')
    map(lambda x: mc.delete(x), children)

def getAllFileTextures(*args, **kwargs):
    textureNodeTypes = kwargs.get('textureNodeTypes', ['file'])
    result = [TexturePath(f, os.path.basename(mc.getAttr(f+'.fileTextureName'))) \
    for f in mc.ls(type=textureNodeTypes)]
    return filter(lambda x: bool(x.tex), result)

def findDuplicatedTexturePath(*args, **kwargs):
    texturePath = sorted(getAllFileTextures(), key=lambda x: x.tex)
    duplicated = [item for item, count in \
    collections.Counter([t.tex for t in texturePath]).items() if count > 1]
    result = []
    for dup in duplicated:
        result.append(tuple([dup, tuple([p.node for p in texturePath if p.tex == dup])]))
    return tuple(result)

def groupDuplicatedTexture(*args, **kwargs):
    mainset = kwargs.get('mainset', 'duplicatedTexturePathSet')
    if mc.objExists(mainset):
        removeSetWithChildren(mainset)
    duplicated = findDuplicatedTexturePath()
    setBuffer = []
    for tex in duplicated:
        grpset = mc.sets(name=tex[0], empty=True)
        for nod in tex[1]:
            setBuffer.append(mc.sets(nod, fe=grpset))
    mc.sets(setBuffer, name=mainset)

def doIt():
    if not len(mc.ls(type='file')):
        mc.warning('Not any vaild texture node in this scene!')
        return
    groupDuplicatedTexture()
