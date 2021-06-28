# Deployment

**Deployment on Heroku**

This project was developed using Gitpod, committed to git and pushed to Github using the built-in functionality.

It was then deployed to Heroku.

1. Create an account or log into [Heroku](https://www.heroku.com).
2. Navigate to Create New App within the New dropdown.
3. Enter App name and select a region

![image](https://user-images.githubusercontent.com/76033080/121817372-5f7ff180-cc81-11eb-90d5-4cb613c61c8d.png)

4. Reveal the Config Variables and enter the following information:
* IP
* SECRET_KEY
* PORT
* MONGO_DB (database name)
* MONGO_URI (taken from Mongo DB)

![image](https://user-images.githubusercontent.com/76033080/121817444-cd2c1d80-cc81-11eb-9ebf-a1c5b0857ee1.png)

5. Connect using Github (if appropriate)

![image](supporting_docs/heroku.png)

6. Select the branch for deployment

![image](https://user-images.githubusercontent.com/76033080/121817469-edf47300-cc81-11eb-84ed-492aae305e88.png)

7. Deploy. The app can now be viewed live.

![image](https://user-images.githubusercontent.com/76033080/121817476-f9479e80-cc81-11eb-9f4b-07ffad140612.png)