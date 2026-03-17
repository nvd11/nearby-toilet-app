import React, { useState, useEffect } from 'react';
import { StyleSheet, View, Text, ActivityIndicator } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import * as Location from 'expo-location';
import axios from 'axios';

export default function App() {
  const [location, setLocation] = useState(null);
  const [toilets, setToilets] = useState([]);
  const [errorMsg, setErrorMsg] = useState(null);

  useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setErrorMsg('Permission to access location was denied');
        return;
      }

      let loc = await Location.getCurrentPositionAsync({});
      setLocation(loc.coords);
      fetchToilets(loc.coords.latitude, loc.coords.longitude);
    })();
  }, []);

  const fetchToilets = async (lat, lon) => {
    try {
      // Overpass API to find nearby public toilets (amenity=toilets)
      const radius = 2000; // 2km
      const query = `
        [out:json];
        node["amenity"="toilets"](around:${radius},${lat},${lon});
        out;
      `;
      const response = await axios.post('https://overpass-api.de/api/interpreter', query);
      if (response.data && response.data.elements) {
        setToilets(response.data.elements);
      }
    } catch (err) {
      console.error(err);
    }
  };

  if (errorMsg) {
    return <View style={styles.container}><Text>{errorMsg}</Text></View>;
  }

  if (!location) {
    return <View style={styles.container}><ActivityIndicator size="large" color="#0000ff" /></View>;
  }

  return (
    <View style={styles.container}>
      <MapView 
        style={styles.map}
        initialRegion={{
          latitude: location.latitude,
          longitude: location.longitude,
          latitudeDelta: 0.05,
          longitudeDelta: 0.05,
        }}
        showsUserLocation={true}
      >
        {toilets.map((toilet) => (
          <Marker
            key={toilet.id}
            coordinate={{
              latitude: toilet.lat,
              longitude: toilet.lon,
            }}
            title={toilet.tags?.name || "Public Toilet"}
            description={toilet.tags?.fee === "yes" ? "Paid" : "Free"}
          />
        ))}
      </MapView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', alignItems: 'center', justifyContent: 'center' },
  map: { width: '100%', height: '100%' },
});
