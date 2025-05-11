import fnmatch
import os
from enum import Enum


class DirItemPolicy(Enum):
    FilesAndDirs = 1  # files first, then dirs (each group in alphabetic order)
    DirsAndFiles = 2  # dirs first, then files (each group in alphabetic order)
    AllAlphabetic = 3  # file and dirs together, in alphabetic order
    OnlyFilesAlphabetic = 4  # only files, in alphabetic order
    OnlyDirsAlphabetic = 5  # only dirs, in alphabetic order

class DirItemOutputForm(Enum):
    FullPath = 1
    Name = 2

def appendItem(items, itemPath, item, outputForm=DirItemOutputForm.FullPath, fileMask=None, fileMaskNot=None):
    if (fileMask == None or fnmatch.fnmatch(item, fileMask)) and (fileMaskNot == None or not fnmatch.fnmatch(item, fileMaskNot)):
        items.append(itemPath) if outputForm == DirItemOutputForm.FullPath else items.append(item)

def dirItems(path, files=DirItemPolicy.FilesAndDirs, outputForm=DirItemOutputForm.FullPath, fileMask=None, fileMaskNot=None, fromDepth=0, maxDepth=65535):
    if maxDepth < 0:
        return []
    # the items that will be returned by the function
    items = []
    # items that are files (temporarily stored here for proper ordering)
    fileItems = []
    fileItemsNames = []
    # items that are directories (temporarily stored here for proper ordering and for recursive calls)
    directoryItems = []
    directoryItemsNames = []
    for item in os.listdir(path):
        itemPath = os.path.join(path, item)
        if os.path.isfile(itemPath) and fromDepth <= 0:
            if files == DirItemPolicy.FilesAndDirs or files == DirItemPolicy.DirsAndFiles:
                fileItems.append(itemPath)
                fileItemsNames.append(item)
            elif files == DirItemPolicy.AllAlphabetic or files == DirItemPolicy.OnlyFilesAlphabetic:
                appendItem(items, itemPath, item, outputForm, fileMask, fileMaskNot)
                # items.append(itemPath) if outputForm == DirItemOutputForm.FullPath else items.append(item)
        elif os.path.isdir(itemPath):
            directoryItems.append(itemPath)
            directoryItemsNames.append(item)
            if files == DirItemPolicy.AllAlphabetic or files == DirItemPolicy.OnlyDirsAlphabetic:
                if fromDepth <= 0:
                    appendItem(items, itemPath, item, outputForm, fileMask, fileMaskNot)
                    # items.append(itemPath) if outputForm == DirItemOutputForm.FullPath else items.append(item)

    # generate final list
    if fromDepth <= 0:
        if files == DirItemPolicy.FilesAndDirs:
            items = fileItems + directoryItems if outputForm == DirItemOutputForm.FullPath else fileItemsNames + directoryItemsNames
        elif files == DirItemPolicy.DirsAndFiles:
            items = directoryItems + fileItems if outputForm == DirItemOutputForm.FullPath else directoryItemsNames + fileItemsNames

    # recursive calls
    for directory in directoryItems:
        items += dirItems(directory, files, outputForm, fileMask, fileMaskNot, fromDepth - 1, maxDepth - 1)

    return items




def RemoveFilesWithParenthesis(path):
    items = dirItems(path, DirItemPolicy.OnlyFilesAlphabetic,
                             DirItemOutputForm.FullPath, "*(*)*")
    for item in items:
        os.remove(item)

def RemoveFiles170x170(path):
    items = dirItems(path, DirItemPolicy.OnlyFilesAlphabetic,
                             DirItemOutputForm.FullPath, "*170x170*")
    for item in items:
        os.remove(item)

def KeepJpgFiles(path):
    items = dirItems(path, DirItemPolicy.OnlyFilesAlphabetic,
                             DirItemOutputForm.FullPath, fileMaskNot="*.jpg")
    for item in items:
        os.remove(item)


def RemoveNonUtf8Chars(s, rep='_'):
    index = 0
    modified = False
    for c in s:
        if (len(c.encode('utf-8')) > 1):
            s = ReplaceChar(s, index, rep)
            modified = True
        index += 1
    return s, modified


def ReplaceChar(s, index, char):
    s = s[:index] + char + s[index + 1:]
    return s
