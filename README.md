# mp3tags
Get and set mp3 ID3 tags

## Working

    get-mp3-info.py *.mp3 info.csv

Creates a csv file `info.csv` with the information of all the mp3 files in the current working directory. Only the following information is retrieved:
 `tracknumber`, `file`, `title`, `artist`, `album`, `genre`, `date`.

Open and edit the csv file using libreoffice (or any other office suite). To update the changes back to the mp3 files run the command

    set-mp3-info.py info.csv

