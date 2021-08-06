
# Rover with Analyzer

Main idea behind this project is to explore and analyze places, especially which are inaccessible to humans.

this project contains algorithms to analyze the captured images, user interface to control it. 
User interface consists of different buttons to control the mobility and camera screen to look at the surroundings of the rover.

## Measure size of objects in an image using OpenCV 

The project has a script to read an image and based on the dimensions of a reference object find the dimensions of other objects in a scene. The reference object must be the leftmost object in the scene. In sample images given, a box of dimension 2cm x 2cm is taken as a reference object.

## Texture analysis done using canny edge detection 

The Canny edge detector is an edge detection operator that uses a multi-stage algorithm to detect a wide range of edges in images. It an image processing method used to detect edges in an image while suppressing noise.It extracts useful structural information from different vision objects and dramatically reduce the amount of data to be processed.

## Screenshots
### GUI


<table>

  <tr>
    <td valign="top"><img src="/screenshots/window1.png?raw=true"  width="500" height="300">
  <figcaption>Window-1 (Controller)</figcaption></td>
   
  <td valign="top"><img src="/screenshots/window2.png?raw=true"  width="500" height="300">
    <figcaption>Window-2 (Analyzer)</figcaption></td>

  </tr>
 
  <tr>
    <td valign="top"><img src="/screenshots/imgToAnalyze.JPG?raw=true"  width="500" height="300">
    <figcaption>Objects to analyze</figcaption></td>
  <td valign="top"><img src="/screenshots/result.png?raw=true"  width="500" height="300">
    <figcaption>Analyzed objects</figcaption></td>
 </tr>
 
 </table>










## License

[MIT](https://choosealicense.com/licenses/mit/)

  
