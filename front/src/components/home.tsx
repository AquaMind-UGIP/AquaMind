import { useState, useEffect } from "react";
import { useJsApiLoader, GoogleMap, LoadScript, Circle } from "@react-google-maps/api";
import Modal from 'react-modal'

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
      height: "100vh"
  };

  const position = {
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

  const circleOptions: google.maps.CircleOptions = {
    strokeColor: "#FF0000",
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: "#FF0000",
    fillOpacity: 0.35,
    center: position,
    radius: 1000
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
        transition: 'backgroundColor 0.2s ease-in-out',
    },
    content: {
      background: 'none',
      border: 'none',
      // position: 'fixed',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      // backgroundColor: 'white',
      // borderRadius: '8px',
      // padding: '20px',
      // opacity: modalIsOpen ? 1 : 0,
      // transition: 'opacity 0.2s ease-in-out',
      // zIndex: 1000,
      width: '100%',
      height: '100%',
      display: 'flex', // 親要素をflexコンテナにする
      alignItems: 'center', // 子要素を垂直方向に中央寄せ
      justifyContent: 'center', // 子要素を水平方向に中央寄せ
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
      <div className="h-screen flex justify-center items-center" style={topBackground}>
        <LoadScript googleMapsApiKey={API_KEY}>
          <GoogleMap
            mapContainerStyle={container}
            center={position}
            zoom={11}
            options={mapOptions}
            onLoad={onLoad}
          >
            {map && <Circle center={position} options={circleOptions} />}
          </GoogleMap>
        </LoadScript>
      </div>
    </div>
  );
};

export default Home;
