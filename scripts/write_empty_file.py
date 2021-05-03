import os

from fenia.object import BaseObject

path = os.path.join('empty')

fo = BaseObject(path)
fo.write()
