Steps and tips for allowing the CST Automation scripts to run correctly.

SCRIPTS:
RunTransferManager - Takes Box IDs, transfers them to a pallet.
RunPutawayManger - Takes Box IDs, transfers them to a pallet, and changes their status to Putaway.
RunPrintBoxLabel - Takes Pallet #, prints labels for all the units associated with the pallet in batches of 50.
RunFindOddOneOut - Takes Box IDs, spin-off of RunTransferManager. Scan a group of units and script will tell
		   which ones aren't on the specified pallet.

STEPS TO RUN:
1. Install Anaconda from the link below. This is what installs Python and gives a good interface.
	1b. Install file can be found at 'https://www.anaconda.com/products/individual'. File was too big to include with package. Anaconda will take a while to install.
		(note: you don't need to make an account/login to the anaconda website)
	1a. After install, you can run python from Jupyter Notebooks. There are other options, but Jupyter is the recommended one.
2. Install Chrome from the ChromeSetup.exe installer in the package/zip
	(note: If you already have Chrome installed, it should work fine. But if there are errors, uninstall and retry with the installer included in the package which uses the 
	            version of Chrome used when making these scripts.)
3. Run ChromeDriver.exe and disable HP Sure Click Protection (you can close out after the protection is disabled)
	(note: if nothing about HP Sure Click opens before the Command Line does, just move on.)
4. Open Jupyter Notebooks
	(note: Jupyter will open a CLI in the background as well as a localhost webpage. Only interact with the webpage. Leave the CLI open while using Jupyter.)
5. Navigate to where you have downloaded the CST Automation folder and open one of the .ipynb scripts.
6. At the bottom of the page at the new line that says "In [ ]:" run these two commands (you can run by pressing CTRL+ENTER or hitting the run button at the top of the page)
	6a. 'pip install selenium' (don't include the quotes with these)
	6b. 'pip install pandas'
7. You can close this extra line afterwards by double-tapping 'd' while the line to the left of the interface is blue (instead of green).
8. Once both libraries are installed, you are free to run any of the .ipynb scripts.
	(note: you only need to install the selenium and pandas libraries once)

TIPS:
-When you run the scripts, a separate Chrome browser instance will open. You're free to watch, but don't click anything on it while the script is running.
-Make sure all the files in the package/zip stay together. 
-If the script you're running doesn't do anything, trying clicking the stop button at the top and running the script again.
-Make sure to select the first cell where all the code is to be able to run or stop it.
-If there is an error saying something along the lines of Pandas or Selenium can't be found or isn't installed, even though you ran the two commands at 6a and 6b, 
restart the kernal by selecting the Kernal tab at the top of the page and selecting "Restart" from the drop-down list.
-If you decide to run the scripts in something else besides Jupyter such as Spyder, Python IDLE, or Window's Command Line Interface,
you'll need to use the .py files instead of the .ipynb files.

HOTKEYS:
Run program: 'CTRL + ENTER'
Interupt/Stop Program: 'i','i'
Save Program: 'CTRL + S'
Delete Cell: 'D','D'
Restart Kernel: '0','0' <---Those are zeros from the row above the keyboard, not NumPad.


Scripts written by Andrew Overton, JAN/2022. 
If you'd like to contract help in troubleshooting or adding to these scripts, contact at AndrewRobOverton@gmail.com