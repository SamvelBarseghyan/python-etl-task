# python-etl-task

This is assignment 
[URL](https://b2boost.bitbucket.io/assignments/python-etl/#target_frameworks_tools_and_services)

## How to BUILD and RUN
It assumes that you already have downloaded or cloned repository and you have `docker` installed on your machine.

```bash
# Move into the working directory
cd python-etl-task
```
```bash
# Build dockerfile
docker build . -t etl-app
```

```bash
# Run docker container
docker run -dp 80:80 etl-app
```

## HOW TO USE THE APPLICATION

Click [http://127.0.0.1:80/docs](http://127.0.0.1:80/docs) to navigate to the application Swagger page
Or you can run
```bash
# To call app to get KPIs of the player
$ curl --location --request GET 'http://127.0.0.1:80/players?account_id=639740&name=YrikGood'
{
    "player_name": "YrikGood",
    "total_games": 20,
    "min_kda": 0.5,
    "avg_kda": 2.19,
    "max_kda": 7.4,
    "min_kp": "31.82%",
    "avg_kp": "49.89%",
    "max_kp": "69.57%",
    "game": "Dota"
}
```