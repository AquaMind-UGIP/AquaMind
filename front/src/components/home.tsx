import { useState, useEffect, ChangeEvent } from "react";
import { GoogleMap, DrawingManager, Polygon, LoadScript } from "@react-google-maps/api";
import Modal from 'react-modal'
import Header from "./Header";
import inference_json from './inference.json';

const Home = () => {
  const [modalIsOpen, setModal] = useState(true);
  const [dataList, setDataList] = useState<{ id: string; latitude_min: string; longitude_min: string; latitude_max: string; longitude_max: string; probability: string; }[]>([]);
  const [probabilityThreshold, setProbabilityThreshold] = useState(0.75);
  const [map, setMap] = useState<google.maps.Map | null>(null);
  const [circles, setCircles] = useState<google.maps.Circle[]>([]);
  const [circlesWithData, setCirclesWithData] = useState<CircleWithData[]>([]);
  const [area50, setAarea50] = useState(0);
  const [area60, setAarea60] = useState(0);
  const [area70, setAarea70] = useState(0);
  const [area80, setAarea80] = useState(0);
  const [area90, setAarea90] = useState(0);
  const [area50rate, setAarea50rate] = useState(0);
  const [area60rate, setAarea60rate] = useState(0);
  const [area70rate, setAarea70rate] = useState(0);
  const [area80rate, setAarea80rate] = useState(0);
  const [area90rate, setAarea90rate] = useState(0);

  useEffect(() => {
    setDataList(inference_json);
  }, []);

  interface CircleWithData {
    circle: google.maps.Circle;
    probability: number;
  }

  useEffect(() => {
    var count50 = 0;
    var count60 = 0;
    var count70 = 0;
    var count80 = 0;
    var count90 = 0;
    if (map) {
      dataList.forEach(data => {
        var possibilityColor: any = "rgb(255, 255, 255)";

        if (parseFloat(data.probability) > probabilityThreshold) {
          if (parseFloat(data.probability) >= 0.9) {
            possibilityColor = "rgb(0, 100, 25";
            count90 = count90 + 1;
          } else if (parseFloat(data.probability) >= 0.8) {
            possibilityColor = "rgb(0, 255, 64)";
            count80 = count80 + 1;
          } else if (parseFloat(data.probability) >= 0.7) {
            possibilityColor = "rgb(255, 255, 0)";
            count70 = count70 + 1;
          } else if (parseFloat(data.probability) >= 0.6) {
            possibilityColor = "rgb(255, 100, 0)";
            count60 = count60 + 1;
          } else {
            possibilityColor = "rgb(255, 0, 0)";
            count50 = count50 + 1;
          }

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
    }
    const area50 = count50 * 31415;
    const area60 = count60 * 31415;
    const area70 = count70 * 31415;
    const area80 = count80 * 31415;
    const area90 = count90 * 31415;
    const area50rate = (area50 / (area50 + area60 + area70 + area80 + area90))*100;
    const area60rate = (area60 / (area50 + area60 + area70 + area80 + area90))*100;
    const area70rate = (area70 / (area50 + area60 + area70 + area80 + area90))*100;
    const area80rate = (area80 / (area50 + area60 + area70 + area80 + area90))*100;
    const area90rate = (area90 / (area50 + area60 + area70 + area80 + area90))*100;

    setAarea50(area50);
    setAarea60(area60);
    setAarea70(area70);
    setAarea80(area80);
    setAarea90(area90);
    setAarea50rate(area50rate);
    setAarea60rate(area60rate);
    setAarea70rate(area70rate);
    setAarea80rate(area80rate);
    setAarea90rate(area90rate);
  }, [probabilityThreshold, map]);

  const removeCircle = (circleToRemove:google.maps.Circle) => {
    const updatedCircles = circles.filter(circle => circle !== circleToRemove);
    circleToRemove.setMap(null);
    setAarea50(0);
    setAarea60(0);
    setAarea70(0);
    setAarea80(0);
    setAarea90(0);
    setAarea50rate(0);
    setAarea60rate(0);
    setAarea70rate(0);
    setAarea80rate(0);
    setAarea90rate(0);
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
              north: 25.83,
              south: 23.83,
              east: 126.31,
              west: 124.31,
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
          <div className="mx-5">
            <div className="flex flex-col">
              {/* <button className="text-3xl text-gray-300 bg-gray-900 hover:bg-black px-5 py-1 rounded-lg">
                Switch to map
              </button> */}
              <div className="text-black bg-white rounded-xl px-4">
                <div className="text-2xl mt-4">Seagrasses Distribution</div>
                <div className="text-2xl">Probability Threshold</div>
                <div className="flex justify-center items-center">
                  <div className="my-4">
                    <div className="">
                      <input
                        type="range"
                        min={0.5}
                        max={1}
                        step={0.01}
                        value={probabilityThreshold}
                        onChange={handleSliderChange}
                        style={{ width: '100%' }}
                      />
                    </div>
                    <div className="w-80 mt-2 text-left text-lg">
                      The further right the slider, the higher probability seagrass is displayed, while the further left, the lower probability seagrass is also displayed.
                    </div>
                    <div className="flex item-center justify-center mt-4">
                      <div className="w-14 h-2 bg-red-500"></div>
                      <div className="w-14 h-2 bg-yellow-500"></div>
                      <div className="w-14 h-2 bg-yellow-300"></div>
                      <div className="w-14 h-2 bg-green-500"></div>
                      <div className="w-14 h-2 bg-green-900"></div>
                    </div>
                    <div>
                      <div className="flex justify-between text-sm">
                        <div>50%</div>
                        <div>60%</div>
                        <div>70%</div>
                        <div>80%</div>
                        <div>90%</div>
                        <div>100%</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="mt-5 text-black text-2xl bg-white rounded-xl px-8">
                <div className="my-4">Distribution Analysis</div>
                <div className="flex items-center">
                  <div className="w-5 h-5 rounded-full bg-red-500 mr-2"></div>
                  <div className="w-28">{area50.toString()}</div>
                  <div><var>km<sup>2</sup></var></div>
                  <div className="w-24">（{area50rate.toFixed(2).toString()}%）</div>
                </div>
                <div className="flex items-center">
                  <div className="w-5 h-5 rounded-full bg-yellow-500 mr-2"></div>
                  <div className="w-28">{area60.toString()}</div>
                  <div><var>km<sup>2</sup></var></div>
                  <div className="w-24">（{area60rate.toFixed(2).toString()}%）</div>
                </div>
                <div className="flex items-center">
                  <div className="w-5 h-5 rounded-full bg-yellow-300 mr-2"></div>
                  <div className="w-28">{area70.toString()}</div>
                  <div><var>km<sup>2</sup></var></div>
                  <div className="w-24">（{area70rate.toFixed(2).toString()}%）</div>
                </div>
                <div className="flex items-center">
                  <div className="w-5 h-5 rounded-full bg-green-500 mr-2"></div>
                  <div className="w-28">{area80.toString()}</div>
                  <div><var>km<sup>2</sup></var></div>
                  <div className="w-24">（{area80rate.toFixed(2).toString()}%）</div>
                </div>
                <div className="flex items-center mb-4">
                  <div className="w-5 h-5 rounded-full bg-green-900 mr-2"></div>
                  <div className="w-28">{area90.toString()}</div>
                  <div><var>km<sup>2</sup></var></div>
                  <div className="w-24">（{area90rate.toFixed(2).toString()}%）</div>
                </div>
              </div>
            </div>
          </div>
            {/* <div className="bg-white" style={{ width: `${60}%`, height: `${80}vh` }}></div> */}
            <LoadScript googleMapsApiKey={API_KEY}>
              <GoogleMap
                mapContainerStyle={{width: "100%",height: "100vh"}}
                center={{lat: 24.83,lng: 125.31}}
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

  // const [polygons, setPolygons] = useState<{ lat: number; lng: number; }[][]>([]);

  // const handlePolygonComplete = (polygon: google.maps.Polygon) => {
  //   const paths = polygon.getPath().getArray().map(latLng => ({
  //     lat: latLng.lat(),
  //     lng: latLng.lng()
  //   }));
  //   setPolygons([...polygons, paths]);
  // };

  // return (
  //   <LoadScript googleMapsApiKey={API_KEY}>
  //     <GoogleMap
  //       zoom={10}
  //       center={{ lat: 0, lng: 0 }}
  //     >
  //       <DrawingManager
  //         onPolygonComplete={handlePolygonComplete}
  //         options={{
  //           drawingControl: true,
  //           drawingControlOptions: {
  //             position: window.google.maps.ControlPosition.TOP_CENTER,
  //             drawingModes: [window.google.maps.drawing.OverlayType.POLYGON],
  //           },
  //           polygonOptions: {
  //             fillColor: '#00FF00',
  //             fillOpacity: 0.5,
  //             strokeWeight: 2,
  //             clickable: true,
  //             editable: true,
  //             zIndex: 1,
  //           },
  //         }}
  //       />
  //       {polygons.map((paths, index) => (
  //         <Polygon key={index} paths={paths} />
  //       ))}
  //     </GoogleMap>
  //   </LoadScript>
  // );
};

export default Home;
