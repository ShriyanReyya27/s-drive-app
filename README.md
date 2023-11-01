# Realtime Road Safety Analyzer

## Setup Instructions

### Install Required Python Modules

```bash
pip install -r requirements.txt
```
### Start Web Server

To start the web server you need to run the following sequence of commands.

```bash 
cd "realtime-roadsafety-analyzer\rtaps-controller"
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
