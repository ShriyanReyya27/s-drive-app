import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import TextField from "@material-ui/core/TextField";
import { ButtonGroup, Input, Modal, Typography } from "@material-ui/core";
import { Box } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { IconButton } from "@material-ui/core";
import { FaBiking, FaLocationArrow, FaTimes, IoSettings } from "react-icons/fa";
import { IoSettingsSharp } from "react-icons/io5";
import { useRef } from "react";
import { useParams } from "react-router-dom";
import { FaHome } from "react-icons/fa";
import carIcon from "/static/images/gps-navigation.png";
import { useEffect } from "react";
import { AiFillCar } from "react-icons/ai";
import { FaCircleInfo } from "react-icons/fa6";
import { AiFillCloseCircle } from "react-icons/ai";
import {GrBike} from "react-icons/gr"
import {FaWalking} from "react-icons/fa"
import {AiFillWarning} from "react-icons/ai"
/*Reference - https://medium.com/@allynak/how-to-use-google-map-api-in-react-app-edb59f64ac9d*/

import {
  GoogleMap,
  useLoadScript,
  Marker,
  Autocomplete,
  DirectionsRenderer,
  DirectionsService,
  InfoWindow,
} from "@react-google-maps/api";

import {
  setKey,
  setDefaults,
  setLanguage,
  setRegion,
  fromAddress,
  fromLatLng,
  fromPlaceId,
  setLocationType,
  geocode,
  RequestType,
} from "react-geocode";


const useStyles = makeStyles((theme) => ({
  root: {
    "& > *": {
      margin: theme.spacing(1),
    },
  },
  mapContainer: {
    position: "relative",
    width: "100%",
    height: "100%",
  },
  parent: {
    position: "absolute",
    zIndex: 0,
    width: "100%", // or you can use width: '100vw'
    height: "100%",
  },
  directionPanel: {
    zIndex: 1,
    backgroundColor: "white",
    margin: 5,
    padding: 10,
    width: 600,
    borderRadius: 20,
  },
  userPanel: {
    zIndex: 1,
    backgroundColor: "white",
    margin: 5,
    padding: 5,
    width: 320,
    borderRadius: 20,
  }
}));

