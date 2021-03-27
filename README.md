# Ana's version

## Environment:
```
$ pip install -r requirements.txt
```
Create a .env file with the following fields:
- consumerKey
- consumerSecret
- bearerToken
- accessToken
- accessTokenSecret
- DATABASE_URL

And on the terminal, set the variable ENV to 'dev'

Windows:

```set ENV=dev```

Mac:

```export ENV=dev```

```
### example.py
```py
from tweetcollector.collector import collect

collect(5)
```
The function collect will pick an adjective of a text file and start the search. As parameter of collect you put the number of minutes you expect to search. main.py is an example of script, you can run on your prompt by the following command in the directory of the application:
```
python main.py
```
A message as 'collecting tweets with key someadjective' will confirm the correct run.
