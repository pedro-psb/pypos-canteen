# Pypos Canteen - A canteen Point of Sale
[Live Demo](https://pedro-psb.github.io/posts/projects/) | [Video Walkthrought](https://pedro-psb.github.io/posts/projects/)

Pypos is a Point of Sale web application aimed to be easily implemented in a small scholar canteen with ease. The key features are cashless payment (a user credit system), basics and insightful financial reporting and offline support (not implemented in this this version yet).

This project was born when my girlfriend was working on a scholar canteen that didn't have any point of sale software and which accepeted payment on credit. It was a mess and she was getting upset. We didn't find a good and affordable service that suited the canteen needs, so back then I made a quick solution with Airtable.

Now she doesn't work there anymore, but as I was quite familiar with the requisites, I've decided to go on for learning purposes and to submit it as the final project on the CS50 course. I didn't manage to make the UX and features as good as I wanted, but I may work on future releases.

### Design and Implementation considerations

The project was implemented using Flask and Sqlite3. Later on I started using pydantic aswell, a helpful library used for data validation.

#### Framework and database
Flask and Sqlite were choosen for some specific reasons. First, they were the tools taught on CS50 course, so I it made sense to just use them. Then, flask is very simple and, while using some other framework like Django would make some authenticaion/admin tasks more easy, I could learn more by building certain structures from scratch, like the acess of control schema and logic. On the sqlite side, it is known that it isn't well suited for web development, but it was ok as the app wasn't intended for real production environment (at least for this first version).

#### Other packages

Well, I just used pydantic as an external library. I was doing a lot of type checking on form input, just to see if it was an int, or a str. When I found out about pydantic I found it very handy. It uses a dataclass strucutre to define data and provides on-the-fly type conversion and validation using only type hints. Besides that, it provides several validation utilities that would make my code a lot more organized. I then started being more conviced on the usefulness of type hints, because my code was growing and I found myself sometimes needing those hints on some parts of the code :grin:

#### Deployment

On deployment phase I decided to go with AWS Elastic Beanstalk because it was quite managed. I considered renting a VPS and learn to setup the server, but it would be an unecessary overhead at the moment as I was dealing with so many new things at once. But still, I had some issues that almost made me give up of either EB or sqlite.

AWS EB works by agregating AWS services, namely EC2 for computing, S3 for storage and ELB for load balancing, to name a few. If I was using a regular client/server database, like PostgreSQL or MySQL, there is yet another AWS service that would run just the DB server. But sqlite wouldn't work there, because it doesn't have a server process, instead it just writes data directly to a file. Saving the sqlite file on S3 wasn't a good option, because it doesn't behave like a regular filesystem (it could work as one, but it wouln't be so trivial). Finally, I could save it directly on the EC2 instance, which is where the app actually runs. This way I wouldn't be able to scale, because duplicated computing instances would have different data, which again wouldn't be a problem in my case. But even if I used only one instance, I was concerned that the data would be too ephemeral, because everything is wiped out on instance reload. But then, for this release, I decided it was ok too, as I just needed a demo site and no real production data need to persist for more than a few days.

And now I have a very good refactoring exercise: to change from sqlite to a postgresql/mysql :smile:


### Run locally

(...)

### Deploy

(...)
