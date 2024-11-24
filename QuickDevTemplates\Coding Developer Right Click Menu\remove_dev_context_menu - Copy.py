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
        
        # Expanded list of paths to remove
        paths_to_remove = [
            r'Software\Classes\Directory\Background\shell\CreateDevFile',
            r'Software\Classes\Directory\Background\shell\DevFiles',
            r'Software\Classes\Directory\Background\shell\DevFileCommands',
            r'Software\Classes\Directory\Background\shell\Create Dev File',
            r'Software\Classes\Directory\Background\shell\New',  # Remove the "New" entry
            r'Software\Classes\Directory\Background\Shell\CreateDevFile',
            r'Software\Classes\Directory\Background\Shell\DevFiles',
            r'Software\Classes\Directory\Background\Shell\DevFileCommands',
            # Add paths for individual file entries
            r'Software\Classes\Directory\Background\shell\Create_scripts_js',
            r'Software\Classes\Directory\Background\shell\Create_README_txt',
            r'Software\Classes\Directory\Background\shell\Create_README_html',
            r'Software\Classes\Directory\Background\shell\Create_popup_html',
            r'Software\Classes\Directory\Background\shell\Create_index_html'
        ]
        
        # Try both HKEY_CURRENT_USER and HKEY_CLASSES_ROOT
        hkeys = [
            (winreg.HKEY_CURRENT_USER, "HKEY_CURRENT_USER"),
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

            # Clean up any remaining related entries
            try:
                base_path = r'Software\Classes\Directory\Background\shell'
                base_key = winreg.OpenKey(hkey, base_path, 0, winreg.KEY_ALL_ACCESS)
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(base_key, i)
                        if any(term in subkey_name for term in ['Create', 'Dev', 'README', 'styles', 'scripts', 'popup', 'background', 'index', 'New']):
                            subkey_path = f"{base_path}\\{subkey_name}"
                            print(f"Removing related key: {subkey_path}")
                            key = winreg.OpenKey(hkey, subkey_path, 0, winreg.KEY_ALL_ACCESS)
                            delete_key_recursive(key, subkey_path)
                            winreg.DeleteKey(hkey, subkey_path)
                            continue
                        i += 1
                    except WindowsError:
                        break
                winreg.CloseKey(base_key)
            except WindowsError as e:
                print(f"Error while cleaning up individual entries: {str(e)}")

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