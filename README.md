# metamatic
A Python command line tool intended to find inconsistencies in metadata for audio files.
## Inspiration
I was messing with audio files and their tags when I noticed a discrepency and decided to make something to hopefully detect such errors en masse. I accomplished this task by maintaining a trie for each tag and a fall-back trie using a standard dictionary. Clustering might have been a better solution but I think tries are super cool and just wanted an excuse to use them. Also, who doesn't love Levenshtein distance?
## Notes/to do
* is it worth it to mess with threads?
* formatting considerations and examples encountered in the wild
    * title case
        * Pollywogs Dancing on a Quilt of Faces
    * title case + roman numerals
        * Rio Part XIII
    * title case + roman numerals + lower case??
        * Part IIc
    * all caps
        * KANSAS NSYNC etc
    * all lower
        * alone (Bill Evans)
    * numbers and punctuation
        * 'Spartacus' Love Theme / Nardis
        * Concerto in E Minor, Op. 64
    * diacritics
        * Arvo Pärt
* writing 'corrected' tags
    * tinytag library only supports reading