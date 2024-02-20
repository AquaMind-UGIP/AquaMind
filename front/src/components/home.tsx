import { useState, useEffect, useCallback } from "react";
import { useJsApiLoader, GoogleMap, Marker, LoadScript } from "@react-google-maps/api";

const Home = () => {
    const container = {
        width: "75%",
        height: "500px"
      };
      
    const position = {
    lat: 24.4064,
    lng: 124.1754
    };

    const API_KEY = process.env.REACT_APP_GOOGLE_MAP

    if (!API_KEY) {
        return <div>Error: Google Maps API Key is not defined.</div>;
    }

    return (
    <>
        <h2>React_Google Map_Sample</h2>
        <div className="wrap">
        <LoadScript googleMapsApiKey={API_KEY}>
            <GoogleMap mapContainerStyle={container} center={position} zoom={15}>
            </GoogleMap>
        </LoadScript>
        </div>
    </>
    )
  }
  export default Home;
