import { useState, useEffect, ChangeEvent } from "react";
import { useJsApiLoader, GoogleMap, LoadScript, Circle } from "@react-google-maps/api";
import Modal from 'react-modal'
import Header from "./Header";
import sample_json from './sample_json.json';
import { parse } from "path";

const Home = () => {
  const [modalIsOpen, setModal] = useState(true);
  const [dataList, setDataList] = useState<{ id: string; latitude_min: string; longitude_min: string; latitude_max: string; longitude_max: string; probability: string; }[]>([]);
  const [probabilityThreshold, setProbabilityThreshold] = useState(0.5);
  const [map, setMap] = useState<google.maps.Map | null>(null);
  const [circles, setCircles] = useState<google.maps.Circle[]>([]);
  const [circlesWithData, setCirclesWithData] = useState<CircleWithData[]>([]);

  useEffect(() => {
    setDataList(sample_json);
  }, []);

  interface CircleWithData {
    circle: google.maps.Circle;
    probability: number;
  }

  useEffect(() => {
    if (map) {
      dataList.forEach(data => {
        var possibilityColor: any = "rgb(255, 255, 255)";
        if (parseFloat(data.probability) >= 0.8) {
          possibilityColor = "rgb(0, 100, 25";
        } else if (parseFloat(data.probability) >= 0.6) {
          possibilityColor = "rgb(0, 255, 64)";
        } else if (parseFloat(data.probability) >= 0.4) {
          possibilityColor = "rgb(255, 255, 0)";
        } else if (parseFloat(data.probability) >= 0.2) {
          possibilityColor = "rgb(255, 100, 0)";
        } else {
          possibilityColor = "rgb(255, 0, 0)";
        }

        if (parseFloat(data.probability) > probabilityThreshold) {
          const circle = new google.maps.Circle({
            center: {
              lat: parseFloat(data.longitude_min),
              lng: parseFloat(data.latitude_min),
            },
            strokeColor: possibilityColor,
            strokeOpacity: 1,
            strokeWeight: 2,
            fillColor: possibilityColor,
            fillOpacity: 1,
            visible: true,
            radius: 200,
            map: map
          });
          const circleWithData: CircleWithData = {
            circle: circle,
            probability: parseFloat(data.probability)
          };
          setCirclesWithData(prevCircles => [...prevCircles, circleWithData]);
        }
      });
      // setCircles(newCircles);
    }
  }, [probabilityThreshold, map]);

  const removeCircle = (circleToRemove:google.maps.Circle) => {
    const updatedCircles = circles.filter(circle => circle !== circleToRemove);
    circleToRemove.setMap(null);
    setCircles(updatedCircles);
  };

  const handleMapLoad = (mapInstance: google.maps.Map) => {
    setMap(mapInstance);
  };

  const handleSliderChange = (event: ChangeEvent<HTMLInputElement>) => {
    const newProbabilityThreshold = parseFloat(event.target.value);
    setProbabilityThreshold(newProbabilityThreshold);
    circlesWithData.forEach(circleData => {
      if (circleData.probability <= newProbabilityThreshold) {
        removeCircle(circleData.circle);
      }
    });
  };

  const openModal = () => {
      setModal(true);
  };
  const closeModal = () => {
      setModal(false);
  };

  const API_KEY = process.env.REACT_APP_GOOGLE_MAP
  if (!API_KEY) {
      return (
          <div className="h-screen flex justify-center items-center">
              Error: Google Maps API Key is not defined.
          </div>
      );
  }

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
    strokeColor: "rgb(254, 0, 0)",
    strokeOpacity: 1,
    strokeWiehgt: 2,
    fillColor: "rgb(255, 0, 0)",
    fillOpacity: 1,
    visible: true,
    radius: 150000
  };

  const modalStyle: Modal.Styles = {
    overlay: {
        position: 'fixed',
        top: 0,
        left: 0,
        backgroundColor: 'rgba(0,0, 0, 1)',
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
            <img src="image/logo_black_text.png" className="h-40"/>
            <div className="text-white text-2xl my-10">
            You can view the area where seaweed live, which was judged from satellite images.
            </div>
            <button onClick={closeModal} className="text-3xl text-black bg-white hover:bg-gray-500 px-5 py-1 rounded-3xl">
              Get Started
            </button>
          </div>
          <div className="text-gray-300 text-3xl mt-12">
              {/* AquaMind is available at */}
          </div>
        </div>
      </Modal>
      <div className="App None h-screen" id="top">
        {!modalIsOpen && <Header />}
        <div className="h-screen flex justify-center items-center" style={{background: 'rgb(18,18,31)'}}>          
          <div className="flex flex-col">
            <input
              type="range"
              min={0}
              max={1}
              step={0.01}
              value={probabilityThreshold}
              onChange={handleSliderChange}
            />
            <button className="text-3xl text-gray-300 bg-gray-900 hover:bg-black px-5 py-1 rounded-lg">
              Switch to map
            </button>
            <button className="text-3xl text-gray-300 bg-gray-900 hover:bg-black px-5 py-1 rounded-lg">
              Switch to satellite img
            </button>
          </div>
            {/* <div className="bg-white" style={{ width: `${60}%`, height: `${80}vh` }}></div> */}
            <LoadScript googleMapsApiKey={API_KEY}>
              <GoogleMap
                mapContainerStyle={{width: "100%",height: "100vh"}}
                center={{lat: 24.4664,lng: 124.2054}}
                zoom={11}
                options={mapOptions}
                onLoad={handleMapLoad}
              >
              </GoogleMap>
            </LoadScript>
        </div>
      </div>
    </div>
  );
};

export default Home;
