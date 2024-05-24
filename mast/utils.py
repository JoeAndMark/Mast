"""
utils.py

This module provides utility functions for file operations, including opening, saving, and moving files.

Functions:
- fileOpen(parent) -> tuple[str, str]: Opens a file dialog to select and read a file.
- fileSave(parent, text: str) -> str: Opens a file dialog to save the current text to a file.
- fileSaveAs(parent, text: str) -> str: Opens a file dialog to save the current text to a new file.
- fileMoveTo(parent) -> str: Opens a file dialog to move a selected file to a new directory.
"""

from PySide6.QtWidgets import QFileDialog
import os
import shutil

def fileOpen(parent):
    """
    Opens a file dialog to select and read a file.

    Args:
        parent: The parent widget for the file dialog.

    Returns:
        tuple[str, str]: The content of the file and the file path.
                    Returns (None, None) if no file is selected.
    """
    file, ok = QFileDialog.getOpenFileName(parent, "Open", QDir.currentPath(), \
                                            "Markdown Files (*.md);;Text Files (*.txt);;\
                                            LaTeX Files (*.tex);;Typst Files (*.typ)")
    if ok:
        with open(file, 'r') as f:
            content = f.read()
        return content, file
    return None, None

def fileSave(parent, text):
    """
    Opens a file dialog to save the current text to a file.

    Args:
        parent: The parent widget for the file dialog.
        text (str): The text content to save.

    Returns:
        str: The file path where the text is saved.
             Returns None if no file is selected.
    """
    file, ok = QFileDialog.getSaveFileName(parent, "Save File", "",\
                                            "Markdown Files (*.md);;Text Files (*.txt);;\
                                            LaTeX Files (*.tex);;Typst Files (*.typ)")
    if ok:
        with open(file, 'w') as f:
            f.write(text)
        return file
    return None

def fileSaveAs(parent, text):
    """
    Opens a file dialog to save the current text to a new file.

    Args:
        parent: The parent widget for the file dialog.
        text (str): The text content to save.

    Returns:
        str: The new file path where the text is saved.
             Returns None if no file is selected.
    """
    file, ok = QFileDialog.getSaveFileName(parent, "Save File As", "", "Markdown Files(*.md);;Text Files (*.txt);;LaTeX Files (*.tex);;Typst Files (*.typ)")
    if ok:
        with open(file, 'w') as f:
            f.write(text)
        return file
    return None

def fileMoveTo(parent):
    """
    Opens a file dialog to move a selected file to a new directory.

    Args:
        parent: The parent widget for the file dialog.

    Returns:
        str: The new file path after moving.
            Returns None if no file is selected or the move is cancelled.
    """
    sourceFile, ok = QFileDialog.getOpenFileName(parent, "Select File", "", "Markdown Files(*.md);;Text Files (*.txt);;LaTeX Files (*.tex);;Typst Files (*.typ)")
    if ok:
        destinationFolder = QFileDialog.getExistingDirectory(parent, "Select Destination Folder", "")
        if destinationFolder:
            destinationFile = shutil.move(sourceFile, destinationFolder)
            return destinationFile
    return None
