# In development!!!!!

version = '1.0.0'
import os
import sys
import time
import colorama
import curses
import tabulate


# Colors
class cprint:
    def orange(text):
        print(colorama.Fore.LIGHTRED_EX + text + colorama.Fore.RESET)
    def red(text):
        print(colorama.Fore.RED + text + colorama.Fore.RESET)
    def green(text):
        print(colorama.Fore.GREEN + text + colorama.Fore.RESET)
    def blue(text):
        print(colorama.Fore.BLUE + text + colorama.Fore.RESET)
    def yellow(text):
        print(colorama.Fore.YELLOW + text + colorama.Fore.RESET)

# Get system clock
def get_time():
    return time.strftime('%H:%M:%S')

# Colorful logging
class log:
    def info(text):
        cprint.blue(f'[{get_time()}] [INFO] {text}')
    def warn(text):
        cprint.yellow(f'[{get_time()}] [WARN] {text}')
    def error(text):
        cprint.red(f'[{get_time()}] [ERROR] {text}')
    def success(text):
        cprint.green(f'[{get_time()}] [SUCCESS] {text}')

# Get the current path of the script
path = os.path.dirname(os.path.realpath(__file__))

# Show logo
'''
y ::::::::  :::::::::: :::::::::::      :::::::::  :::::::::: ::::::::::: ::::::::::: :::::::::: :::::::::  
y:+:    :+: :+:            :+:          :+:    :+: :+:            :+:         :+:     :+:        :+:    :+: 
y+:+        +:+            +:+          +:+    +:+ +:+            +:+         +:+     +:+        +:+    +:+ 
o:#:        +#++:++#       +#+          +#++:++#+  +#++:++#       +#+         +#+     +#++:++#   +#++:++#:  
o+#+   +#+# +#+            +#+          +#+    +#+ +#+            +#+         +#+     +#+        +#+    +#+ 
r#+#    #+# #+#            #+#          #+#    #+# #+#            #+#         #+#     #+#        #+#    #+# 
r ########  ##########     ###          #########  ##########     ###         ###     ########## ###    ### 
'''
cprint.yellow('''::::::::  :::::::::: :::::::::::      :::::::::  :::::::::: ::::::::::: ::::::::::: :::::::::: :::::::::  \n:+:    :+: :+:            :+:          :+:    :+: :+:            :+:         :+:     :+:        :+:    :+: \n+:+        +:+            +:+          +:+    +:+ +:+            +:+         +:+     +:+        +:+    +:+ ''')
cprint.orange(''':#:        +#++:++#       +#+          +#++:++#+  +#++:++#       +#+         +#+     +#++:++#   +#++:++#:  \n+#+   +#+# +#+            +#+          +#+    +#+ +#+            +#+         +#+     +#+        +#+    +#+ \n''')
cprint.red('''#+#    #+# #+#            #+#          #+#    #+# #+#            #+#         #+#     #+#        #+#    #+# \n ########  ##########     ###          #########  ##########     ###         ###     ########## ###    ### \n''')
    
log.info('Launched!')
log.info('Using path: ' + path)
log.info('Version: ' + version)
log.info('Python version: ' + sys.version)

#

# Search for all files with "mosyle" in the name, for the full hard drive, and return the results in the function, full path of the file
def search_mosyle():
    log.info('Searching for mosyle files, this can take a bit...')
    log.warn('IT WILL ASK FOR YOU TO ALLOW IT TO ACCESS CERTAIN AREAS, ALLOW IT!!!')
    time.sleep(2)
    log.warn("Please enter your password for it to search system files")
    global mosyle_files
    mosyle_files = []
    for root, dirs, files in os.walk('/'):
        for file in files:
            if 'mosyle' in file:
                mosyle_files.append(os.path.join(root, file))
                log.info(f'Found mosyle file: {os.path.join(root, file)}')
    return mosyle_files


# Display number of mosyle files found
def count_mosyle():
    mosyle_files = search_mosyle()
    log.info(f'Found {len(mosyle_files)} files with "mosyle" in the name')
    
