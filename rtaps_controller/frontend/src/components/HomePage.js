import React from "react";
import logo from "/static/images/sdrivelogoWORDSLOWERBEST.png";
import { Grid } from "@material-ui/core";
import { Box, Button, Link } from "@material-ui/core";
import { makeStyles } from "@material-ui/core";
import { useNavigate } from "react-router-dom";


const imageFilePath = "/static/images/sdrivelogoWORDSLOWERBEST.png";
const logoStyle = {
  //backgroundImage: "url(' + require('/static/images/sdrivelogoFULL.png') + ')",
  backgroundImage: `url(${logo})`,
  height: "100vh",
  marginTop: "-70px",
  fontSize: "50px",
  backgroundSize: "cover",
  backgroundRepeat: "no-repeat",
};
const imagesList = [
  {
    id: 1,
    src: logo,
    alt: "SDrive Logo",
  },
];
const useStyles = makeStyles((theme) => ({
  directionPanel: {
    margin: 8,
  },
}));
export default function HomePage() {
  const classes = useStyles();
  const navigate = useNavigate();
  
  function handleCreateProfileClicked(e) {
    navigate("/rtaps/createProfile/");
  }

  function handleGuest(e) {
    navigate("/rtaps/roadSafetyMap");
  }


  return (
    <Grid container direction="row">
      
      <Grid container spacing={1} alignItems="right" justifyContent="flex-end" style={{height:'5%'}}>
        <Grid item align="right">
          <Box className={classes.directionPanel}>
          
            <Button
              color="primary"
              variant="contained"
              onClick={handleCreateProfileClicked}
              style={{borderRadius: 12}}
            >
              Create Profile
            </Button>
          </Box>
        </Grid>
        <Grid item align="right">
          <Box className={classes.directionPanel}>
            <Button              
              style={{color:"white", backgroundColor:"green", borderRadius: 12}}
              variant="contained"
              onClick={handleGuest}
            >
              Guest
            </Button>
          </Box>
        </Grid>
      </Grid>
      
      <Grid item xs={12} align="center">
        {imagesList.map((image) => (
          <img
            key={image.id}
            src={image.src}
            alt={image.alt}
            style={logoStyle}
          />
        ))}
      </Grid>
    </Grid>
  );
}
