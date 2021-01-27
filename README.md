#My Climate Change API App

This effort produced a Flask driven API product that allows the user to pull JSON formatted Hawaii precipitation and temperature readings from 9 weather stations located throughout the islands.

The climate starter notebook has been renamed to "climate".

Building the SQLAlchemy ORM queries was pretty straight forward. I had a major challenge getting the datetime module to calculate a 1 year prior date. I struggled getting the text formatted date to be understood by timedelta method. The error message noted I was required to provide the date in an integer format. 

After many failed attempts, I switched to just converting the date text into a date object and then the timedelta(days=365) function worked just fine

The second lessor challenge was getting the groupby to function as required. Several passes eventully lead to a functioning solution.

When producing the summary statistics for the precipitation data there was a small difference between my results and the sample results provide. It appears the sample results include 1 year + 1 day of data 2016-08-23 through 2017-08-23 = 366 days. I left my results with a reading count of 2015 which is 6 less than the sample provided due to the inclusion of the date 2016-08-23.

Building the climate app was a fun exercise and even allowed me to provide some minor flair by taking advantage of what we learned in day 1 Web page development. 

I didn't like the solution for our date input challenge (start and start/end as it was just not elegant. However, it works and presented the trickiest challenge as to how to incorporate picking up user input from a url. 

Time did not permit me to address the bonus questions this round but I will look at them for future skillset enhancement. 

Aloha!

![alt text](https://img1.10bestmedia.com/Images/Photos/374469/GettyImages-1038532990_54_990x660.jpg)