# Get all packages in the pkg folder
def get_packages():
    packages = []
    for package in os.listdir(path + '/pkg'):
        if os.path.isdir(path + '/pkg/' + package):
            packages.append(package)
    return packages

def get_packages_swselection():
    # Assuming the structure of the pkg folder is as follows, change if needed:
    # pkg/
    #   category1/
    #     app1
    #     app2
    #   category2/
    #     app3
    #     app4
    pkg_folder = 'pkg'
    packages = {}
    for category in os.listdir(pkg_folder):
        category_path = os.path.join(pkg_folder, category)
        if os.path.isdir(category_path):
            packages[category] = os.listdir(category_path)
    return packages

# Install package
def install_package(pkg):
    log.info(f'Installing package: {pkg}')
    os.system(f'sudo installer -pkg {path}/pkg/{pkg}/{pkg}.pkg -target /')
    log.success(f'Package {pkg} installed!')

def mosyle_remover():
    log.info('Removing mosyle files...')
    mosyle_files = search_mosyle()
    for file in mosyle_files:
        log.info(f'Removing file: {file}')
        os.remove(file)
        log.success(f'Removed file: {file}')

def get_packages():
    pkg_folder = 'pkg'
    packages = {}
    for category in os.listdir(pkg_folder):
        category_path = os.path.join(pkg_folder, category)
        if os.path.isdir(category_path):
            packages[category] = os.listdir(category_path)
    return packages

def display_menu(stdscr, packages):

    curses.curs_set(0)
    global selected_packages
    current_row = 0
    selected_packages = {category: [False] * len(packages[category]) for category in packages}

    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)  # Selection box
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Selected item
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Package text
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Category text

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        row_idx = 0
        for category, apps in packages.items():
            if row_idx < height:
                if row_idx == current_row:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(row_idx, 0, category[:width])
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.attron(curses.color_pair(4))
                    stdscr.addstr(row_idx, 0, category[:width])
                    stdscr.attroff(curses.color_pair(4))
            row_idx += 1
            for idx, app in enumerate(apps):
                x = 2
                y = row_idx
                checkbox = "[X]" if selected_packages[category][idx] else "[ ]"
                text = f"{checkbox} {app}"
                if row_idx < height:
                    if len(text) > width - x:
                        text = text[:width - x - 1]
                    if row_idx == current_row:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr(y, x, text)
                        stdscr.attroff(curses.color_pair(1))
                    else:
                        attr = curses.color_pair(2) if selected_packages[category][idx] else curses.color_pair(3)
                        if selected_packages[category][idx]:
                            attr |= curses.A_UNDERLINE
                        stdscr.attron(attr)
                        stdscr.addstr(y, x, text)
                        stdscr.attroff(attr)
                row_idx += 1

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < row_idx - 1:
            current_row += 1
        elif key == ord(' '):
            category_idx = 0
            for category, apps in packages.items():
                if current_row == category_idx:
                    # Toggle all items in the category
                    all_selected = all(selected_packages[category])
                    selected_packages[category] = [not all_selected] * len(apps)
                    break
                category_idx += 1
                if current_row < category_idx + len(apps):
                    app_idx = current_row - category_idx
                    selected_packages[category][app_idx] = not selected_packages[category][app_idx]
                    break
                category_idx += len(apps)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            break

    return selected_packages

def getAbsolutePathPkg(path):
    return os.path.abspath(path)

# Nice table for the installer list
def tableInstallerList(paths):
    table = []
    for path in paths:
        table.append([path])
    print(tabulate.tabulate(table, headers=['Installer'], tablefmt='fancy_grid'))

