# Ticketing

## About the project
this is a Music recommender system that users can send their intedetes music/voice file and system recommends them 5 similar Music based on that file.

## Project structure:
![structure](https://github.com/pooyatfn/Music-recommender/assets/98226980/e932a71f-9898-4210-b884-114848067160)

### service 1: requestApi
  this service get users voice file and email(written with Flask), insert a row in cloud postgres database(ID, email, status=pending, song_id=null) and get inserted ID. send this ID with user's voice file to cloud object storage and to the cloud rabbitMQ for the processing queue.

![Screenshot 2024-04-04 223350](https://github.com/pooyatfn/Music-recommender/assets/98226980/2b268ee5-4522-4457-a740-6601651ba832)
![Screenshot 2024-04-04 224016](https://github.com/pooyatfn/Music-recommender/assets/98226980/f0cd4c33-057d-4389-8045-360688bde2d3)


### service 2: music recognition
  this service listens for ids in queue. when it get the id, send a request to cloud object storage and download the associated voice file. send this file to the Shazam api for recognizing the music and returns music title and artist. then, send this title and artist to spotify api to get song id of that music and update associated row in database(song_id, status=ready).



### service 3: recommender
  this service listens for ready status in database. when some row's status changes to ready, this service get its songID and sends it to spotify api for get recommended musics. then, send this recommends to the email of that user with mailgun(cloud mail service).

![Screenshot 2024-04-04 231240](https://github.com/pooyatfn/Music-recommender/assets/98226980/0aee6f55-b320-4216-a1f8-d8dfd83471a3)

  all services handle exeptions and save logs for processed tasks and error detection.
  
