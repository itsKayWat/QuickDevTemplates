import winreg
import traceback

def add_context_menu_options():
    file_options = {
        'README.txt': '',
        'README.md': '',
        'README.html': '<!DOCTYPE html>\n<html>\n<head>\n    <title>README</title>\n</head>\n<body>\n\n</body>\n</html>',
        'Repository_Structure.txt': '',
        'styles.css': '/* Add your styles here */',
        'index.html': '<!DOCTYPE html>\n<html>\n<head>\n    <title>My Page</title>\n    <link rel="stylesheet" href="styles.css">\n</head>\n<body>\n\n    <script src="scripts.js"></script>\n</body>\n</html>',
        'scripts.js': '// Add your JavaScript code here',
        'popup.html': '<!DOCTYPE html>\n<html>\n<head>\n    <title>Popup</title>\n    <link rel="stylesheet" href="popup.css">\n</head>\n<body>\n\n    <script src="popup.js"></script>\n</body>\n</html>',
        'popup.css': '/* Add your popup styles here */',
        'popup.js': '// Add your popup JavaScript code here',
        'background.js': '// Add your background script code here'
    }

    try:
        print("Starting to add context menu options...")
        
        # Create individual menu items for each file type
        for filename, template in file_options.items():
            print(f"Adding menu option for: {filename}")
            
            # Create registry key for this file type
            key_path = f"Software\\Classes\\Directory\\Background\\shell\\Create{filename.replace('.', '_')}"
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            
            # Set the display name
            winreg.SetValue(key, '', winreg.REG_SZ, f'Create {filename}')
            
            # Add to 'New Dev Files' menu
            winreg.SetValueEx(key, 'MUIVerb', 0, winreg.REG_SZ, f'Create {filename}')
            winreg.SetValueEx(key, 'Icon', 0, winreg.REG_SZ, 'notepad.exe,0')
            winreg.SetValueEx(key, 'Position', 0, winreg.REG_SZ, 'Top')
            
            # Create command subkey
            cmd_key = winreg.CreateKey(key, 'command')
            
            if template:
                # Create file with template content
                escaped_template = template.replace('"', '\\"').replace('\n', '^&echo.')
                cmd = f'cmd.exe /c (echo {escaped_template}) > "%V\\{filename}"'
            else:
                # Create empty file
                cmd = f'cmd.exe /c echo. > "%V\\{filename}"'
            
            winreg.SetValue(cmd_key, '', winreg.REG_SZ, cmd)
            
            # Close keys
            winreg.CloseKey(cmd_key)
            winreg.CloseKey(key)

        print("Context menu options added successfully!")
        print("You can now right-click in any folder to see the new options.")
        input("Press Enter to exit...")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Full error traceback:")
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    add_context_menu_options()