import React from "react";
import { useState } from "react";
import { useParams } from "react-router-dom";
import { useEffect } from "react";

function RoadSafetyAnalyzer() {
  const [profile, setProfile] = useState({
    first_name: "",
    last_name: "",
    user_name: "",
  });

  const { userName } = useParams();
  useEffect(() => {
    fetch("/rtaps/api/get-user" + "?userName=" + userName)
      .then((response) => response.json())
      .then((data) => {
        setProfile({
          first_name: data.first_name,
          last_name: data.last_name,
          user_name: data.user_name,
        });
      });
  },[]);
  //Use the empty dependency array [] above to define that the useEffect should run only once 
  //Ref -https://www.freecodecamp.org/news/prevent-infinite-loops-when-using-useeffect-in-reactjs/#:~:text=useEffect%20checks%20if%20the%20dependencies,if%20state%20is%20being%20updated.

  return (
    <div>
      <h3>User Profile: {userName}</h3>
      <p>First Name: {profile.first_name}</p>
      <p>Last Name: {profile.last_name} </p>
      <p>User Name: {profile.user_name}</p>
    </div>
  );
}

export default RoadSafetyAnalyzer;
