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

      return (
        <>
          <h2>React_Google Map_Sample</h2>
          <div className="wrap">
            <LoadScript googleMapsApiKey="AIzaSyDROGIsDMxVZxM_cELK7TMmZYRtpe8ELzI">
              <GoogleMap mapContainerStyle={container} center={position} zoom={15}>
              </GoogleMap>
            </LoadScript>
          </div>
        </>
      )
  }
  export default Home;

// const defaultPosition = { lat: 0, lng: 0 }; // 仮のデフォルト位置

// const Home = () => {
//   useEffect(() => {
//     window.scrollTo(0, 0);
//   }, []);

//   console.log("API_KEY:", "AIzaSyDROGIsDMxVZxM_cELK7TMmZYRtpe8ELzI");

//   const { isLoaded, loadError } = useJsApiLoader({
//     googleMapsApiKey: process.env.REACT_APP_API_KEY || "",
//   });

//   const [map, setMap] = useState<google.maps.Map | null>(null);

//   const onLoad = useCallback(function callback(map: google.maps.Map) {
//     setMap(map);
//   }, []);

//   const onUnmount = useCallback(function callback(map: google.maps.Map) {
//     setMap(null);
//   }, []);

//   useEffect(() => {
//     if (map) {
//       const bounds = new google.maps.LatLngBounds(defaultPosition);
//       map.fitBounds(bounds);
//     }
//   }, [map]);

//   return (
//     <div>
//       {loadError ? (
//         <div>Error loading Google Maps</div>
//       ) : isLoaded ? (
//         <GoogleMap
//           mapContainerStyle={{ width: "100%", height: "400px" }}
//           center={defaultPosition}
//           zoom={8}
//           onLoad={onLoad}
//           onUnmount={onUnmount}
//         >
//           <Marker position={defaultPosition} />
//         </GoogleMap>
//       ) : (
//         <div>Loading...</div>
//       )}
//     </div>
//   );
// };

// export default Home;
