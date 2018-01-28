#! -*- coding: utf-8 -*-

import os.path
from os.path import basename
import collections
import maya.cmds as mc

class TexturePath(object):
    '''
        Texture class
    '''
    def __init__(self, node, texture):
        '''
            Initialize
        '''
        self.node = node
        self.tex = texture

    def __eq__(self, other):
        if isinstance(TexturePath, other):
            return self.tex == other.tex
        elif isinstance(TexturePath, (str, unicode)):
            return self.tex == other
        return False

    def __ne__(self, other):
        return self.tex != other.tex

    def __lt__(self, other):
        return self.tex < other.tex

    def __gt__(self, other):
        return self.tex > other.tex

    def __repr__(self):
        return self.node + '@' + self.tex

def remove_set_with_children(setname):
    '''
        pass
    '''
    children = mc.listConnections(
        setname, s=True, d=False, type='objectSet'
    )
    map(lambda x: mc.delete(x), children)

def get_all_file_textures(*args, **kwargs):
    '''
        Get all texture as TexturePath class in the scene.
    '''
    texture_node_types = kwargs.get('texture_node_types', ['file'])
    result = [
        TexturePath(f, basename(mc.getAttr(f+'.fileTextureName')))\
        for f in mc.ls(type=texture_node_types)
    ]
    return [f for f in result if bool(f.tex)]

def find_duplicated_texture_path(*args, **kwargs):
    '''
        ---
    '''
    texture_path = sorted(get_all_file_textures(), key=lambda x: x.tex)
    duplicated = [item for item, count in \
    collections.Counter([t.tex for t in texture_path]).items() if count > 1]
    result = []
    for dup in duplicated:
        result.append(tuple([dup, tuple([p.node for p in texture_path if p.tex == dup])]))
    return tuple(result)

def group_duplicated_texture(*args, **kwargs):
    '''
        ---
    '''
    mainset = kwargs.get('mainset', 'duplicatedTexturePathSet')
    if mc.objExists(mainset):
        remove_set_with_children(mainset)
    duplicated = find_duplicated_texture_path()
    setBuffer = []
    for tex in duplicated:
        grpset = mc.sets(name=tex[0], empty=True)
        for nod in tex[1]:
            setBuffer.append(mc.sets(nod, fe=grpset))
    mc.sets(setBuffer, name=mainset)

def doIt():
    if not len(mc.ls(type='file')):
        mc.warning('Not any valid texture node in this scene!')
        return
    group_duplicated_texture()
