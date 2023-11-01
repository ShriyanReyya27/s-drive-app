import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import { Link } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const useStyles = makeStyles((theme) => ({
  root: {
    "& > *": {
      margin: theme.spacing(1),
    },
  },
}));

function CreateProfile() {
  const classes = useStyles();
  const navigate = useNavigate();

  const [profile, setProfile] = useState({
    first_name: "",
    last_name: "",
    user_name: "",
  });

  function handleFirstNameChanged(e) {
    setProfile({
      ...profile,
      first_name: e.target.value,
    });
  }

  function handleLastNameChanged(e) {
    setProfile({
      ...profile,
      last_name: e.target.value,
    });
  }

  function handleUserNameChanged(e) {
    setProfile({
      ...profile,
      user_name: e.target.value,
    });
  }

  function handleCreateProfileClicked(e) {
    console.log('from browser'+profile);
    console.log('JSON.stringify'+JSON.stringify(profile));
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(profile),
    };
    fetch("/rtaps/api/create-user", requestOptions)
      .then((response) => response.json())
      .then((data) => navigate("/rtaps/roadSafetyMap/"+data.user_name));
  }

  return (
    <Grid container spacing={1} style={{ height: "50%" }}>
      <Grid item xs={12} align="center">
        <Typography component="h4" variant="h4">
          Create s-drive User Profile
        </Typography>
        <FormControl component="fieldset">
          <TextField
            id="first_name"
            required={true}
            variant="standard"
            label="First Name"
            onChange={handleFirstNameChanged}
            inputProps={{
              max: 50,
              style: { textAlign: "center" },
            }}
          />
          <FormHelperText>
            <div align="center">Please enter your first name</div>
          </FormHelperText>
          <TextField
            id="last_name"
            required={true}
            variant="standard"
            label="Last Name"
            onChange={handleLastNameChanged}
            inputProps={{
              max: 50,
              style: { textAlign: "center" },
            }}
          />
          <FormHelperText>
            <div align="center">Please enter your last name</div>
          </FormHelperText>
          <TextField
            id="user_name"
            label="User Name"
            required={true}
            variant="standard"
            onChange={handleUserNameChanged}
            inputProps={{
              max: 50,
              style: { textAlign: "center" },
            }}
          />
          <FormHelperText>
            <div align="center">Please enter your user name</div>
          </FormHelperText>
        </FormControl>
      </Grid>
      <Grid item xs={12} align="center" direction="column">
        <div className={classes.root}>
          <Button
            color="primary"
            variant="contained"
            onClick={handleCreateProfileClicked}
          >
            Create Profile
          </Button>
          <Button color="secondary" variant="contained" to="/rtaps/home" component={Link}>
            Back
          </Button>
        </div>
      </Grid>
    </Grid>
  );
}

export default CreateProfile;
