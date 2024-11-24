DevFileForge - Developer File Template Generator

Why:
This tool was created to streamline the development workflow by eliminating repetitive file creation tasks. Instead of manually creating and structuring common development files, developers can generate them instantly through the Windows context menu.

How it was made:
Built using Python, the tool leverages the Windows Registry (winreg) to create custom context menu entries. It injects template-based file generation commands that execute when selected.

Purpose:
- Rapid creation of common development files
- Consistent file structures across projects
- Time-saving developer utility
- Pre-filled templates for quick starts

Usage Example:
When starting a new web project:
1. Right-click in your project folder
2. Select "Create Dev File"
3. Choose from options like README.md, index.html, styles.css, etc.
4. Files are created instantly with basic templates

Installation:
1. Run install_dev_context_menu.py with administrator privileges
2. Windows Explorer will now have the new context menu options
3. Restart Explorer or log out/in for changes to take effect

Removal:
1. Run remove_dev_context_menu.py with administrator privileges
2. All context menu modifications will be removed
3. Restart Explorer or log out/in for changes to take effect