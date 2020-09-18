# BeNice
A Python program that detects when a Reddit user is being rude.

Uses spacy NLU API to detect when someone is being rude. Outputs a list of comments that are deemed to be "rude" along with number of rude comments.

To Use:

You need to create an account on Reddit and create a script application here https://www.reddit.com/prefs/apps/

Then take the id and secret of the application plus the username and password of the account you created and put them in the CONFIG.txt file.

Creates a file called rude_output.txt will all rude comments found.



## Usage
```
python be_nice.py -u <reddit username>
```

## Output

```
=== Please BeNice! ===

id_string is: [redacted]
secret_string is: [redacted]

Searching posts for user /u/[reddit_username]...


This may take a while...

Writing to output file...
Number of rude posts: 25
Total number of posts: 999

Rude percentage: 2.502

Congrats! This user is not that rude.


Exiting.
```
