# s-drive

My app, s-drive is a web application that proactively determines and informs users of the high accident risk areas along a route from one location to another. It is targeted towards drivers, cyclists, and walkers in order to increase traffic accident awareness and road safety.

The app is based on a systemic approach to safety. The Federal Highway Association defines this as “acknowledg\[ing\] crashes alone are not always sufficient” to evaluate the risk of a location. The number of crashes in an area might be influenced by having a high or low amount of traffic and not a direct indicator of accident risk. Additionally, the nature of accidents is random and without years of accident data in a location, that analysis is not meaningful. Instead, identifying which physical road features (number of lanes, lane width, surface type, etc.) contribute most to accidents proves to be a more effective method of risk evaluation. Doing so allows for any location, accident history or not, to be evaluated simply based on its physical features.

Using the random forest algorithm and data from the Highway Safety Information System (maintained by the NHTSA), I trained a machine learning model that captured the patterns between road features and accidents on the target variable of accident severity. This variable is a research backed indicator of accident risk and can be used to quantify risk in real time in the app.

The app uses the Google Maps API with React.js for a simple and familiar interface that allows for very fast use. One of the features is the ability to switch between the modes of travel. The users can select whether they want to drive, walk, or cycle and select the origin and destination. The app automatically takes into account different routes based on the mode of travel.

When the route is generated, each location on it is passed to the machine learning model, which accesses the current weather, time of day, and light conditions and also the associated road features. It returns the accident risk, and if the risks are high enough, the locations are displayed on the route as markers for the user to note and view in Street View as well.

With such a fast and easy way to assess the high risk locations along the routes, hopefully our roads will become a safer place for everyone.

Note: Current Google Maps API and OpenWeatherMap API keys are not active. Additionally, due to the confidentiality of data used to train the model, certain files are hidden. 

## Setup Instructions

### Install Required Python Modules

```bash
pip install -r requirements.txt
```
### Start Web Server

To start the web server you need to run the following sequence of commands.

```bash 
cd "s-drive-app\rtaps-controller"
```
Next run the django web server.
```bash
python manage.py runserver
```

### Install file loader and image loaders from webpack
npm install image-webpack-loader --save-dev --legacy-peer-deps
npm install --save-dev file-loader --legacy-peer-deps

### [Install Node.js](https://nodejs.org/en/)

### Install Node Modules

First cd into the ```frontend``` folder.
```bash
cd frontend
```
Next install all dependicies.
```bash
npm i
```

### To Make Migrations and Migrate
First cd into the ```rtaps_controller``` folder.
```bash
cd rtaps_controller
```
Then make the migrations.

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

### Compile the Front-End

Run the production compile script
```bash
npm run build
```
or for development:
```bash
npm run dev
```

### To install react google maps api
npm i -S @react-google-maps/api --legacy-peer-deps

### To install FontAwesome Icons
npm install react-icons --legacy-peer-deps

### Install react-geocode
npm i react-geocode --legacy-peer-deps

### Install modal
npm install react-modal --legacy-peer-deps