const infoModal = {
  position: "absolute",
  top: "30%",
  left: "70%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

const center = { lat: 36.19592357014476, lng: -79.36215114119307 };


const mapContainerStyle = {
  width: "100vw",
  height: "100vh",
};
const libraries = ["places"];

/****START OF FUNCTION DEF*********************** */
function RoadSafetyMap() {
  const classes = useStyles();
  const navigate = useNavigate();
  const { userName } = useParams();

  const travelStates = ["DRIVING","WALKING", "BICYCLING"]

  const [map, setMap] = useState(/** @type google.maps.Map */ (null));
  const [directionsResponse, setDirectionsResponse] = useState(null);
  const [distance, setDistance] = useState("");
  const [duration, setDuration] = useState("");
  const initialState = [];
  const [markers, setMarkers] = useState(initialState);
  const [activeMarker, setActiveMarker] = useState(null);
  const [mapCurrentLocation, setMapCurrentLocation] = useState(center);
  const [useTracking, setUseTracking] = useState(false);
  const [infoShown, setInfoShown] = useState(false);
  const [travelState, setTravelState] = useState(travelStates[0]);

  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const addMarker = (newMarker) => {
    setMarkers((current) => [...current, newMarker]);
  };

  /** @type React.MutableRefObject<HTMLInputElement> */
  const originRef = useRef();
  /** @type React.MutableRefObject<HTMLInputElement> */
  const destinationRef = useRef();

  const travelStateRef = useRef();
  travelStateRef.current = travelState;

  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: "AIzaSyDU0GyhTfbYcx9M2OcyUYWfgi1xQmjGi0s",
    libraries,
  });

  if (loadError) return "Error";
  if (!isLoaded) return "Loading...";


  setDefaults({
    key: "AIzaSyDU0GyhTfbYcx9M2OcyUYWfgi1xQmjGi0s", // Your API key here.
    language: "en", // Default language for responses.
    region: "es", // Default region for responses.
  });

  async function calculateRoute(e) {
    //set markers to empty
    setMarkers(initialState)
    if (originRef.current.value === "" || destinationRef.current.value === "") {
      return;
    }

    //get user input
    console.log("Origin:" + originRef.current.value);
    console.log("Destination:" + destinationRef.current.value);
    const directionService = new window.google.maps.DirectionsService();

    //set travel mode based on button state
    const results = await directionService.route({
      origin: originRef.current.value,
      destination: destinationRef.current.value,
      travelMode: window.google.maps.TravelMode[travelState],
    });

    //calculate route-------------------------------------------------
    setDirectionsResponse(results);
    setDistance(results.routes[0].legs[0].distance.text);
    setDuration(results.routes[0].legs[0].duration.text);
    console.log("These are the Lat Lng in the route");
    let steps = results.routes[0].legs[0].steps;
    console.log(steps[0].start_location.toString());
    console.log(steps.length);
    //This array is used to pass to the model.
    const routeData = [];

    for (let i = 0; i < steps.length; i++) {
      let routeAddress = {
        lat: "",
        lng: "",
        route: "",
        city: "",
        county: "",
        establishment: "abc",
      };
      console.log("Step " + i + " " + steps[i].path.toString());
      let lat = steps[i].start_location.lat();
      let lng = steps[i].start_location.lng();
      console.log("Lat and Long returned:" + lat + lng);
      fromLatLng(lat, lng)
        .then(({ results }) => {
          console.log(results[0]);
          routeAddress.lat = lat;
          routeAddress.lng = lng;

          let address = results[0].address_components;
          for (let j = 0; j < address.length; j++) {
            let addrTypes = address[j].types;
            //Get the address components of types - 'route', 'locality' and 'administrative_area_level_2'
            if (addrTypes.includes("route")) {
              routeAddress.route = address[j].short_name;
            } else if (addrTypes.includes("locality")) {
              routeAddress.city = address[j].short_name;
            } else if (addrTypes.includes("administrative_area_level_2")) {
              routeAddress.county = address[j].short_name;
            } else if (addrTypes.includes("establishment")) {
              routeAddress.establishment = address[j].short_name;
            }
          }
          calculateAccidentProbability(routeAddress);
        })
        .catch(console.error);
    }
  }

  async function calculateAccidentProbability(routeAddress) {
    if (
      routeAddress.county != "" &&
      (routeAddress.route != "" || routeAddress.establishment != "")
    ) {
      console.log(
        "Route Address pushed to RTAPS: Route:" +
          routeAddress.route +
          " County:" +
          routeAddress.county +
          " Establishment:" +
          routeAddress.establishment +
          " Lat:" +
          routeAddress.lat +
          " Lng:" +
          routeAddress.lng
      );
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(routeAddress),
      };
      await fetch("/rtaps/api/sdrive-query", requestOptions)
        .then((response) => response.json())
        .then((data) => handleMarkerUpdate(data));
    }
  }

  function handleMarkerUpdate(data) {
    //use marker and infobox to show the data, the data is in the form of lat, lng, and proba

    if (parseFloat(data.accident_probability) > 0.4) {
      console.log(
        "Marker data received:" +
          data.lat +
          " " +
          data.lng +
          " " +
          data.accident_probability
      );
      let new_id = markers.length + 1;
      let marker = {
        id: { new_id },
        position: { lat: data.lat, lng: data.lng },
        proba: data.accident_probability,
        road_name: data.road_name
      };

      addMarker(marker);
      markers.map((obj) =>
        console.log(
          "Marker data updated:" + obj.id + " " + obj.position + " " + obj.proba
        )
      );
    }
  }

  function clearRoute() {
    setMarkers(initialState);
    setDirectionsResponse(null);
    originRef.current.value = "";
    destinationRef.current.value = "";
    setDistance("");
    setDuration("");
  }

  function goHome() {
    navigate("/rtaps/home");
  }

  function changeTravelState(){
    let index = travelStates.indexOf(travelState);
    let newIndex = (index + 1) % 3;
    console.log("Before updating state:", travelStateRef.current);
    setTravelState(travelStates[newIndex], printCurrentState);// Access the updated value here
    console.log("Current state:", travelStates[newIndex]);
    
    
  }
  
  function printCurrentState(){
    console.log("Current state:", travelStateRef.current);
  }
  function showInfo() {
    setInfoShown({ infoShown: true });
    console.log("open");
  }

  function closeInfo() {
    setInfoShown(!infoShown);
    console.log("close");
  }

  function toggleInfo() {
    setInfoShown(!infoShown);
    console.log("toggle");
  }

  const handleActiveMarker = (marker) => {
    if (marker === activeMarker) {
      return;
    }
    setActiveMarker(marker);
  };

  //GPS Location Tracking
  const options = {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0,
  };
  function error(err) {
    console.warn(`ERROR(${err.code}): ${err.message}`);
  }

  function startTracking() {
    /*navigator.geolocation.getCurrentPosition(
      (position) => {
        const currentLocation = {
          lat: parseFloat(position.coords.latitude),
          lng: parseFloat(position.coords.longitude),
        };
        console.log(currentLocation);
        //mapCurrentLocation.push(currentLocation);
        //updateMapCurrentLocation(currentLocation);
        setMapCurrentLocation({...mapCurrentLocation,lat:currentLocation.lat,lng:currentLocation.lng});
        console.log("After update", mapCurrentLocation);
        
      },
      error,
      options
    );*/
    const position = navigator.geolocation.getCurrentPosition(error, options);
    const currentLocation = {
      lat: parseFloat(position.coords.latitude),
      lng: parseFloat(position.coords.longitude),
    };
    console.log(currentLocation);
    //mapCurrentLocation.push(currentLocation);
    //updateMapCurrentLocation(currentLocation);
    setMapCurrentLocation(currentLocation);
    console.log("After update", mapCurrentLocation);
  }

  const updateMapCurrentLocation = (position) => {
    console.log("Coordinate", position);
    console.log("Before updating location:", { mapCurrentLocation });
    setMapCurrentLocation({
      ...mapCurrentLocation,
      lat: position.lat,
      lng: position.lng,
    });
    console.log("After update", mapCurrentLocation);
  };

  return (
    <Box className={classes.parent}>
      <Box className={classes.parent}>
        <GoogleMap
          mapContainerStyle={mapContainerStyle}
          zoom={15}
          center={center}
          options={{
            fullscreenControl: false,
          }}
          onLoad={(map) => setMap(map)}
        >
          {markers.map(({ id, position, proba, road_name }) => (
            <Marker
              key={id}
              position={position}
              icon={<AiFillWarning/>}
              onClick={() => handleActiveMarker(id)}
            >
              {activeMarker === id ? (
                <InfoWindow onCloseClick={() => setActiveMarker(null)}>
                  <div>{road_name}</div>
                </InfoWindow>
              ) : null}
            </Marker>
          ))}

          {directionsResponse && (
            <DirectionsRenderer directions={directionsResponse} />
          )}
        </GoogleMap>
      </Box>

      <Grid container spacing={1} direction="row">
        <Grid
          container
          spacing={1}
          alignItems="right"
          justifyContent="flex-end"
          style={{ width: "70%" }}
        >
          <Box className={classes.directionPanel}>
            <Grid
              container
              spacing={1}
              alignItems="right"
              justifyContent="flex-end"
            >
              <Grid item align="center">
                <Autocomplete>
                  <TextField
                    id="origin"
                    required={true}
                    variant="outlined"
                    label="Origin"
                    inputProps={{
                      style: { textAlign: "center", width: 200, height: 10 },
                    }}
                    inputRef={originRef}
                  />
                </Autocomplete>
              </Grid>
              <Grid item align="center">
                <Autocomplete>
                  <TextField
                    id="destination"
                    required={true}
                    variant="outlined"
                    label="Destination"
                    inputProps={{
                      style: { textAlign: "center", width: 200, height: 10 },
                    }}
                    inputRef={destinationRef}
                  />
                </Autocomplete>
              </Grid>
              <Grid item align="center">
                <ButtonGroup>
                  <Button
                    color="primary"
                    variant="contained"
                    onClick={calculateRoute}
                  >
                    Route
                  </Button>
                  <IconButton aria-label="center back" onClick={clearRoute}>
                    <FaTimes style={{ color: "black", fontSize: "0.9em" }}/>
                  </IconButton>
                </ButtonGroup>
              </Grid>
            </Grid>
            <Grid container spacing={1} direction="row">
              <Grid item xs={5} align="left">
                <Typography paragraph>Distance: {distance}</Typography>
              </Grid>
              <Grid item xs={5} align="left">
                <Typography paragraph>Duration: {duration}</Typography>
              </Grid>
              <Grid item xs={2} align="right">
                <IconButton
                  aria-label="center back"
                                  
                  onClick={() => {
                    map.panTo(center);
                    map.setZoom(15);
                  }}
                >
                  <FaLocationArrow style={{ color: "red", fontSize: "1.0em" }}/>
                </IconButton>
              </Grid>
            </Grid>
          </Box>
        </Grid>
        <Grid
          container
          alignItems="right"
          justifyContent="flex-end"
          style={{ width: "30%", height: "30%" }}
        >
          <Grid
            container
            spacing={0}
            align="right"
            justifyContent="flex-end"
            style={{ height: "30%" }}
          >
            <Box className={classes.userPanel}>
              <Grid item xs={12}>
                <IconButton aria-label="center back" onClick={handleOpen}>
                  <FaCircleInfo
                    style={{ color: "orange", fontSize: "1.20em" }}
                  />
                </IconButton>

                <Modal
                  open={open}
                  onClose={handleClose}
                  aria-labelledby="modal-modal-title"
                  aria-describedby="modal-modal-description"
                >
                  <Box sx={infoModal}>
                    <Typography
                      id="modal-modal-title"
                      variant="h6"
                      component="h2"
                    >
                      How to use:
                    </Typography>
                    <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                      <ul>
                      <li>
                          Click on the travel icon to change your mode of travel. This will update how your route is created.
                        </li>
                        <li>
                          Enter your starting and ending location and click
                          "Route" to generate the route.
                        </li>
                        <li>
                          The locations of high risk will appear as markers on
                          the map; click on them to view their information.
                        </li>
                        <li>
                          If you would like, use the droppable person to view
                          the location in Street View.
                        </li>
                        <li>Travel safe!</li>
                      </ul>
                    </Typography>
                  </Box>
                </Modal>

                <IconButton aria-label="center back" onClick={goHome}>
                  <FaHome style={{ color: "darkblue", fontSize: "1.25em" }} />
                </IconButton>

                <IconButton aria-label="center back" onClick={changeTravelState}>
                  {travelState === travelStates[0] ? <AiFillCar style={{ color: "green", fontSize: "1.25em" }} />
                  : (travelState === travelStates[1] ? <FaWalking style={{ color: "blueviolet", fontSize: "1.25em" }} />
                                                     : <FaBiking style={{ color: "red", fontSize: "1.25em" }}/>)}
                </IconButton>

                <Button color="secondary" variant="contained" style={{borderRadius: 12}}>
                  Welcome {!!userName ? userName : "Guest"}
                </Button>
              </Grid>
            </Box>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
}

export default RoadSafetyMap;
