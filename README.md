# LKZ_scraper
Scraper for electronic version of [Academic Dictionary of Lithuanian](http://lkz.lt/).

### Usage

Download dependencies:
```sh
> pip install -r requirements.txt
```

Run the script:
```sh
> python LKZ_scraper.py

Querying letter "A"...
Got 10661 words.
Querying letter "Ą"...
Got 44 words.
Querying letter "B"...
Got 11265 words.

...

Querying letter "Z"...
Got 1952 words.
Querying letter "Ž"...
Got 8360 words.
Saving files to file...
Done!
```
After script finishes up you should see `lkz_words.txt` file in the same directory.

