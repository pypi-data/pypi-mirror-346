**[Finessensual]{.underline}**

[Finessensual is a python script that allows the conversion of Oracle
financial transaction reports into an overview that is useful for
research groups (around one or more Pis). Its name is contraction (or
you might call it a contraption) of 'finance', 'essential' and
'UA'.]{.underline}

**[A. Installation]{.underline}**

*[1. Install the prerequisites]{.underline}*

-   [When on GNU/Linux, UNIX or MAC:]{.underline}

[Install:]{.underline}

-   [libreoffice]{.underline}\
    [(e.g. on Ubuntu: \'sudo apt-get install libreoffice\')]{.underline}

-   [a python 3 interpreter]{.underline}\
    [(e.g. on Ubuntu: \'sudo apt-get install python3\')]{.underline}

[Make sure the libreoffice executable and the python3 executable can be
found based on your PATH environment variable.]{.underline}

-   [When on MS-Windows:]{.underline}\
    [Install:]{.underline}

    -   [libreoffice]{.underline}

[Go to the , download the latest version and install it.]{.underline}\
[(don\'t install libreoffice from the microsoft store, or those b@s!@rds
will charge you for it!)]{.underline}

-   [python]{.underline}\
    [Click on the windows start icon and start typing \'python\' until
    you see as best match \'python, Run command\'. Clicking on that will
    open the microsoft store on the Python page. Click on \'Get\' to
    install python on your machine.]{.underline}

*[2. Install the package itself]{.underline}*

[The finessensual code can be found on .]{.underline}

-   [When on GNU/Linux, UNIX or MAC:]{.underline}\
    [If you have a python interpreter installed on a GNU/Linux, BSD-like
    or UNIX-like workstation that is all you need. You can install the
    package from the command line as follows:]{.underline}

[ \$ pip install --upgrade finessensual]{.underline}

-   [When on MS-Windows]{.underline}\
    [On this platform, unfortunately, users have unlearnt how to install
    software and how to use the command line). Therefore, I spent on of
    me weekends making you a finessensual installer executable that will
    perform the installation and make a desktop icon for
    you.]{.underline}

**[B. Using the package]{.underline}**

*[1. Download all financial files from oracle]{.underline}*

[Start your oracle java application to consult "Financiële
gebruikersrapporten" (below this will be abbreviated as FG) from . If we
say 'download' below, we mean ]{.underline}*[save in one and the same
folder]{.underline}*[.]{.underline}

-   [Download the information on Vlottende Budgetten:]{.underline}

[FG \> Werk voor derde en derdengeld \> Forfaitaire project, BOF, IOF en
activiteiten \> Vlottende Budgetten]{.underline}\
\
[Download all 'vlottende budgetten' (like: AK, AO, RA, WD, WO) in excel
format and name them 'VBTransacties-' + nummer + '.xls'.]{.underline}\
[As an example: 'VBTransacties-AK160007.xls']{.underline}

-   [Download 'Budgets and transactions' related to the PIs that are
    part of the financial overview in excel format]{.underline}

[FG \> Werk voor derden en derdengeld \> Verantwoordingsprojecten \>
Budgetten en transacties]{.underline}

[ Select the PI you want to cover.]{.underline}

[ Select 'excel' as format. This will leave only three buttons active in
the rightmost row:]{.underline}\
[  - Budgetten : download this file and name it
UB-\<PI-name\>.xml]{.underline}\
[  - Vastleggingen : download this file and name it
UV-\<PI-name\>.xml]{.underline}

[ - Uitgaven : download this file and name it
UU-\<PI-name\>.xml]{.underline}\
\
[As an example: UB-DMW.xml, UV-DMW.xml, UU-DMW.xml]{.underline}

-   [Download 'Project transactions' per project (for the current
    accounting year) in excel format]{.underline}

[FG \> Tansactierapporten \> Transacties]{.underline}

[ Download these as 'Transacties-\<PROJNR\>.xls']{.underline}\
[ As an example: 'Transacties-FFI230414.xls' or
'Transacties-OZ10097.xls']{.underline}

-   [Download 'Budgetboekingen' for the FFP and FFI projects in excel
    format]{.underline}\
    [(has to be done in the year of the start, or you can select 'over
    alle boekjaren heen')]{.underline}

[FG \> Tansactierapporten \> Budgetboekingen]{.underline}

\
[Name these: 'Budgetboekingen-\<PROJNR\>.xls]{.underline}

[As an example: 'Budgetboekingen-FFI230414.xls']{.underline}

-   [Download 'Transacties lonen' per PI in excel. Select 'alle
    boekjaren t.e.m. boekjaar'.]{.underline}

[FG \> Tansactierapporten \> Transacties lonen]{.underline}

[Name these: 'Lonen-Transacties-\<PI-name\>.xml']{.underline}

[As an example: 'Lonen-transacties-STJ.xml']{.underline}

*[2. Complete the input files yourself:]{.underline}*

-   [Projects.xlsx : contains an overview of all projects]{.underline}

-   [Persons.xlsx : contains an overview of all the employees you want
    to track]{.underline}

-   [Planning.xlsx : contains an overview of the planning as you
    maintain it]{.underline}

[If the first two do not exist in your folder with all oracle files,
then the first invocation of]{.underline}*[ finessensual
]{.underline}*[will create empty versions of these files.
]{.underline}*[Finessensual]{.underline}*[ will also complain about
missing data in those files. Complete them based on the hints you
get.]{.underline}

[The latter file is an excel file that you can create by copying the
'Personnel' tab blad from the overview that has been generated to a
separate file and update that.]{.underline}

*[3. Run finessensual]{.underline}*

[This can be simply done, by dragging the folder that contains all (a)
all oracle-generated files and (b) your project, persons and planning
files, onto the finessensual icon that the installation procedure has
planted on your desktop.]{.underline}\
[You will see that the script starts running and informs you about its
progress.]{.underline}

[After the script completed, the result file
]{.underline}*[']{.underline}[financial-overview.xlsx]{.underline}[']{.underline}[
]{.underline}*[will be present in the original folder.]{.underline}

[Open it, and enjoy!]{.underline}

**[C. License]{.underline}**

[\`finessensual\` is distributed under the terms of the
-license.]{.underline}

**[D. Warranty]{.underline}**

[None!]{.underline}
