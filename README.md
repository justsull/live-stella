# STELLA - fashion content auto tagger Slack command app’
Working at a company with dozens of editors that published over 2k articles a month, a large pain point was having the editors “cleanly” and consistently tag their articles. Go figure the business intelligence team was always struggling to extract any meaningful insights from our content with such poor metadata. Since I was learning machine learning, I decided to train my own NLP model that could accurately auto tag any article an editor wrote. Now I needed a quick and easy way for editors to work with the auto tagger. Since Slack was already widely adopted at our company, I decided a Slack app would be a great platform to leverage to get immediate adoption and feedback. Enter Stella - a fashion content auto tagger Slack command app. Trained on over 20,000 fashion articles and 300 white listed tags, the machine achieved 90% accuracy when tested against the humans. Maybe it will write the articles next.



## Built With

I wrote this app when I was taking the [Fast AI](https://www.fast.ai/) course on machine learning. Some of the biggest motivations to writing this script was to learn how to write NLP models using Tensorflow. Also, I used Django to quickly build an API that could manage the communications between Slack and the nlp model:

* [Tensorflow](https://www.tensorflow.org/) - An open source machine learning framework.
* [Django](https://www.djangoproject.com/) - Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.


## Authors

* **Justin Sullivan** - [Linkedin](https://www.linkedin.com/in/justsull)


## Acknowledgments

* Hat tip to [ml4a-guides](https://github.com/ml4a/ml4a-guides) for providing excellent IPython notebooks and tutorials on Tensorflow.
