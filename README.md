Simple standalone script to sync subreddit subscriptions between accounts. Mainly used when you want to delete your account and start fresh.

<h1>Usage</h1>
You first need to follow these steps prior to running the script:  

* Go to https://old.reddit.com/prefs/apps/
* Create a new app named new-reddit-account with redirect uri "http://localhost:8080" (this will not matter) and type "script"
* Create a new reddit account and add this new account as a developer to the app you just created.

Now you can run the script like this:

`./new_reddit_account.py --username OLD_USERNAME --password OLD_PASSWORD --app-id APP_ID --app-secret APP_SECRET --new-username NEW_USERNAME --new-password NEW_PASSWORD`

The APP_ID and APP_SECRET are pulled from https://old.reddit.com/prefs/apps/ in the section of the app that you created above.

<h1>Next Steps</h1>

* Make it easier to run. Right now its very annoying to have to set up everything by making an app and whatnot. Would be nice if we could get around this somehow.
* Create an account automatically. Would be cool if we could somehow create the new account automatically instead of the user doing that automatically. Would somehow need to get around the captcha though so might be impossible.
