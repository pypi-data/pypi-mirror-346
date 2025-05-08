import os
import importlib.util
import traceback

def load_modules(bot, platform, folder='modules'):
    if not os.path.exists(folder):
        print(f"Module folder '{folder}' does not exist. Skipping module load.")
        return

    for filename in os.listdir(folder):
        if filename.endswith('.py'):
            module_path = os.path.join(folder, filename)
            module_name = filename[:-3]
            try:
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'setup'):
                    module.setup(bot, platform)
                    print(f"Loaded module: {module_name}")
                else:
                    print(f"Module '{module_name}' does not have a setup(bot, platform) function. Skipped.")
            except Exception as e:
                print(f"Failed to load module '{module_name}': {e}")
                traceback.print_exc()
