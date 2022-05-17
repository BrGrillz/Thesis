The first step was to get the HTML page using the request library. This library works on the principle of a Postman program, that is, it sends requests to the specified web address. Using the get method, the page was received, and the cookies of a specific account are transmitted in the cookie parameter. The received HTML code must be processed for further work with it. For this purpose, the BeautifulSoup library was used, which formats the HTML for further processing, after which we can use it to search for the required tags. Upon visual analysis of the HTML code, it became clear that the necessary data is located under the script tag. The script tag is intended to describe scripts, and there can be many such tags in one HTML code. Fortunately, YouTube displays IDs of recommended videos in the script tag always at number 40. The resulting script tag block at number 40 is translated into text format, slightly edited with regular expressions and deserialized into Json using the Json library. That is, the first function get_html_data is responsible for receiving the html page, processing it, and eventually it returns the deserialized object.

The second function is called get_array_of_video_id. This function takes an input parameter in the form of a deserialized Json. Through visual analysis, it turned out that the necessary ID videos from the recommendations page are located on a certain path. It is this path that is passed to the variable, to which the iteration cycle is applied, and if a certain parameter is located along the path that consumes the video ID, then this ID is written to the array. Finally, the function returns an array of id videos that are selected on the YouTube recommendation page.

After the first two functions work, we can already get all the necessary data for all the recommended videos, since there is their ID. To access the YouTube API, the get_video_info function was created. The required data is located in such resources as: snippet, statistics and contentDetails. It is necessary to clarify that for requests to the YouTube API, we also need to install the google API python client and create a separate function for connecting to the API. According to the specified parameters, a request to receive data is sent. As a result, the function returns all the required data for further writing to the database.

The next function next_video is, in fact, the starting function of the entire program. It is responsible for calling all other functions. Moreover, it has a limited number of iterations. Within the project, 200 iterations were chosen as the main value. However, there is also a variation on the function that is needed to analyze the theory that short videos are promoted more often than others. In turn, this modification is supplemented with themes, it takes a parameter with the video duration obtained from the API requests function, after which it determines the smallest and longest video duration from the list of recommended videos and makes such a video the next one to send a request for it.

Separately, a small function get_random_video has been taken out that returns a random ID video from the recommendations. This is necessary to simulate the clicks of a user who impartially chooses which video to watch next. The rest of the functionality is related to the database and analysis.

To run this program you nee d to istall requirements.txt

pip install -r /your path to file
