# Finessensual

Finessensual is a python script that allows the conversion of Oracle
financial transaction reports into an overview that is useful for
research groups (around one or more Pis). Its name is contraction (or
you might call it a contraption) of ‘finance’, ‘essential’ and ‘UA’.

* [A. Installation](#installation)
* [B. Using the package](#usage)
* [C. License](#license)
* [D. Warranty](#warranty)


## A. Installation <a id="installation"></a>

### 1. Install the prerequisites

- When on GNU/Linux, UNIX or MAC:

  Install:

  - libreoffice
    (e.g. on Ubuntu: 'sudo apt-get install libreoffice')

  - a python 3 interpreter
    (e.g. on Ubuntu: 'sudo apt-get install python3')

  Make sure the libreoffice executable and the python3 executable can
  be found based on your PATH environment variable.

- When on MS-Windows:

  Install:

  - libreoffice
    Go to the , download the latest version and install it.  
    (don't install libreoffice from the microsoft store, or those
    b@s!@rds will charge you for it!)

  - python  
    Click on the windows start icon and start typing 'python' until you
    see as best match 'python, Run command'. Clicking on that will open
    the microsoft store on the Python page. Click on 'Get' to install
    python on your machine.

### 2. Install the package itself

The finessensual code can be found on [PyPI](https://pypi.org/project/finessensual).

- When on GNU/Linux, UNIX or MAC:
  If you have a python interpreter installed on a GNU/Linux, BSD-like
  or UNIX-like workstation that is all you need. You can install the
  package from the command line as follows:

 \$ pip install –upgrade finessensual

- When on MS-Windows
  On this platform, unfortunately, users have unlearnt how to install
  software and how to use the command line). Therefore, I spent on of me
  weekends making you a finessensual installer executable that will
  perform the installation and make a desktop icon for you.

## B. Using the package <a id="usage"></a>

### 1. Download all financial files from oracle

Start your oracle java application to consult “Financiële
gebruikersrapporten” (below this will be abbreviated as FG) from . If we
say ‘download’ below, we mean *save in one and the same
folder*.

- Download the information on Vlottende Budgetten:

  FG \> Werk voor derde en derdengeld \> Forfaitaire project, BOF, IOF
  en activiteiten \> Vlottende Budgetten
  
  Download all ‘vlottende budgetten’ (like: AK, AO, RA, WD, WO) in
  excel format and name them ‘VBTransacties-’ + nummer + ‘.xls’.
  As an example: ‘VBTransacties-AK160007.xls’

- Download ‘Budgets and transactions’ related to the PIs that are
  part of the financial overview in excel format

  FG \> Werk voor derden en derdengeld \> Verantwoordingsprojecten \>
  Budgetten en transacties

  Select the PI you want to cover.

  Select ‘excel’ as format. This will leave only three buttons active in the rightmost row:
  - Budgetten : download this file and name it UB-\<PI-name\>.xml
  - Vastleggingen : download this file and name it UV-\<PI-name\>.xml
  - Uitgaven : download this file and name it UU-\<PI-name\>.xml
  
  As an example: UB-DMW.xml, UV-DMW.xml, UU-DMW.xml

- Download ‘Project transactions’ per project (for the current accounting year) in excel format

  FG \> Tansactierapporten \> Transacties

  Download these as ‘Transacties-\<PROJNR\>.xls’
  As an example: ‘Transacties-FFI230414.xls’ or ‘Transacties-OZ10097.xls’

- Download ‘Budgetboekingen’ for the FFP and FFI projects in excel format (has to be done in the year of the start, or you can select ‘over
  alle boekjaren heen’)

  FG \> Tansactierapporten \> Budgetboekingen

  Name these: ‘Budgetboekingen-\<PROJNR\>.xls

  As an example: ‘Budgetboekingen-FFI230414.xls’

- Download ‘Transacties lonen’ per PI in excel. Select ‘alle
  boekjaren t.e.m. boekjaar’.

  FG \> Tansactierapporten \> Transacties lonen

  Name these: ‘Lonen-Transacties-\<PI-name\>.xml’

  As an example: ‘Lonen-transacties-STJ.xml’

### 2. Complete the input files yourself

- Projects.xlsx : contains an overview of all projects
- Persons.xlsx : contains an overview of all the employees you want to track
- Planning.xlsx : contains an overview of the planning as you maintain it

If the first two do not exist in your folder with all oracle files,
then the first invocation of* finessensual *will create
empty versions of these files. *Finessensual* will also
complain about missing data in those files. Complete them based on the
hints you get.

The latter file is an excel file that you can create by copying the
‘Personnel’ tab blad from the overview that has been generated to a
separate file and update that.

### 3. Run finessensual

This can be simply done, by dragging the folder that contains all (a)
all oracle-generated files and (b) your project, persons and planning
files, onto the finessensual icon that the installation procedure has
planted on your desktop.
You will see that the script starts running and informs you about its
progress.

After the script completed, the result file
*‘financial-overview.xlsx’ *will be
present in the original folder.

Open it, and enjoy!

## C. License <a id="license"></a>

\`finessensual\` is distributed under the terms of the -license.

## D. Warranty <a id="warranty"></a>

None!
