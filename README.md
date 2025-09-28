# Finn: Your AI "Finn"ancial Advisor
## Inspiration
The inspiration for **Finn** came from our own lives as first-year college students. This is our first time being away from home, and our first time managing our own money without much oversight. This additional freedom comes with questions and headaches, that serves as obstacle for new banking clients. Bankers are often inaccessible for small questions and are not heavily personalized and that is where Finn comes in.

## What it does
Finn serves as a general purpose financial advisor, and breaks down the early hurdles for new clients. Finn presents recent transaction data, highlights your monthly spending, and provides you with helpful budgeting tips. 

## How we built it
### Using Nessie API
The majority of Finn is built in Python with implementation of Capital One's Hackathon API, Nessie. The Nessie API is used to store the user's transaction data, and allow it to be accessible across the project. The use of the API also enables scalability and future improvements that will be detailed further. The Nessie API made fetching the user's data easy, and allowed for easier organization of data across the project. 
### Using Streamlit
After the API was used to create the data for our customers, the next step was the dashboard for the user. The dashboard was created in the Streamlit library with Python, allowing for a stylistic website in a timely manner. CSS was implemented with Streamlit in order to make the site even more aesthetically pleasing and improve user satisfaction.
### Using Gemini
The next part of the project was actually implementing the AI chatbot. This was done using Google Gemini's API. The AI was trained to specifically focus on financial questions and provide information relevant to the user's transactions and purchases

## Challenges we ran into
As with any long term there were a number of issues we ran into. Using the Nessie API took time to understand to implementation and learn exactly how to utilize its features. Understanding how to create the data and updates served a first hurdle

Creating the website, also required gaining a deeper understanding of Streamlit and its capabilities. Debugging, ensuring everything made sense served as another challenge. Finally, fitting the Gemini API to our use case was another challenge, that required a lot of troubleshooting.

By far the biggest challenge was combining everything into one final product to be shipped out. Working in a group together on a single project like this has been a new experience, and fitting all the components into the website, was more of a struggle than anticipated. Everything from the dashboard, back-end data, AI agent, needed to work together seamlessly and managing that was especially challenging

## Accomplishments that we're proud of
This is the first ever full Hackathon project that any of us have completed. From start to finish we have forced to push an idea to completion, a concept foreign to all of us. A lot of the tools we used were foreign to us as well. That sense of having created something on your own is so incredibly rewarding and we are not only proud of our work, but also each other. 

## What we learned
Beyond learning new Python libraries and API's, we learned how to work together in a team and truly create something. Learning how to collaborate to use Git as a team, and develop in a timed manner all made an ideal learning environment for all of us to grow our skills and make even greater projects in the future.

## What's next for Finn: Your AI "Finn"ancial Advisor
Because Finn is very basic right now, there is a lot of room for the program to grow. The next step we would like to add is user input. Currently Finn, is based on sample, realistic hardcoded data. In the future we would like to add security and bank account connection, or allow users to input their own purchases. This comes with a variety of necessary parts, including a user-side input dashboard and account creation, security and encryption when managing real purchases, and scalability with a database so that each login is linked to a specific account.
