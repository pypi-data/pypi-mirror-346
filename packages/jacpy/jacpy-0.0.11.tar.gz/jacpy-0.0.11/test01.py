import os

from src.jacpy.hash import hashUtils
from src.jacpy.io import ioUtils
from src.jacpy.geometry import geoUtils

items = ioUtils.dirItems(r'C:\Users\alber\Downloads\pics', ioUtils.DirItemPolicy.OnlyFilesAlphabetic, ioUtils.DirItemOutputForm.FullPath)

# print(items)
for item in items:
    fixedItem, modified = ioUtils.RemoveNonUtf8Chars(item)
    if modified:
        os.rename(item, fixedItem)

sss = 'pexels-tobias-bjørkli-2360673'

ioUtils.RemoveNonUtf8Chars(sss)



ioUtils.RemoveFilesWithParenthesis(r'C:\Users\alber\Downloads\pics')
ioUtils.RemoveFiles170x170(r'C:\Users\alber\Downloads\pics')
ioUtils.KeepJpgFiles(r'C:\Users\alber\Downloads\pics')


partitions = geoUtils.partition1DGeometry(50, 50, 0.5, 1.5)
print(partitions)


partitions = geoUtils.partition2DGeometry(100, 51, 50, 50, 0.5, 1.5)
print(partitions)