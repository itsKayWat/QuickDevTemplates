import winreg
import traceback

def delete_key_recursive(key, path):
    try:
        while True:
            try:
                subkey = winreg.EnumKey(key, 0)
                subkey_path = f"{path}\\{subkey}"
                subkey_handle = winreg.OpenKey(key, subkey, 0, winreg.KEY_ALL_ACCESS)
                delete_key_recursive(subkey_handle, subkey_path)
                winreg.CloseKey(subkey_handle)
                winreg.DeleteKey(key, subkey)
            except WindowsError:
                break
        winreg.CloseKey(key)
    except WindowsError as e:
        print(f"Error while deleting {path}: {str(e)}")

def remove_context_menu_options():
    try:
        print("Attempting to remove all context menu options...")
        
        # Expanded list of paths to remove, including Visual Studio's New entry
        paths_to_remove = [
            # Standard Windows New menu
            r'Software\Classes\Directory\Background\shellex\New',
            # Visual Studio context menu paths
            r'Software\Classes\Directory\Background\shell\AnyCode\shell\New',
            r'Software\Classes\Directory\Background\shell\VSCode\shell\New',
            r'Software\Classes\Directory\Background\shell\VisualStudio\shell\New',
            # Our previous paths
            r'Software\Classes\Directory\Background\shell\CreateDevFile',
            r'Software\Classes\Directory\Background\shell\DevFiles',
            r'Software\Classes\Directory\Background\shell\DevFileCommands',
            r'Software\Classes\Directory\Background\shell\Create Dev File'
        ]
        
        # Try both HKEY_CURRENT_USER and HKEY_LOCAL_MACHINE
        hkeys = [
            (winreg.HKEY_CURRENT_USER, "HKEY_CURRENT_USER"),
            (winreg.HKEY_LOCAL_MACHINE, "HKEY_LOCAL_MACHINE"),
            (winreg.HKEY_CLASSES_ROOT, "HKEY_CLASSES_ROOT")
        ]
        
        for hkey, hkey_name in hkeys:
            for path in paths_to_remove:
                try:
                    print(f"Attempting to remove from {hkey_name}: {path}")
                    key = winreg.OpenKey(hkey, path, 0, winreg.KEY_ALL_ACCESS)
                    delete_key_recursive(key, path)
                    winreg.DeleteKey(hkey, path)
                    print(f"Successfully removed: {path}")
                except WindowsError as e:
                    print(f"Could not find or delete: {path}")
                    continue

            # Additional cleanup for Visual Studio related entries
            try:
                vs_paths = [
                    r'Software\Classes\Directory\Background\shell\VisualStudio',
                    r'Software\Classes\Directory\Background\shell\VSCode',
                    r'Software\Classes\Directory\Background\shell\AnyCode'
                ]
                
                for vs_path in vs_paths:
                    try:
                        key = winreg.OpenKey(hkey, vs_path, 0, winreg.KEY_ALL_ACCESS)
                        shell_key_path = f"{vs_path}\\shell"
                        shell_key = winreg.OpenKey(hkey, shell_key_path, 0, winreg.KEY_ALL_ACCESS)
                        try:
                            winreg.DeleteKey(shell_key, 'New')
                            print(f"Removed 'New' from {shell_key_path}")
                        except WindowsError:
                            pass
                        winreg.CloseKey(shell_key)
                        winreg.CloseKey(key)
                    except WindowsError:
                        continue

            except WindowsError as e:
                print(f"Error while cleaning Visual Studio entries: {str(e)}")

        print("\nContext menu cleanup completed!")
        print("Please restart Explorer or log out and back in for changes to take effect.")
        input("Press Enter to exit...")
        
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        print("Full error traceback:")
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    remove_context_menu_options()