def main(stdscr):
    packages = get_packages()
    selected_packages = display_menu(stdscr, packages)

    stdscr.clear()
    stdscr.addstr(0, 0, "Selected packages:")
    row_idx = 1
    for category, apps in selected_packages.items():
        for idx, selected in enumerate(apps):
            if selected:
                stdscr.addstr(row_idx, 0, f"{category}/{packages[category][idx]}")
                row_idx += 1
    stdscr.refresh()
    stdscr.getch()

    # Get the selected packages in a list of paths
    global selected_paths
    selected_paths = [os.path.join('pkg', category, packages[category][idx]) for category, apps in selected_packages.items() for idx, selected in enumerate(apps) if selected]
    for path in selected_paths:
        print(path)

def main1(stdscr):
    packages = get_packages_swselection()
    selected_packages = display_menu(stdscr, packages)

    stdscr.clear()
    stdscr.addstr(0, 0, "Selected packages:")
    row_idx = 1
    for category, apps in selected_packages.items():
        for idx, selected in enumerate(apps):
            if selected:
                stdscr.addstr(row_idx, 0, f"{category}/{packages[category][idx]}")
                row_idx += 1
    stdscr.refresh()
    stdscr.getch()

    # Get the selected packages in a list of paths
    global selected_paths
    selected_paths = [os.path.join('dmg', category, packages[category][idx]) for category, apps in selected_packages.items() for idx, selected in enumerate(apps) if selected]
    for path in selected_paths:
        print(path)

# Second installation menu for dmg files, just add to the list of selected paths but have a different function and work from the dmg folder
def getDmgFiles():
    dmg_folder = 'dmg'
    dmg_files = []
    for file in os.listdir(dmg_folder):
        if file.endswith('.dmg'):
            dmg_files.append(file)
    return dmg_files

def display_menu_dmg(stdscr, dmg_files):
        curses.curs_set(0)
        global selected_dmg_files
        current_row = 0
        selected_dmg_files = [False] * len(dmg_files)
    
        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)  # Selection box
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Selected item
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Package text
    
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
    
            for idx, file in enumerate(dmg_files):
                x = 2
                y = idx
                checkbox = "[X]" if selected_dmg_files[idx] else "[ ]"
                text = f"{checkbox} {file}"
                if y < height:
                    if len(text) > width - x:
                        text = text[:width - x - 1]
                    if y == current_row:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr(y, x, text)
                        stdscr.attroff(curses.color_pair(1))
                    else:
                        attr = curses.color_pair(2) if selected_dmg_files[idx] else curses.color_pair(3)
                        if selected_dmg_files[idx]:
                            attr |= curses.A_UNDERLINE
                        stdscr.attron(attr)
                        stdscr.addstr(y, x, text)
                        stdscr.attroff(attr)
    
            stdscr.refresh()
    
            key = stdscr.getch()
    
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(dmg_files) - 1:
                current_row += 1
            elif key == ord(' '):
                selected_dmg_files[current_row] = not selected_dmg_files[current_row]
            elif key == curses.KEY_ENTER or key in [10, 13]:
                break
    
        return selected_dmg_files



def installPackageDmg():
    log.info("Installing DMG packages")
    for path in selected_paths:
        log.info(f"Installing DMG package: {path}")
        os.system(f'sudo hdiutil attach {path}')
        log.success(f"DMG package {path} installed!")
        log.warn("You must manually install the package from the mounted DMG file!!!")



def programMain(selected_paths, mosyle_files):
    # Show the installer list
    log.info('Selected installers:')
    tableInstallerList(selected_paths)
    log.info('Found mosyle files based on naming schema and hashID:')
    tableInstallerList(mosyle_files)
    log.info("Mosyle search complete")
    # Exit with the installers selected

if __name__ == '__main__':
    # Grab mosyle data on the computer
    log.info("Checking for mosyle hash, this is going to take a bit...")
    mosyle_files = search_mosyle()
    log.warn("Starting the menu for the installer of pkg files!!!")
    curses.wrapper(main)
    programMain(selected_paths, mosyle_files)
    log.warn("Starting the menu for the installer of dmg files!!!")
    curses.wrapper(main1) 
    log.success('Exiting the termial UI with the paths with installers: ' + ', '.join(getAbsolutePathPkg(path) for path in selected_paths))
