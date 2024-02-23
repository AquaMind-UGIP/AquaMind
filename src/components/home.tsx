import { useState, useEffect } from "react";
import { useJsApiLoader, GoogleMap, LoadScript, Circle } from "@react-google-maps/api";
import Modal from 'react-modal'
import Header from "./Header";
import * as fs from 'fs';

const Home = () => {
  const [modalIsOpen, setModal] = useState(true);
  const openModal = () => {
      setModal(true);
  };
  const closeModal = () => {
      setModal(false);
  };

  const topBackground: React.CSSProperties = {
    background: 'rgb(0,0,0) linear-gradient(0deg, rgba(0,0,0,1) 0%, rgba(0,114,255,0.7) 100%)',

  };

  const [map, setMap] = useState<google.maps.Map | null>(null);

  const API_KEY = process.env.REACT_APP_GOOGLE_MAP
  if (!API_KEY) {
      return (
          <div className="h-screen flex justify-center items-center">
              Error: Google Maps API Key is not defined.
          </div>
      );
  }

  const container = {
      width: "60%",
      height: "80vh"
  };

  const mapCenter = {
      lat: 24.4664,
      lng: 124.2054
  };

  const mapOptions = {
      mapTypeId: "satellite",
      mapTypeControl: false,
      streetViewControl: false,
      restriction: {
          latLngBounds: {
              north: 24.7664,
              south: 24.1664,
              east: 124.7054,
              west: 123.7054,
          },
          strictBounds: true
      },
  };

  const circleOptions = {
    strokeColor: "rgb(255, 0, 0)",
    strokeOpacity: 1,
    strokeWiehgt: 2,
    fillColor: "rgb(255, 0, 0)",
    fillOpacity: 1,
    visible: true,
    radius: 150000
  };
  
  const onLoad = (map: google.maps.Map) => {
    setMap(map);
  };

  const modalStyle: Modal.Styles = {
    overlay: {
        position: 'fixed',
        top: 0,
        left: 0,
        backgroundColor: 'rgba(0, 0, 0, 1)',
    },
    content: {
      background: 'none',
      border: 'none',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      width: '100%',
      height: '100%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    },
};

  return (
    <div>
      <Modal 
        isOpen={modalIsOpen}
        onRequestClose={() => setModal(false)}
        style={modalStyle}
        closeTimeoutMS={200}
      >
        <div className="flex flex-col items-center">
          <div className="flex flex-col items-center">
            <img src="logo_black.png" className="h-96"/>
            <button onClick={closeModal} className="text-3xl text-gray-300 bg-gray-700 hover:bg-black px-5 py-1 rounded-lg">
              Get Started
            </button>
          </div>
          <div className="text-gray-300 text-3xl mt-12">
              {/* AquaMind is available at */}
          </div>
        </div>
      </Modal>
      <div className="App None h-screen" id="top">
        <Header />
        <div className="h-screen flex justify-center items-center" style={topBackground}>
          <LoadScript googleMapsApiKey={API_KEY}>
            <GoogleMap
              mapContainerStyle={container}
              center={mapCenter}
              zoom={11}
              options={mapOptions}
              onLoad={(map: google.maps.Map) => {
                const circle = new google.maps.Circle({
                  center: mapCenter,
                  strokeColor: "rgb(255, 0, 0)",
                  strokeOpacity: 1,
                  strokeWeight: 2,
                  fillColor: "rgb(255, 0, 0)",
                  fillOpacity: 1,
                  visible: true,
                  radius: 200,
                  map: map
                });
              }}
            >
            </GoogleMap>
          </LoadScript>
          <div className="flex flex-col">
            <button className="text-3xl text-gray-300 bg-gray-900 hover:bg-black px-5 py-1 rounded-lg">
              地図に切り替えるボタン
            </button>
            <button className="text-3xl text-gray-300 bg-gray-900 hover:bg-black px-5 py-1 rounded-lg">
              衛星画像に切り替えるボタン
            </button>
            <button className="text-3xl text-gray-300 bg-gray-900 hover:bg-black px-5 py-1 rounded-lg">
              範囲選択するボタン
            </button>
            <button className="text-3xl text-gray-300 bg-gray-900 hover:bg-black px-5 py-1 rounded-lg">
              海草分布確率20%
            </button>
            <button className="text-3xl text-gray-300 bg-gray-900 hover:bg-black px-5 py-1 rounded-lg">
              海草分布確率40%
            </button>
            <button className="text-3xl text-gray-300 bg-gray-900 hover:bg-black px-5 py-1 rounded-lg">
              海草分布確率60%
            </button>
            <button className="text-3xl text-gray-300 bg-gray-900 hover:bg-black px-5 py-1 rounded-lg">
              海草分布確率80%
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
