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

        # First, create the shell commands registry key
        shell_cmds_path = r'Software\Classes\Directory\Background\shell\DevFileCommands'
        shell_cmds_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, shell_cmds_path)

        # Create individual command entries
        for filename, template in file_options.items():
            cmd_key_path = f"{shell_cmds_path}\\{filename.replace('.', '_')}"
            cmd_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_key_path)
            winreg.SetValue(cmd_key, '', winreg.REG_SZ, f'Create {filename}')
            winreg.SetValueEx(cmd_key, 'Icon', 0, winreg.REG_SZ, 'shell32.dll,41')

            # Create command subkey
            command_key = winreg.CreateKey(cmd_key, 'command')
            if template:
                escaped_template = template.replace('"', '\\"').replace('\n', '^&echo.')
                cmd = f'cmd.exe /c (echo {escaped_template}) > "%V\\{filename}"'
            else:
                cmd = f'cmd.exe /c echo. > "%V\\{filename}"'
            winreg.SetValue(command_key, '', winreg.REG_SZ, cmd)
            winreg.CloseKey(command_key)
            winreg.CloseKey(cmd_key)

        # Create the main menu item
        main_key_path = r'Software\Classes\Directory\Background\shell\DevFiles'
        main_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, main_key_path)
        winreg.SetValue(main_key, '', winreg.REG_SZ, 'Create Dev File')
        winreg.SetValueEx(main_key, 'Icon', 0, winreg.REG_SZ, 'shell32.dll,41')
        winreg.SetValueEx(main_key, 'ExtendedSubCommandsKey', 0, winreg.REG_SZ, 
                         r'Directory\Background\shell\DevFileCommands')
        winreg.SetValueEx(main_key, 'Position', 0, winreg.REG_SZ, 'Top')

        winreg.CloseKey(main_key)
        winreg.CloseKey(shell_cmds_key)

        print("Context menu options added successfully!")
        print("You can now right-click in any folder and select 'Create Dev File' to see the options.")
        input("Press Enter to exit...")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Full error traceback:")
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    add_context_menu_options()