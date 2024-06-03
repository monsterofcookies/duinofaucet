# duinofaucet

To start the faucet you need to host the index and the api app. 

First you will need to host the api with a accessible URL / IP. 

Hosting the api can be done with running this command in the `api` directory. Note that this will not give  you a URL that can be accessed from the internet.

the `--reload` flag is optional. Just so you can change something in the fly without the api going down.

```
uvicorn app:app --reload
```


#
## Now that you have the API running with a URL that is public, lets host the index file for the website UI.

You can do this in two different ways. 

- Locally host it with public URL (Really Easy)

    Just run `php -S 0.0.0.0:<your desired port>`. I'd say go with port 8080 as 8000 will be used by the API.


- Host it on a cloud provider. (Difficulty is based on the provider)

    If you host is in providers like render or vercel it is easy just point your source to the `index` directory and the site should be live after building.


#
## Contributing 

If you want to add a new feature or have already develeoped a new feature and want it to be the part of a centralized repo pullrequests are more than welcome.
