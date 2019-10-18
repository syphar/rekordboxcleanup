# rekordboxcleanup
Some scripts to help with managing a rekordbox collection. 

In general this is not (yet) usable as a normal python package with executable. Probably I'll do it at some point, but 
for now this is only the public collection of the code I use regularly.  

# Installation 
Just clone this repository. 
 
# Usage 
I'm using `click`, so you can simply use `python rekordbox.py --help` or (for example) 
`python rekordbox.py trackswithoutplaylist --help` to know more about the usage of the command. 

Rekordbox itself is closed and doesn't offer any API. But regarding the library there is one way out, 
and one way back in. They are not that convenient, but it's enough to do the job. 

So all the commands work in this way. 

## 1. Export library in XML 
By using *File->Export Collection in XML Format* you can export an XML file which contains everything from your library, 
except the music files themselves. 

## 2. Run command 
Run the command you want with the XML file as parameter, perhaps adding an output filename. 

## 2. Re-Import Playlist
Rekordbox can show you an external XML library. For this you have to configure two things in the rekordbox preferences:  

* View: under *Layout*, enable *rekordbox xml* 
* Advanced: under *Database* and *rekordbox xml* set *Imported Library* to the output library path. I usually use the 
  same name all the time. 
  
Now in the list of sources you will find the XML, including a new playlist. This playlist you now can drag&drop to your 
normal library, and voilà. 