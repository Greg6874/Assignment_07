#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# GEisele, 2022-Nov-19, Modified code for assignment 06
# GEisele, 2022-Nov-21, Modified code for assignment 07
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    
    @staticmethod
    def add_row():
        """Adds a dictionary row to 2d list.
        
        Adds user input stored in variables intID, strTitle, to a dictionary row,
        then stores the dictionary row in a 2d table.
        
        Args:
            None.       
            
        Returns:
            None.
        """
        intID = int(strID)
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        lstTbl.append(dicRow)   
    
    @staticmethod
    def del_row():
        """Removes a dictionary row from 2d list.
        
        Removes a dictionary row from the 2d table based on user input ID.
        
        Args:
            None.        
            
        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')    

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage binary data ingestion from .dat file to a list of dictionaries.

        Reads the binary data from file identified by file_name into a 2D table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        
        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        objFile = open(file_name, 'rb')
        global lstTbl
        lstTbl = pickle.load(objFile)
        objFile.close()
       

    @staticmethod
    def write_file(file_name, table):
        """Function to manage data writing from list of dictionaries to .dat file.

        Writes the data to file identified by file_name in binary format.

        Args:
            file_name (string): name of file used to write the data to.
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        
        Returns:
            None.
        """
        objFile = open(strFileName, 'wb')
        pickle.dump(lstTbl, objFile)
        objFile.close()
        print('file saved')
        
# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user.

        Args:
            None.
        
        Returns:
            None.
        """
        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection.

        Args:
            None.
        
        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x.
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table.

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        
        Returns:
            None.
        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def ask_user():
        """User to inputs new data.
        
        Args:
            None.
        
        Returns:
            None.
        """
        global strID
        strID = input('Enter ID: ').strip()
        global strTitle
        strTitle = input('What is the CD\'s title? ').strip()
        global strArtist
        strArtist = input('What is the Artist\'s name? ').strip()        
        
# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled \n')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        while True:
            IO.ask_user()
        # 3.3.2 Add item to the table
            try:
                DataProcessor.add_row()
                break
            except (ValueError):
                print('USER ERROR!\nOnly numbers can be entered for ID!  Try again!\n')
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        while True:
            try:
                intIDDel = int(input('Which ID would you like to delete? ').strip())
                break
            except (ValueError):
                print('Only numbers can be entered for ID!  Try again!\n')
        # 3.5.2 search thru table and delete CD
        DataProcessor.del_row()
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)   
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')





